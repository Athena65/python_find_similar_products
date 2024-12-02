import sys
sys.path.append('C:/bitirmetezi-ratesfromeverywhere/python_scripts/yolov3')  # Yol ekleme
import json
from flask import Flask, request, jsonify
import cv2
import numpy as np
import torch
from yolov3.models.experimental import attempt_load
from yolov3.utils.general import non_max_suppression, scale_boxes
from yolov3.utils.torch_utils import select_device

app = Flask(__name__)

# YOLOv3 model yükleme
device = select_device('')
weights_path = 'yolov3/weights/yolov3.pt'
model = attempt_load(weights_path, device=device)
model.eval()

@app.route('/process-image', methods=['POST'])
def process_image():
    import json

    # Tüm alt kategorileri alın
    all_subcategories = json.loads(request.form.get('all_subcategories', '[]'))

    # Resmi al ve işle
    if 'image' not in request.files:
        return jsonify({'categories': []}), 200

    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Görüntü ön işleme
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (640, 640))
    img = torch.from_numpy(img).float()
    img = img.permute(2, 0, 1) / 255.0
    img = img.unsqueeze(0)

    # YOLO ile tahmin yap
    with torch.no_grad():
        results = model(img)

    # Tahmin sonuçlarını işleme
    if isinstance(results, tuple):
        predictions = results[0]
    else:
        predictions = results

    # Non-Max Suppression (NMS)
    predictions = non_max_suppression(predictions, conf_thres=0.4, iou_thres=0.5)

    # Kategorileri işle
    detected_categories = []
    for det in predictions:
        if det is not None and len(det):
            for *xyxy, conf, cls in det:
                category_id = int(cls)
                confidence = float(conf)
                if category_id < len(all_subcategories):
                    detected_categories.append((all_subcategories[category_id], confidence))

    # En yüksek güven skoru olan kategoriyi seç
    detected_categories = sorted(detected_categories, key=lambda x: x[1], reverse=True)
    best_category = detected_categories[0][0] if detected_categories else None

    # Kategori bulunamazsa boş liste döndür
    if not best_category:
        return jsonify({'categories': []}), 200

    return jsonify({'categories': [best_category]})






if __name__ == '__main__':
    app.run(debug=True, port=5000)
