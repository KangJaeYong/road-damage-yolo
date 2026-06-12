# YOLOv8 기반 도로 표면 위험요소 탐지 모델 학습 및 성능 비교

## 1. 프로젝트 개요

본 프로젝트는 도로 이미지 데이터를 활용하여 도로 표면에 존재하는 위험요소를 자동으로 탐지하는 객체탐지 프로젝트이다. 탐지 대상은 포트홀, 균열, 맨홀이며, YOLOv8 계열 모델을 사용하여 각 객체의 위치와 클래스를 동시에 예측한다.

도로 위의 포트홀, 균열, 맨홀 등은 차량 주행 안전과 도로 유지보수 측면에서 중요한 관리 대상이다. 기존의 도로 점검 방식은 사람이 직접 확인하거나 민원 신고에 의존하는 경우가 많아 넓은 도로망을 효율적으로 관리하는 데 한계가 있다. 따라서 본 프로젝트에서는 딥러닝 기반 객체탐지 모델을 활용하여 도로 표면 위험요소를 자동으로 탐지하고, YOLOv8 모델 크기에 따른 성능 차이를 비교하였다.

---

## 2. 문제 정의

본 프로젝트의 문제는 다음과 같이 정의할 수 있다.

> 도로 이미지가 주어졌을 때, 이미지 내에 존재하는 포트홀, 균열, 맨홀의 위치와 종류를 자동으로 탐지할 수 있는가?

이는 단순 이미지 분류 문제가 아니라 객체탐지 문제이다. 즉, 이미지 전체가 어떤 클래스에 속하는지를 판단하는 것이 아니라, 이미지 안에서 객체가 존재하는 위치를 bounding box로 찾고, 해당 객체가 pothole, crack, manhole 중 어떤 클래스인지 분류하는 문제이다.

---

## 3. 데이터셋 설명

### 3.1 데이터셋 출처

본 프로젝트에서는 Kaggle에서 제공되는 다음 데이터셋을 사용하였다.

* **Road Damage Dataset: Potholes, Cracks and Manholes**

해당 데이터셋은 도로 이미지와 함께 객체탐지 학습에 사용할 수 있는 YOLO 형식의 annotation txt 파일을 포함하고 있다.

데이터셋 전체는 용량 문제로 GitHub 저장소에 직접 포함하지 않았으며, Kaggle 원본 데이터셋을 기반으로 학습 환경에서 YOLO 학습 구조로 재구성하였다.

### 3.2 탐지 클래스

본 프로젝트에서 사용한 클래스는 다음과 같다.

| Class ID | Class Name | Description |
| -------: | ---------- | ----------- |
|        0 | pothole    | 도로 위 포트홀    |
|        1 | crack      | 도로 균열       |
|        2 | manhole    | 맨홀          |

### 3.3 데이터 구성

원본 데이터셋의 이미지와 라벨 파일을 학습에 사용할 수 있도록 train, validation, test 데이터로 분리하였다.

| 구분         | 역할                     |
| ---------- | ---------------------- |
| Train      | 모델 학습에 사용              |
| Validation | 학습 중 성능 확인 및 과적합 여부 확인 |
| Test       | 최종 성능 평가에 사용           |

YOLO 학습을 위해 이미지 파일과 라벨 파일은 같은 이름으로 대응되도록 구성하였다.

예시:

```text
images/train/example_001.jpg
labels/train/example_001.txt
```

---

## 4. 데이터 전처리 방법

YOLO 학습을 위해 데이터셋을 다음과 같은 구조로 정리하였다.

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
```

위 구조는 실제 학습 환경에서 구성한 데이터셋 구조이며, GitHub 저장소에는 데이터셋 용량 문제로 `images/`와 `labels/` 폴더를 포함하지 않았다.

전처리 과정은 다음과 같다.

1. 원본 이미지 파일과 YOLO 형식 txt 라벨 파일 확인
2. 이미지와 라벨 파일의 이름 매칭 여부 확인
3. 전체 데이터를 train, validation, test 데이터로 분할
4. YOLO 학습 구조에 맞게 `images`와 `labels` 폴더 구성
5. 클래스 정보와 데이터 경로를 포함한 `data.yaml` 작성

`data.yaml` 예시는 다음과 같다.

```yaml
path: .
train: images/train
val: images/val
test: images/test

nc: 3
names:
  0: pothole
  1: crack
  2: manhole
