from flask import Flask, request, jsonify
import cv2
import numpy as np
import torch
from torchvision import transforms

app = Flask(__name__)

# YOLO v3 model yükleme
model = torch.hub.load('ultralytics/yolov5', 'yolov3', pretrained=True)

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Resmi al ve işle
    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    results = model(img)

    # Tespit edilen kategorileri al
    categories = results.pandas().xyxy[0]['name'].unique().tolist()
    return jsonify({'categories': categories})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
