## Raw-спецификации

- `data/raw_specs/pdf_zmk/*.csv` — сырые спецификации для листа `PDF_ZMK`.
  - Формат колонок: `poz;designation;name;qty;weight`.
  - Эти файлы повторяют таблицу чертежа `Поз / Обозначение / Наименование / Кол / Примеч.` без нормализации.
- `data/raw_specs/pdf_zmk2/*.csv` — сырые спецификации стали для листа `PDF_ZMK2`.
  - Формат: `elem;det;t;n;section;length;mass_sht;mass_total;note`.

## Пайплайн

1. Добавить новый чертёж (JPEG) в `new/`.
2. Если таблица мелкая — запустить `crop_tables.py` и использовать кроп из `new_crops/*_table_x2.jpg` для снятия данных.
3. Создать raw‑CSV в соответствующей папке `data/raw_specs/...` по таблице спецификации.
4. Запустить:

   ```bash
   python3 write_pdf_zmk.py
   ```

5. Скрипт вызовет нормализаторы:
   - `normalizer/pdf_zmk_normalizer.py` → перегенерирует `data/pdf_zmk_baza2.csv` и лист `PDF_ZMK` (Лист / Круг / Метизы).
   - `normalizer/pdf_zmk2_normalizer.py` → перегенерирует `data/pdf_zmk2_spec.csv` и лист `PDF_ZMK2`.