```

---

## 5. 사용 모델 설명

본 프로젝트에서는 PyTorch 기반 YOLOv8 모델을 사용하였다. YOLO는 이미지를 한 번에 처리하여 객체의 위치와 클래스를 동시에 예측하는 one-stage object detection 모델이다. 따라서 실시간성이 중요한 도로 위험요소 탐지 문제에 적합하다.

비교 모델은 다음 세 가지이다.

| Model   | 특징                      |
| ------- | ----------------------- |
| YOLOv8n | 가장 작은 모델, 빠른 추론 속도      |
| YOLOv8s | 속도와 정확도의 균형             |
| YOLOv8m | 더 큰 모델, 상대적으로 높은 정확도 기대 |

본 프로젝트에서는 새로운 모델 구조를 직접 설계한 것이 아니라, 기존 YOLOv8 모델을 도로 손상 데이터셋에 맞게 학습하고 성능을 비교하였다.

---

## 6. YOLO 구조 개요

YOLOv8 객체탐지 모델은 크게 다음과 같은 구조로 동작한다.

```text
Input Image
→ Backbone
→ Neck
→ Detection Head
→ Bounding Box + Class Prediction
```

각 구성 요소의 역할은 다음과 같다.

| 구성 요소          | 역할                     |
| -------------- | ---------------------- |
| Backbone       | 입력 이미지에서 특징 추출         |
| Neck           | 다양한 크기의 특징 결합          |
| Detection Head | bounding box와 class 예측 |

본 프로젝트에서는 YOLOv8 모델을 사용하여 도로 이미지에서 pothole, crack, manhole의 위치와 클래스를 예측하였다.

---

## 7. 학습 환경

본 프로젝트의 모델 학습은 AWS EC2 인스턴스 환경에서 수행하였다.

| 항목                | 내용                           |
| ----------------- | ---------------------------- |
| Cloud Environment | AWS EC2                      |
| Instance Type     | g4dn.xlarge                  |
| GPU               | NVIDIA Tesla T4              |
| Framework         | PyTorch / Ultralytics YOLOv8 |
| Python            | Python 3.12.3                |
| OS                | Ubuntu Linux                 |

---

## 8. 학습 Parameter

세 모델은 동일한 조건에서 학습하여 모델 크기별 성능 차이를 비교하였다.

| Parameter  | Value                     |
| ---------- | ------------------------- |
| Epochs     | 50                        |
| Image Size | 640                       |
| Batch Size | 16                        |
| Model      | YOLOv8n, YOLOv8s, YOLOv8m |
| Task       | Object Detection          |
| Dataset    | Road Damage Dataset       |

---

## 9. Pretrained Weight 및 Transfer Learning

본 프로젝트에서는 YOLOv8 모델을 처음부터 학습하지 않고 pretrained weight를 사용하였다.

즉, 기존에 대규모 데이터셋으로 사전 학습된 YOLOv8 모델을 기반으로 하여, 도로 손상 데이터셋에 맞게 fine-tuning하는 transfer learning 방식으로 학습을 진행하였다.

Pretrained weight를 사용한 이유는 다음과 같다.

1. 비교적 적은 데이터셋에서도 안정적인 학습 가능
2. 학습 시간 단축
3. 기존 모델이 학습한 이미지 특징 추출 능력 활용 가능
4. 처음부터 학습하는 것보다 높은 초기 성능 기대 가능

따라서 본 프로젝트는 새로운 모델 구조를 처음부터 학습한 것이 아니라, 기존 YOLOv8 모델을 도로 표면 위험요소 탐지 문제에 맞게 재학습한 방식이다.

---

## 10. 성능 비교 방법

본 프로젝트에서는 모델 크기에 따른 성능 차이를 비교하였다.

비교 대상은 다음과 같다.

* YOLOv8n
* YOLOv8s
* YOLOv8m

세 모델은 동일한 데이터셋, 동일한 image size, 동일한 epoch 조건에서 학습하였다. 이를 통해 모델 크기 변화가 탐지 정확도와 추론 속도에 어떤 영향을 주는지 확인하였다.

초기 계획에서는 입력 이미지 크기별 비교와 데이터 증강 적용 여부 비교도 고려하였으나, 최종 실험에서는 AWS EC2 학습 시간과 프로젝트 범위를 고려하여 모델 크기별 비교를 중심으로 진행하였다.

---

## 11. 성능 측정 기준

객체탐지 성능 평가는 다음 지표를 기준으로 수행하였다.

| 지표             | 의미                           |
| -------------- | ---------------------------- |
| Precision      | 모델이 탐지한 객체 중 실제 정답인 비율       |
| Recall         | 실제 객체 중 모델이 탐지에 성공한 비율       |
| mAP@0.5        | IoU 0.5 기준 평균 탐지 성능          |
| mAP@0.5:0.95   | IoU 0.5부터 0.95까지의 기준을 평균한 성능 |
| Inference Time | 이미지 한 장을 처리하는 데 걸리는 시간       |
| FPS            | 초당 처리 가능한 이미지 수              |

도로 위험요소 탐지에서는 실제 위험요소를 놓치지 않는 것이 중요하므로 Recall을 함께 고려하였다. 또한 실제 도로 모니터링 환경에서는 빠른 처리 속도도 중요하기 때문에 inference time과 FPS를 함께 비교하였다.

---

## 12. 모델별 성능 결과

최종 test 데이터에 대한 모델별 성능은 다음과 같다.

| Model   | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 | Inference Time |   FPS |
| ------- | --------: | -----: | ------: | -----------: | -------------: | ----: |
| YOLOv8n |     0.574 |  0.454 |   0.486 |        0.212 |         2.3 ms | 약 435 |
| YOLOv8s |     0.593 |  0.516 |   0.527 |        0.226 |         4.7 ms | 약 213 |
| YOLOv8m |     0.640 |  0.485 |   0.527 |        0.220 |        11.1 ms |  약 90 |

### 결과 해석

YOLOv8n은 가장 빠른 추론 속도를 보였지만, 탐지 성능은 상대적으로 낮았다. YOLOv8m은 Precision이 가장 높았지만 inference time이 크게 증가하였다. YOLOv8s는 mAP@0.5와 mAP@0.5:0.95에서 가장 우수하거나 동등한 성능을 보이면서도 YOLOv8m보다 빠른 추론 속도를 보였다.

따라서 본 데이터셋에서는 YOLOv8s가 정확도와 속도의 균형이 가장 좋은 모델로 판단된다.

---

## 13. 클래스별 성능 결과

YOLOv8s 모델 기준 클래스별 성능은 다음과 같다.

| Class   | Precision | Recall | mAP@0.5 | mAP@0.5:0.95 |
| ------- | --------: | -----: | ------: | -----------: |
| Pothole |     0.578 |  0.442 |   0.466 |        0.193 |
| Crack   |     0.496 |  0.401 |   0.369 |        0.127 |
| Manhole |     0.705 |  0.707 |   0.746 |        0.358 |

클래스별 성능을 보면 manhole 클래스의 탐지 성능이 가장 높게 나타났다. 이는 맨홀의 형태가 비교적 뚜렷하고 경계가 명확하기 때문으로 해석할 수 있다. 반면 crack 클래스는 형태가 가늘고 도로 표면의 질감, 그림자와 혼동될 수 있어 상대적으로 낮은 성능을 보였다.

---

## 14. 탐지 결과 시각화

학습된 모델을 test 이미지에 적용하여 탐지 결과를 시각화하였다. 예측 결과는 `final_results/predictions` 폴더에 저장하였다.

탐지 결과를 통해 포트홀, 균열, 맨홀 객체가 bounding box로 표시되는 것을 확인할 수 있었다. 특히 맨홀은 비교적 안정적으로 탐지되었으며, 균열은 형태가 가늘고 불규칙하여 일부 이미지에서 낮은 신뢰도 또는 미탐지가 발생할 수 있었다.

---

## 15. 학습 Log

YOLO 학습 과정에서 epoch별 loss, precision, recall, mAP 변화는 `results.png` 파일로 저장되었다.

학습 로그를 확인한 결과, box loss, class loss, dfl loss는 학습이 진행될수록 전반적으로 감소하는 경향을 보였다. 반면 Precision, Recall, mAP@0.5, mAP@0.5:0.95는 epoch가 증가함에 따라 점차 상승하였다. 이는 모델이 학습 과정에서 포트홀, 균열, 맨홀의 위치와 클래스를 점차 안정적으로 학습했음을 의미한다.

후반부에서는 mAP 증가 폭이 줄어드는 모습을 보여 학습이 어느 정도 수렴하는 경향을 확인할 수 있었다.

---

## 16. Repository 구조

GitHub 저장소의 주요 구조는 다음과 같다.

```text
road-damage-yolo/
├── README.md
├── data.yaml
├── train.py
├── requirements.txt
├── split_dataset.py
├── check_dataset.py
└── final_results/
    ├── predictions/
    ├── box_pr_curve_yolov8s.png
    ├── confusion_matrix_yolov8s.png
    ├── yolov8n_results.png
    ├── yolov8s_results.png
    └── yolov8m_results.png
