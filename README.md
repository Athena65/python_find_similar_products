# Python Scripts for Image-Based Category Detection

This project processes images to detect categories using a YOLOv3 model and returns the best-matching category for further use in a product recommendation system.

---

## Features

- Uses **YOLOv3** for image-based category detection.
- Integrates with a Flask API for communication with the YOLOv3 model.
- Supports image uploads and JSON-based responses.
- Handles category matching for product recommendations.
- Logs detected categories and similar products for debugging.

---

## Prerequisites

Ensure the following are installed on your system:

- Python 3.8 or later
- PyTorch and required dependencies
- Flask
- OpenCV
- YOLOv3 weights and configuration files

---

## Setup Instructions

### 1. Clone This Repository
```bash
git clone https://github.com/your-repo/python_find_similar_products.git
cd python_find_similar_products
Add this to folder shown on image : https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x-oiv7.pt
![image](https://github.com/user-attachments/assets/5673cdee-2ccb-4b17-a4ee-47958a86b049)
