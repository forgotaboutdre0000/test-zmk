from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List


RAW_PDF_ZMK2_DIR = Path("data/raw_specs/pdf_zmk2")
OUTPUT_CSV_PATH = Path("data/pdf_zmk2_spec.csv")


def _load_raw_items(path: Path) -> List[Dict[str, str]]:
    items: List[Dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for row in reader:
            items.append(
                {
                    "elem": (row.get("elem") or "").strip(),
                    "det": (row.get("det") or "").strip(),
                    "t": (row.get("t") or "").strip(),
                    "n": (row.get("n") or "").strip(),
                    "section": (row.get("section") or "").strip(),
                    "length": (row.get("length") or "").strip(),
                    "mass_sht": (row.get("mass_sht") or "").strip(),
                    "mass_total": (row.get("mass_total") or "").strip(),
                    "note": (row.get("note") or "").strip(),
                }
            )
    return items


def generate_pdf_zmk2_values() -> List[List[str]]:
    """
    Строит значения для листа PDF_ZMK2 по стальным спецификациям.
    Одновременно перезаписывает data/pdf_zmk2_spec.csv.
    """
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

    values: List[List[str]] = [header_group, header_columns]

    raw_files = sorted(RAW_PDF_ZMK2_DIR.glob("*.csv"))
    for idx, raw_path in enumerate(raw_files):
        items = _load_raw_items(raw_path)
        for item in items:
            values.append(
                [
                    item["elem"],
                    item["det"],
                    item["t"],
                    item["n"],
                    item["section"],
                    item["length"],
                    item["mass_sht"],
                    item["mass_total"],
                    item.get("mass_elem", ""),
                    "",
                    item["note"],
                ]
            )
        if idx != len(raw_files) - 1:
            values.append([])

    OUTPUT_CSV_PATH.parent.mkdir(exist_ok=True)
    with OUTPUT_CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        for row in values:
            writer.writerow(row)

    return values