```

각 파일의 역할은 다음과 같다.

| 파일/폴더              | 설명                                               |
| ------------------ | ------------------------------------------------ |
| `README.md`        | 프로젝트 설명 문서                                       |
| `data.yaml`        | YOLO 학습을 위한 데이터 경로 및 클래스 정보                      |
| `train.py`         | YOLOv8 모델 학습 코드                                  |
| `requirements.txt` | 실행에 필요한 Python 패키지 목록                            |
| `split_dataset.py` | 원본 데이터를 train/val/test로 분리하는 코드                  |
| `check_dataset.py` | 이미지와 라벨 파일 대응 여부 확인 코드                           |
| `final_results/`   | 학습 결과 이미지, PR curve, confusion matrix, 예측 이미지 저장 |

---

## 17. GitHub 관리

프로젝트 코드는 GitHub 저장소를 통해 관리하였다.

GitHub 저장소에는 다음 항목을 포함하였다.

* 학습 코드
* 데이터 설정 파일
* 실행 환경 파일
* 데이터셋 분할 및 검증 코드
* 학습 결과 이미지
* 탐지 결과 이미지
* README 문서

데이터셋 전체는 용량 문제로 GitHub에 직접 포함하지 않았으며, Kaggle 원본 데이터셋을 기반으로 학습 환경에서 YOLO 구조로 재구성하였다.

---

## 18. 실행 방법

### 18.1 패키지 설치

```bash
pip install -r requirements.txt
```

### 18.2 모델 학습

YOLOv8n 학습 예시:

```bash
yolo detect train model=yolov8n.pt data=data.yaml epochs=50 imgsz=640 batch=16 name=yolov8n_road
```

YOLOv8s 학습 예시:

```bash
yolo detect train model=yolov8s.pt data=data.yaml epochs=50 imgsz=640 batch=16 name=yolov8s_road
```

YOLOv8m 학습 예시:

```bash
yolo detect train model=yolov8m.pt data=data.yaml epochs=50 imgsz=640 batch=16 name=yolov8m_road
```

### 18.3 모델 평가

```bash
yolo detect val model=runs/detect/yolov8s_road/weights/best.pt data=data.yaml split=test
```

### 18.4 예측 결과 생성

```bash
yolo detect predict model=runs/detect/yolov8s_road/weights/best.pt source=images/test save=True
```

---

## 19. 결론

본 프로젝트에서는 YOLOv8 기반 객체탐지 모델을 사용하여 도로 이미지 내 포트홀, 균열, 맨홀을 탐지하였다. YOLOv8n, YOLOv8s, YOLOv8m 모델을 동일한 조건에서 학습하고 성능을 비교한 결과, YOLOv8s가 정확도와 추론 속도의 균형 측면에서 가장 적합한 모델로 판단되었다.

YOLOv8n은 가장 빠른 추론 속도를 보였지만 성능이 상대적으로 낮았고, YOLOv8m은 Precision은 높았지만 추론 시간이 증가하였다. YOLOv8s는 mAP와 FPS 측면에서 균형 잡힌 결과를 보여 실제 도로 모니터링 환경에 적용 가능성이 높은 모델로 분석되었다.

---

## 20. 한계 및 향후 개선 방향

본 프로젝트의 한계는 다음과 같다.

1. Crack 클래스의 탐지 성능이 상대적으로 낮았다.
2. 야간, 우천, 저조도 환경에 대한 추가 검증이 부족하다.
3. 입력 이미지 크기별 성능 비교는 수행하지 못하였다.
4. 데이터 증강 적용 여부에 따른 정량적 비교는 수행하지 못하였다.
5. 실제 도로 CCTV 또는 주행 영상 기반 실시간 추론 실험은 수행하지 못하였다.

향후에는 다양한 도로 환경의 데이터를 추가하고, 이미지 크기별 비교 및 데이터 증강 기법을 적용하여 모델 성능을 개선할 수 있다. 또한 실제 영상 데이터에 대한 실시간 추론 실험을 수행하면 도로 모니터링 시스템으로의 적용 가능성을 더 구체적으로 검증할 수 있다.
