from __future__ import annotations

from pathlib import Path

from PIL import Image


SRC_DIR = Path("new")
OUT_DIR = Path("new_crops")

# Относительные границы области, где расположена большая таблица спецификации.
# Подобрано на примере slojniy3.jpg:
#  - снизу берём весь лист;
#  - сверху отсекаем верхние ~50 % высоты;
#  - слева отсекаем область без таблицы.
LEFT_FRAC = 0.25
TOP_FRAC = 0.50

# Масштаб увеличения вырезанной области.
SCALE = 2.0


def process_image(img_path: Path) -> Path:
    """Вырезает нижнюю правую часть листа с таблицей и сохраняет увеличенный кроп."""
    img = Image.open(img_path)
    w, h = img.size

    left = int(w * LEFT_FRAC)
    top = int(h * TOP_FRAC)
    right = w
    bottom = h

    crop = img.crop((left, top, right, bottom))
    crop = crop.resize(
        (int(crop.width * SCALE), int(crop.height * SCALE)),
        Image.LANCZOS,
    )

    OUT_DIR.mkdir(exist_ok=True)
    out_path = OUT_DIR / f"{img_path.stem}_table_x2.jpg"
    crop.save(out_path, quality=95)
    return out_path


def main() -> None:
    jpg_files = sorted(SRC_DIR.glob("*.jpg"))
    if not jpg_files:
        print("No .jpg files found in", SRC_DIR)
        return

    for img_path in jpg_files:
        out_path = process_image(img_path)
        print("saved", out_path)


if __name__ == "__main__":
    main()

