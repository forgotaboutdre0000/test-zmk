from __future__ import annotations

import csv
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from normalizer.pdf_zmk_normalizer import generate_pdf_zmk_values
from normalizer.pdf_zmk2_normalizer import generate_pdf_zmk2_values


SPREADSHEET_ID = "1gT9H5wAfs-MRzId0E5TarF7Qo6pvNOl0lsUbWIi_1kc"
SHEET_NAME = "PDF_ZMK"
SHEET_NAME_SPEC = "PDF_ZMK2"


RAW_ITEMS_530_12 = [
    {
        "poz": 1,
        "size": "490x275x8",
        "name": "Основание",
        "qty": 1,
        "weight": "8,41",
        "note": "",
    },
    {
        "poz": 2,
        "size": "695x240x8",
        "name": "Угольник",
        "qty": 2,
        "weight": "8,34",
        "note": "",
    },
    {
        "poz": 3,
        "size": "663x275x10",
        "name": "Подушка",
        "qty": 1,
        "weight": "14,21",
        "note": "",
    },
    {
        "poz": 4,
        "size": "292x80x8",
        "name": "Проушина",
        "qty": 4,
        "weight": "1,29",
        "note": "",
    },
    {
        "poz": 5,
        "size": "d24x1450",
        "name": "Хомут",
        "qty": 2,
        "weight": "5,12",
        "note": "",
    },
    {
        "poz": 6,
        "size": "",
        "name": "Гайка М24 ГОСТ 5915-70",
        "qty": 8,
        "weight": "0,123",
        "note": "",
    },
]


RAW_ITEMS_720_14 = [
    {
        "poz": 1,
        "size": "660x330x10",
        "name": "Основание",
        "qty": 1,
        "weight": "16,99",
        "note": "",
    },
    {
        "poz": 2,
        "size": "910x295x10",
        "name": "Угольник",
        "qty": 2,
        "weight": "16,32",
        "note": "",
    },
    {
        "poz": 3,
        "size": "555x100x10",
        "name": "Проушина",
        "qty": 4,
        "weight": "3,93",
        "note": "",
    },
    {
        "poz": 4,
        "size": "910x330x13",
        "name": "Подушка",
        "qty": 1,
        "weight": "30,45",
        "note": "",
    },
    {
        "poz": 5,
        "size": "d30x2080",
        "name": "Хомут",
        "qty": 2,
        "weight": "11,47",
        "note": "",
    },
    {
        "poz": 6,
        "size": "",
        "name": "Гайка М30 ГОСТ 5915-70",
        "qty": 8,
        "weight": "0,24",
        "note": "",
    },
    {
        "poz": 7,
        "size": "",
        "name": "Шайба 16 ГОСТ 11371-78",
        "qty": 4,
        "weight": "0,05",
        "note": "",
    },
]


RAW_ITEMS_OPH_32_000 = [
    {
        "poz": 1,
        "size": "333x200x4",
        "name": "Скоба",
        "qty": 1,
        "weight": "2,08",
        "note": "",
    },
    {
        "poz": 2,
        "size": "250x40x4",
        "name": "Полухомут",
        "qty": 1,
        "weight": "0,31",
        "note": "",
    },
    {
        "poz": 3,
        "size": "",
        "name": "Болт М10х40 ГОСТ 7798-70",
        "qty": 4,
        "weight": "0,036",
        "note": "",
    },
    {
        "poz": 4,
        "size": "",
        "name": "Гайка М10 ГОСТ 5915-70",
        "qty": 8,
        "weight": "0,012",
        "note": "",
    },
]


RAW_ITEMS_OPH_40_000 = [
    {
        "poz": 1,
        "size": "333x200x4",
        "name": "Скоба",
        "qty": 1,
        "weight": "2,08",
        "note": "",
    },
    {
        "poz": 2,
        "size": "250x40x4",
        "name": "Полухомут",
        "qty": 1,
        "weight": "0,31",
        "note": "",
    },
    {
        "poz": 3,
        "size": "",
        "name": "Болт М10х40 ГОСТ 7798-70",
        "qty": 4,
        "weight": "0,036",
        "note": "",
    },
    {
        "poz": 4,
        "size": "",
        "name": "Гайка М10 ГОСТ 5915-70",
        "qty": 8,
        "weight": "0,012",
        "note": "",
    },
]


