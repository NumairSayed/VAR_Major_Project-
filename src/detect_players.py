import cv2
import numpy as np
import torch
from ultralytics import YOLO

# Load the pre-trained YOLO model
model = YOLO("yolov8n.pt")  # Will use the model from root or we can change it to "models/yolov8.pt"

def detect_players(frame):
    """Detects players in the frame using YOLO."""
    results = model(frame)
    players = []
    
    for result in results:
        for box in result.boxes:
            if box.cls == 0:  # Filter only people (class 0 from COCO)
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                players.append((x1, y1, x2, y2))
    
    return players