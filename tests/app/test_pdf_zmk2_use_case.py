from __future__ import annotations

import json
from pathlib import Path

import pytest
from PIL import Image

from app import cli
from app.config import Settings
from app.use_cases.pdf_zmk2 import build_pdf_zmk2_values_from_payload, run_pdf_zmk2_full


def test_build_pdf_zmk2_values_from_payload() -> None:
    values = build_pdf_zmk2_values_from_payload(
        {
            "items": [
                {
                    "elem": "",
                    "det": "8",
                    "t": "4",
                    "n": "",
                    "section": "Шайба 30 ГОСТ 11371-78*",
                    "length": "",
                    "mass_sht": "0,053",
                    "mass_total": "0,21",
                    "note": "",
                }
            ]
        }
    )
    assert len(values) == 3
    assert values[2][1] == "8"
    assert values[2][4].startswith("Шайба")


def test_build_pdf_zmk2_values_fails_on_empty_items() -> None:
    with pytest.raises(ValueError):
        build_pdf_zmk2_values_from_payload({"drawing_name": "X", "items": []})


def test_run_pdf_zmk2_full_with_json_payloads(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    input_dir = tmp_path / "input"
    input_dir.mkdir()

    for idx in range(3):
        payload = input_dir / f"steel_{idx}.json"
        payload.write_text(
            json.dumps(
                {
                    "drawing_name": f"STEEL-{idx}",
                    "items": [
                        {
                            "elem": "1",
                            "det": "1",
                            "t": "",
                            "n": "",
                            "section": "Лист 10",
                            "length": "500",
                            "mass_sht": "1,0",
                            "mass_total": "2,0",
                            "note": "",
                        }
                    ],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    result = run_pdf_zmk2_full(
        input_dir=input_dir,
        settings=Settings.from_env(),
        dry_run=True,
    )
    assert result.status == "ok"
    assert result.total_files == 3
    assert result.processed_files == 3
    assert result.skipped_files == 0


def test_cli_pdf_zmk2_full_agent_read_required(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    Image.new("RGB", (1000, 700), color="white").save(input_dir / "drawing.jpg")

    code = cli.main(
        ["pdf-zmk2", "full", "--input-dir", str(input_dir), "--dry-run"]
    )
    assert code == cli.EXIT_AGENT_READ


def test_cli_pdf_zmk2_full_dry_mode(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    Image.new("RGB", (1000, 700), color="white").save(input_dir / "doc.jpg")

    rec = tmp_path / "data" / "recognition"
    rec.mkdir(parents=True, exist_ok=True)
    (rec / "doc.json").write_text(
        json.dumps(
            {
                "drawing_name": "doc",
                "items": [
                    {
                        "elem": "1",
                        "det": "1",
                        "t": "",
                        "n": "",
                        "section": "Лист 10",
                        "length": "500",
                        "mass_sht": "1,0",
                        "mass_total": "2,0",
                        "note": "",
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    code = cli.main(
        ["pdf-zmk2", "full", "--input-dir", str(input_dir), "--dry-run"]
    )
    assert code == 0
