# Image-Based Category Detection with YOLOv8 and Product Rating Extraction

This project combines YOLOv8-based category detection for images with the ability to extract product ratings from two popular e-commerce platforms, **Trendyol** and **Hepsiburada**. It includes a Flask API to manage image uploads and product recommendations, along with Selenium-based scraping for product information and ratings.

## Features

- **YOLOv8 Integration**: Detect categories from uploaded images with high accuracy.
- **Flask API**: Manage image uploads and handle product recommendation requests.
- **Selenium Scraping**: Retrieve product details and ratings from Trendyol and Hepsiburada.
- **Dynamic Product Recommendations**: Match detected categories with relevant products.
- **Cross-Platform Support**: Extract ratings from Trendyol's `product-rating-score` or Hepsiburada's `JYHIcZ8Z_Gz7VXzxFB96` classes.

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

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up ChromeDriver**:
   Ensure ChromeDriver is installed and matches your Chrome browser version.

4. **Run the Application**:
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
