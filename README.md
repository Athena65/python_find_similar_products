# Image-Based Category Detection with YOLOv3

This project uses YOLOv3 to detect categories from images and integrates these detections into a product recommendation system via a Flask API.

## Features

- **YOLOv3 Integration**: Utilizes YOLOv3 for accurate image-based category detection.
- **Flask API**: Communicates with the YOLOv3 model for seamless integration.
- **Image Upload Support**: Accepts image uploads for processing.
- **Category Matching**: Matches detected categories for product recommendation.
- **Logging**: Provides detailed logs for debugging detected categories and similar products.

## Prerequisites

Before starting, ensure your system meets the following requirements:

- Python 3.8 or later
- PyTorch and its dependencies
- Flask
- OpenCV
- YOLOv3 weights and configuration files

## Setup Instructions

### Step 1: Clone the Repository

Run the following command to clone this repository:

```bash
git clone https://github.com/your-repo/python_find_similar_products.git
cd python_find_similar_products
```

### Step 2: Download YOLOv3 Weights

Download the required YOLOv3 weights from the [Ultralytics repository](https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x-oiv7.pt) and save them to the `weights/` directory:

```bash
mkdir -p weights
wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x-oiv7.pt -O weights/yolov8x-oiv7.pt
```

### Step 3: Install Dependencies

Install all required Python libraries:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

Start the Flask server:

```bash
python app.py
```

The server will start on `http://127.0.0.1:5000/`.

## Usage

1. Upload an image using the Flask API.
2. The YOLOv3 model processes the image and returns the detected categories.
3. The system matches the categories with available products for recommendations.

## Folder Structure

```plaintext
python_find_similar_products/
├── app.py                 # Flask application
├── detect.py              # YOLOv3 image detection script
├── requirements.txt       # Python dependencies
├── weights/               # YOLOv3 weight files
│   └── yolov8x-oiv7.pt    # Downloaded weight file
├── static/                # Static assets (optional)
└── README.md              # Project documentation
```
