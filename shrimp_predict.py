from ultralytics import YOLO

# Load a pretrained YOLO26n model
model = YOLO("./best20260316_5.pt")

# Run inference on 'bus.jpg' with arguments
model.predict(r"image\20260308\*", save=True, imgsz=640, conf=0.3,iou=0.3,device=0,line_width=4)