from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path

from app.config import Settings
from app.recognizers.agent import (
    prepare_crops,
    list_pending_payloads,
    load_validated_payload,
)
from app.recognizers.base import AgentReadRequired, RecognitionError
from app.sheets_gateway import SheetsGateway


@dataclass
class PdfZmk2FullResult:
    tool: str
    status: str
    input_dir: str
    total_files: int
    processed_files: int
    skipped_files: int
    rows_count: int
    sheet_written: bool
    elapsed_seconds: float
    processed: list[str]
    skipped: list[dict[str, str]]


def build_pdf_zmk2_values_from_payload(payload: dict) -> list[list[str]]:
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("Payload field 'items' must be a list.")

    header_group = [
        "отпр. элем.",
        "дет.",
        "КОЛ.",
        "",
        "",
        "",
        "МАССА В КГ",
        "",
        "",
        "марка стали",
        "примечания",
    ]
    header_columns = [
        "отпр. элем.",
        "дет.",
        "т.",
        "н.",
        "сечение",
        "длина",
        "шт.",
        "общ.",
        "элем.",
        "марка стали",
        "примечания",
    ]

    values = [header_group, header_columns]
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Each item must be an object.")
        values.append(
            [
                str(item.get("elem", "")),
                str(item.get("det", "")),
                str(item.get("t", "")),
                str(item.get("n", "")),
                str(item.get("section", "")),
                str(item.get("length", "")),
                str(item.get("mass_sht", "")),
                str(item.get("mass_total", "")),
                str(item.get("mass_elem", "")),
                str(item.get("steel", "")),
                str(item.get("note", "")),
            ]
        )

    if len(values) == 2:
        drawing = payload.get("drawing_name", "unknown")
        raise ValueError(
            f"No items extracted for drawing '{drawing}'. "
            "Strict contract forbids unresolved payloads."
        )
    return values


def run_pdf_zmk2_full(
    input_dir: Path,
    settings: Settings,
    sheet_write: bool = False,
    dry_run: bool = False,
    output_json: Path | None = None,
    workers: int = 6,
) -> PdfZmk2FullResult:
    """
    Strict pipeline for PDF_ZMK2. Three explicit phases:

    ┌─────────────────────────────────────────────────────┐
    │ PHASE 1  crop + upscale                             │
    │   For every image in input_dir:                     │
    │   → crop table region                               │
    │   → upscale x4                                      │
    │   → save data/recognition/<slug>.table_x4.jpg       │
    ├─────────────────────────────────────────────────────┤
    │ PHASE 2  agent read  (HARD GATE)                    │
    │   For every crop without a valid JSON payload:      │
    │   → raises AgentReadRequired                        │
    │   → the Cursor agent MUST read each crop,           │
    │     extract table data, write <slug>.json            │
    │   → then re-run this function                       │
    ├─────────────────────────────────────────────────────┤
    │ PHASE 3  normalize + sheets                         │
    │   Load all payload JSONs                            │
    │   → normalize rows                                  │
    │   → write to Google Sheet PDF_ZMK2                  │
    └─────────────────────────────────────────────────────┘
    """
    start = time.perf_counter()

    # ── PHASE 1: crop + upscale ──────────────────────────────────────
    prepared = prepare_crops(input_dir)
    total_files = len(prepared)

    # ── PHASE 2: agent read gate ─────────────────────────────────────
    pending = list_pending_payloads(prepared)
    if pending:
        raise AgentReadRequired(pending)

    # ── PHASE 3: normalize + sheets ──────────────────────────────────
    processed: list[tuple[str, list[list[str]]]] = []
    skipped: list[dict[str, str]] = []

    for source, slug, _crop, payload_path in prepared:
        try:
            if source.suffix.lower() == ".json":
                payload = load_validated_payload(source)
            else:
                payload = load_validated_payload(payload_path)
            values = build_pdf_zmk2_values_from_payload(payload)
            processed.append((source.name, values))
        except (RecognitionError, ValueError) as exc:
            skipped.append({"file": source.name, "reason": str(exc)})

    if skipped:
        sample = "; ".join(
            f"{s['file']}: {s['reason']}" for s in skipped[:3]
        )
        raise RuntimeError(
            f"pdf-zmk2 full failed: {len(skipped)} file(s) with errors. "
            f"Examples: {sample}"
        )

    processed.sort(key=lambda x: x[0])
    merged_values: list[list[str]] = []
    rows_count = 0
    for idx, (_name, block) in enumerate(processed):
        if idx == 0:
            merged_values.extend(block)
        else:
            merged_values.append([])
            merged_values.extend(block[2:])
        rows_count += max(0, len(block) - 2)

    sheet_written = False
    if merged_values and sheet_write and not dry_run:
        SheetsGateway(settings).write_values(settings.sheet_pdf_zmk2, merged_values)
        sheet_written = True

    elapsed_seconds = round(time.perf_counter() - start, 3)
    result = PdfZmk2FullResult(
        tool="pdf-zmk2-full",
        status="ok",
        input_dir=str(input_dir),
        total_files=total_files,
        processed_files=len(processed),
        skipped_files=len(skipped),
        rows_count=rows_count,
        sheet_written=sheet_written,
        elapsed_seconds=elapsed_seconds,
        processed=[name for name, _ in processed],
        skipped=skipped,
    )
    if output_json is not None:
        output_json.parent.mkdir(parents=True, exist_ok=True)
        output_json.write_text(
            json.dumps(asdict(result), ensure_ascii=False, indent=2), encoding="utf-8"
        )
    return result
