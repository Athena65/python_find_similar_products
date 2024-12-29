```markdown
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
├── app.py                 # Flask application
├── detect.py              # YOLOv8 image detection script
├── product_rating.py      # Functions for scraping product details and ratings
├── requirements.txt       # Python dependencies
├── weights/               # YOLOv8 weight files
├── static/                # Static assets
└── README.md              # Project documentation
```

## Example: Extracting Product Rating

The following steps illustrate how the project fetches product ratings:

1. Call `get_product_url` with the base URL and product name:
   ```python
   base_url = "https://www.hepsiburada.com/"
   product_name = "Apple iPhone 13"
   product_url = get_product_url(base_url, product_name)
   ```

2. Use Selenium to load the product page and extract the HTML:
   ```python
   chrome_options = get_chrome_options()
   driver = webdriver.Chrome(options=chrome_options)
   driver.get(product_url)
   time.sleep(5)
   html_content = driver.page_source
   driver.quit()
   ```

3. Pass the HTML content to `extract_rating_from_html`:
   ```python
   rating = extract_rating_from_html(html_content, base_url)
   print("Rating:", rating)
   ```

The system dynamically selects the appropriate scraping method for Trendyol or Hepsiburada, ensuring flexible and accurate rating retrieval.
```
