import os
import random
import shutil
from pathlib import Path

# =========================
# 1. 경로 설정
# =========================

# 원본 데이터셋 경로
# 본인 컴퓨터 경로에 맞게 수정하세요.
SOURCE_DIR = Path(r"C:\Users\wodyd\Downloads\road_damage_yolo\data")
TARGET_DIR = Path("road_damage_yolo")

SOURCE_IMAGES = SOURCE_DIR / "images"
SOURCE_LABELS = SOURCE_DIR / "labels-YOLO"

# 새로 만들 YOLO 학습용 폴더
TARGET_DIR = Path("road_damage_yolo")

TARGET_IMAGES = TARGET_DIR / "images"
TARGET_LABELS = TARGET_DIR / "labels"

# train / val / test 비율
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1

# 랜덤 고정
random.seed(42)


# =========================
# 2. 폴더 생성
# =========================

for split in ["train", "val", "test"]:
    (TARGET_IMAGES / split).mkdir(parents=True, exist_ok=True)
    (TARGET_LABELS / split).mkdir(parents=True, exist_ok=True)


# =========================
# 3. 이미지-라벨 쌍 찾기
# =========================

image_extensions = [".jpg", ".jpeg", ".png"]

image_files = []
for ext in image_extensions:
    image_files.extend(SOURCE_IMAGES.glob(f"*{ext}"))

matched_files = []

for image_path in image_files:
    label_path = SOURCE_LABELS / f"{image_path.stem}.txt"

    if label_path.exists():
        matched_files.append((image_path, label_path))
    else:
        print(f"[경고] 라벨 파일 없음: {image_path.name}")

print(f"전체 이미지 수: {len(image_files)}")
print(f"이미지-라벨 매칭 완료 수: {len(matched_files)}")


# =========================
# 4. 랜덤 셔플 후 분할
# =========================

random.shuffle(matched_files)

total = len(matched_files)
train_count = int(total * TRAIN_RATIO)
val_count = int(total * VAL_RATIO)

train_files = matched_files[:train_count]
val_files = matched_files[train_count:train_count + val_count]
test_files = matched_files[train_count + val_count:]

splits = {
    "train": train_files,
    "val": val_files,
    "test": test_files
}


# =========================
# 5. 파일 복사
# =========================

for split_name, files in splits.items():
    for image_path, label_path in files:
        shutil.copy2(image_path, TARGET_IMAGES / split_name / image_path.name)
        shutil.copy2(label_path, TARGET_LABELS / split_name / label_path.name)

    print(f"{split_name}: {len(files)}개 복사 완료")


# =========================
# 6. data.yaml 생성
# =========================

yaml_content = """path: ./road_damage_yolo
train: images/train
val: images/val
test: images/test

nc: 3
names:
  0: pothole
  1: crack
  2: manhole
"""

with open(TARGET_DIR / "data.yaml", "w", encoding="utf-8") as f:
    f.write(yaml_content)

print("data.yaml 생성 완료")
print("데이터셋 분할 완료")