RAW_ITEMS_OPH_50_000 = [
    {
        "poz": 1,
        "size": "375x200x4",
        "name": "Скоба",
        "qty": 1,
        "weight": "2,34",
        "note": "",
    },
    {
        "poz": 2,
        "size": "296x40x4",
        "name": "Полухомут",
        "qty": 1,
        "weight": "0,36",
        "note": "",
    },
    {
        "poz": 3,
        "size": "",
        "name": "Болт М10х40 ГОСТ 7798-70",
        "qty": 4,
        "weight": "0,036",
        "note": "",
    },
    {
        "poz": 4,
        "size": "",
        "name": "Гайка М10 ГОСТ 5915-70",
        "qty": 8,
        "weight": "0,012",
        "note": "",
    },
]


SPEC_630_13 = [
    # Порядок строк как на чертеже — сверху вниз
    # В самом чертеже первая колонка (отпр. элем.) пустая,
    # значения начинаются со второй колонки (дет.) и третьей (т.)
    {
        "elem": "",  # отпр. элем.
        "det": 8,
        "t": 4,
        "n": "",
        "section": "Шайба 30 ГОСТ 11371-78*",
        "length": "",
        "mass_sht": "0,053",
        "mass_total": "0,21",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 7,
        "t": 8,
        "n": "",
        "section": "Гайка М30.8 ГОСТ 5915-70*",
        "length": "",
        "mass_sht": "0,242",
        "mass_total": "1,94",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 5,
        "t": 2,
        "n": "",
        "section": "КрГ30",
        "length": 1676,
        "mass_sht": "9,3",
        "mass_total": "18,6",
        "mass_elem": "",
        "steel": "",
        "note": "нар. резьбу, гнуть",
    },
    {
        "elem": "",
        "det": 4,
        "t": 1,
        "n": "",
        "section": "305x14",
        "length": 780,
        "mass_sht": "26,14",
        "mass_total": "26,14",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 3,
        "t": 1,
        "n": "",
        "section": "95x10",
        "length": 328,
        "mass_sht": "2,05",
        "mass_total": "2,05",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
    {
        "elem": "",
        "det": 2,
        "t": 1,
        "n": "",
        "section": "305x10",
        "length": 590,
        "mass_sht": "14,12",
        "mass_total": "14,12",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
    {
        "elem": "",
        "det": 1,
        "t": 2,
        "n": "",
        "section": "280x10",
        "length": 810,
        "mass_sht": "15,0",
        "mass_total": "30,0",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
]


SPEC_426_10 = [
    # Структура аналогична 630-13, значения прочитаны с чертежа 426-10
    {
        "elem": "",
        "det": 8,
        "t": 4,
        "n": "",
        "section": "Шайба 24 ГОСТ 11371-78*",
        "length": "",
        "mass_sht": "0,053",
        "mass_total": "0,21",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 7,
        "t": 8,
        "n": "",
        "section": "Гайка М24.8 ГОСТ 5915-70*",
        "length": "",
        "mass_sht": "0,242",
        "mass_total": "1,94",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 5,
        "t": 2,
        "n": "",
        "section": "КрГ24",
        "length": 1676,
        "mass_sht": "7,06",
        "mass_total": "14,12",
        "mass_elem": "",
        "steel": "",
        "note": "нар. резьбу, гнуть",
    },
    {
        "elem": "",
        "det": 4,
        "t": 1,
        "n": "",
        "section": "305x14",
        "length": 780,
        "mass_sht": "19,63",
        "mass_total": "19,63",
        "mass_elem": "",
        "steel": "",
        "note": "",
    },
    {
        "elem": "",
        "det": 3,
        "t": 1,
        "n": "",
        "section": "95x10",
        "length": 328,
        "mass_sht": "1,54",
        "mass_total": "1,54",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
    {
        "elem": "",
        "det": 2,
        "t": 1,
        "n": "",
        "section": "305x10",
        "length": 590,
        "mass_sht": "10,92",
        "mass_total": "10,92",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
    {
        "elem": "",
        "det": 1,
        "t": 2,
        "n": "",
        "section": "280x10",
        "length": 810,
        "mass_sht": "11,58",
        "mass_total": "23,16",
        "mass_elem": "",
        "steel": "",
        "note": "гнуть",
    },
]


def _split_size_and_thickness(size: str) -> tuple[str, str]:
    """
    Разделяет строку вида '490x275x8' на:
    - '490x275x8' как размер листовой детали
    - '8' как толщину.
    Если формат другой или пусто, возвращает (size, '').
    """
    if not size:
        return "", ""
    if "x" not in size:
        return size, ""
    parts = size.split("x")
    if len(parts) < 2:
        return size, ""
    thickness = parts[-1].lstrip("dDØø")
    return size, thickness


def transform_to_baza2_rows(drawing_name: str, items: list[dict]) -> list[list[str]]:
    """
    Преобразует сырые позиции спецификации в формат, как в baza2_example.csv.
    """
    rows: list[list[str]] = []

    for item in items:
        poz = str(item["poz"])
        part_name = item["name"]
        qty = str(item["qty"])
        weight = item["weight"]
        size = item["size"]

        sheet_size = ""
        thickness = ""
        circle_size = ""
        circle_qty = ""
        fastener_name = ""
        fastener_qty = ""
        short_part_name = part_name

        if part_name in {"Основание", "Угольник", "Подушка", "Проушина", "Ложемент", "Шило", "Ушко"}:
            sheet_size, thickness = _split_size_and_thickness(size)
        elif part_name == "Хомут":
            # Деталь из круга: d24x1450 -> М24х1450
            circle_qty = qty
            thickness = "—"
            if size:
                size_body = size.lstrip("dD").replace("x", "х")
                circle_size = f"М{size_body}"
        elif part_name.startswith("Гайка") or part_name.startswith("Шайба"):
            short_part_name = part_name.split()[0]
            fastener_name = part_name
            fastener_qty = qty
            thickness = "—"

        row = [
            poz,
            drawing_name,
            sheet_size,
            qty if sheet_size or part_name == "Хомут" else "",
            weight,
            short_part_name,
            thickness,
            circle_size,
            circle_qty,
            fastener_name,
            fastener_qty,
        ]
        rows.append(row)

    return rows


def transform_to_spec_rows(items: list[dict]) -> list[list[str]]:
    """
    Преобразует спецификацию типа 630-13 в плоские строки для PDF_ZMK2.
    """
    rows: list[list[str]] = []
    for item in items:
        rows.append(
            [
                str(item["elem"]),
                str(item["det"]),
                str(item["t"]),
                str(item["n"]),
                item["section"],
                str(item["length"]),
                item["mass_sht"],
                item["mass_total"],
                item["mass_elem"],
                item["steel"],
                item["note"],
            ]
        )
    return rows


def get_sheets_service():
    creds = Credentials.from_authorized_user_file(
        "token.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )
    return build("sheets", "v4", credentials=creds)


def main():
    service = get_sheets_service()

    # Готовим директорию для выходных CSV
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # --- Лист PDF_ZMK: генерируем значения из raw-спецификаций и заливаем ---
    pdf_zmk_values = generate_pdf_zmk_values()

    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME,
        body={},
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A1",
        valueInputOption="RAW",
        body={"values": pdf_zmk_values},
    ).execute()

    # Стилизуем шапку: строки с группами/заголовками
    spreadsheet = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID,
        fields="sheets(properties.sheetId,properties.title)",
    ).execute()
    sheet_id = None
    for sh in spreadsheet.get("sheets", []):
        props = sh.get("properties", {})
        if props.get("title") == SHEET_NAME:
            sheet_id = props.get("sheetId")
            break

    if sheet_id is not None and len(pdf_zmk_values) >= 2:
        requests = [
            # Лист: столбцы C–G (индексы 2–7) во второй строке (index 1)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": 2,
                        "endColumnIndex": 7,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.85,
                                "green": 0.94,
                                "blue": 0.82,
                            }
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor",
                }
            },
            # Круг: столбцы H–I (7–9)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": 7,
                        "endColumnIndex": 9,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.82,
                                "green": 0.89,
                                "blue": 0.96,
                            }
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor",
                }
            },
            # Метизы: столбцы J–K (9–11)
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": 1,
                        "endRowIndex": 2,
                        "startColumnIndex": 9,
                        "endColumnIndex": 11,
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 0.99,
                                "green": 0.9,
                                "blue": 0.8,
                            }
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor",
                }
            },
        ]

        service.spreadsheets().batchUpdate(
            spreadsheetId=SPREADSHEET_ID,
            body={"requests": requests},
        ).execute()

    # --- Лист PDF_ZMK2: генерируем значения и заливаем ---
    pdf_spec_values = generate_pdf_zmk2_values()

    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME_SPEC,
        body={},
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME_SPEC}!A1",
        valueInputOption="RAW",
        body={"values": pdf_spec_values},
    ).execute()


if __name__ == "__main__":
    main()

