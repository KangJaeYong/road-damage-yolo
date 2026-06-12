from pathlib import Path

base = Path(".")

splits = ["train", "val", "test"]

for split in splits:
    image_dir = base / "images" / split
    label_dir = base / "labels" / split

    image_stems = set()
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]:
        image_stems.update(p.stem for p in image_dir.glob(ext))

    label_stems = set(p.stem for p in label_dir.glob("*.txt"))

    missing_labels = image_stems - label_stems
    missing_images = label_stems - image_stems

    print(f"\n[{split}]")
    print(f"이미지 수: {len(image_stems)}")
    print(f"라벨 수: {len(label_stems)}")
    print(f"라벨 없는 이미지 수: {len(missing_labels)}")
    print(f"이미지 없는 라벨 수: {len(missing_images)}")

    if missing_labels:
        print("라벨 없는 이미지 예시:", list(missing_labels)[:5])

    if missing_images:
        print("이미지 없는 라벨 예시:", list(missing_images)[:5])

print("\n검사 완료")