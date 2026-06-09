# YOLO 기반 도로 표면 위험요소 탐지

## 프로젝트 개요
본 프로젝트는 도로 이미지에서 포트홀, 균열, 맨홀을 탐지하는 YOLO 기반 객체탐지 프로젝트이다.

## 사용 데이터셋
Road Damage Dataset: Potholes, Cracks and Manholes

## 클래스
- pothole
- crack
- manhole

## 데이터 구조
```text
road_damage_yolo/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── data.yaml