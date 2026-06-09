from ultralytics import YOLO

def main():
    model = YOLO("yolov8n.pt")

    model.train(
        data="data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        name="yolov8n_road"
    )

if __name__ == "__main__":
    main()