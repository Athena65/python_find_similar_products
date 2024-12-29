# Image-Based Category Detection with YOLOv8 and Product Rating Extraction

This project combines YOLOv8-based category detection for images with the ability to extract product ratings from multiple e-commerce platforms. It includes a Flask API to manage image uploads and product recommendations, along with Selenium-based scraping for product information and ratings.

## Features

- **YOLOv8 Integration**: Detect categories from uploaded images with high accuracy.
- **Flask API**: Manage image uploads and handle product recommendation requests.
- **Selenium Scraping**: Retrieve product details and ratings from multiple e-commerce platforms.
- **Dynamic Product Recommendations**: Match detected categories with relevant products.
- **Cross-Platform Support**: Extract ratings from various e-commerce platforms to calculate an overall rating.

## Prerequisites

Ensure the following dependencies are installed:

- Python 3.8 or later
- Flask
- Selenium with ChromeDriver
- PyTorch and OpenCV (for YOLOv8)
- BeautifulSoup for HTML parsing

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/python_find_similar_products.git
   cd python_find_similar_products
   ```

2. **Download YOLOv8 Weights**:  
   Download the YOLOv8 model weights from the [Ultralytics Open Images V7 Documentation](https://docs.ultralytics.com/datasets/detect/open-images-v7/#usage) and save them in the `weights/` directory:  
   ```bash
   mkdir -p weights
   wget https://github.com/ultralytics/assets/releases/download/v8.2.0/yolov8x-oiv7.pt -O weights/yolov8x-oiv7.pt
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up ChromeDriver**:
   Ensure ChromeDriver is installed and matches your Chrome browser version.

5. **Run the Application**:
   ```bash
   python app.py
   ```

## Usage

1. Upload an image through the Flask API.
2. YOLOv8 processes the image to detect categories.
3. Use the `get_product_url` function to fetch the first product URL from Trendyol or Hepsiburada using a product name.
4. Use Selenium to scrape the product's rating from the detail page.

## Folder Structure

```plaintext
python_find_similar_products/
├── app.py                        # Flask application
├── find_category_of_product.py   # Category detection script
├── get_global_rating_of_product.py # Rating extraction script
├── requirements.txt              # Python dependencies
├── weights/                      # Model weights directory
│   └── yolov8x-oiv7.pt           # YOLOv8 model weights
├── .gitignore                    # Git ignore file
└── README.md                     # Project documentation
```
## Related Project

This project works in conjunction with the [RatesFromEverywhere2](https://github.com/Athena65/ratesfromeverywhere2) repository. While this project focuses on **image-based category detection**, the related repository specializes in scraping product ratings from multiple e-commerce platforms.

### How It Works:

1. **Image-Based Category Detection**:  
   Users can upload images of products to this project. The system processes the images using YOLOv8 to detect relevant categories, which are then used for product recommendations.

2. **Product Rating Integration**:  
   The project communicates with the **RatesFromEverywhere2** repository to retrieve product ratings from two different e-commerce platforms. The ratings from these platforms are averaged to provide a general rating value for the detected categories.

This combined functionality ensures accurate category detection and integrates user-friendly rating insights into the recommendation process.

You can explore more about the **RatesFromEverywhere2** repository [here](https://github.com/Athena65/ratesfromeverywhere2).
