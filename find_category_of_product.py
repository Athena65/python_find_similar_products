import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLOv8 model
MODEL_PATH = 'weights/yolov8x-oiv7.pt'  # Yolov8 trained dataset
model = YOLO(MODEL_PATH)

def process_image(file):
    """
    Process the image and return the best category detected.
    """
    # Decode the image
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to decode the image.")

    # Preprocess the image for YOLOv8
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform YOLOv8 inference
    results = model.predict(img, conf=0.25, iou=0.45) # 0.25 trust , 0.45 Intersection over union

    # Process YOLOv8 predictions
    detected_category_ids = []  # category id to return
    detected_categories = []  # category names for logging

    for result in results:
        for box in result.boxes:
            category_id = int(box.cls[0])  # Class ID
            confidence = float(box.conf[0])  # Confidence score

            # Map category_id to OpenImagesV7 dataset category name
            if category_id in result.names:  # Check if category_id, category_name exists in dataset
                detected_category_ids.append((category_id, confidence))
                detected_categories.append((result.names[category_id], confidence))

    # Select the category with the highest confidence
    detected_category_ids = sorted(detected_category_ids, key=lambda x: x[1], reverse=True)
    best_category_ids = detected_category_ids[0][0] if detected_category_ids else None

    detected_categories = sorted(detected_categories, key=lambda x: x[1], reverse=True)
    best_category = detected_categories[0][0] if detected_categories else None

    return best_category_ids, best_category, results
