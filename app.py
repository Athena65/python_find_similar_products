from flask import Flask, request, jsonify
import cv2
import numpy as np
from ultralytics import YOLO

app = Flask(__name__)

# Load YOLOv8 model
MODEL_PATH = 'weights/yolov8x-oiv7.pt'  # Replace with your desired YOLOv8 weights file
model = YOLO(MODEL_PATH)

@app.route('/process-image', methods=['POST'])
def process_image():
    import json

    # Retrieve all subcategories from the request
    all_subcategories = json.loads(request.form.get('all_subcategories', '[]'))

    # Validate that an image is provided in the request
    if 'image' not in request.files:
        app.logger.error('No image provided in the request.')
        return jsonify({'categories': []}), 200

    # Read and decode the image
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        app.logger.error('Failed to decode the image.')
        return jsonify({'categories': []}), 200

    # Preprocess the image for YOLOv8
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Perform YOLOv8 inference
    try:
        results = model.predict(img, conf=0.2, iou=0.1)
    except Exception as e:
        app.logger.error(f'Error during YOLOv8 inference: {e}')
        return jsonify({'categories': []}), 200

    # Log the raw YOLOv8 output
    app.logger.info(f'YOLOv8 Results: {results}')  # Logs the results object

    # Process YOLOv8 predictions
    detected_categories = []
    for result in results:
        for box in result.boxes:
            category_id = int(box.cls[0])  # Class ID
            confidence = float(box.conf[0])  # Confidence score
            app.logger.info(f"Detected: {box.cls[0]}, Confidence: {box.conf[0]}")

            # Map category_id to COCO category name
            if category_id in result.names:  # Check if category_id exists in names mapping
                detected_categories.append((result.names[category_id], confidence))

    # Select the category with the highest confidence
    detected_categories = sorted(detected_categories, key=lambda x: x[1], reverse=True)
    best_category = detected_categories[0][0] if detected_categories else None

    # Return the result
    if not best_category:
        app.logger.info('No matching category found.')
        return jsonify({'categories': [], 'yolo_output': str(results)}), 200

    app.logger.info(f'Best category detected: {best_category}')
    return jsonify({'categories': [best_category], 'yolo_output': str(results)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
