import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2
import pytesseract

def get_product_url(base_url, product_name):
    """Ürün adını arayıp ürün detay sayfasının URL'sini alır."""
    search_url = f"{base_url}/search?q={product_name.replace(' ', '+')}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Ürün detay sayfasının linkini bul
    product_link = soup.find('a', {'class': 'product-link'})['href']
    return base_url + product_link

def capture_screenshot(product_url, output_file='product_screenshot.png'):
    """Ürün detay sayfasının ekran görüntüsünü kaydeder."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Görüntüsüz mod
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    # Sayfayı aç ve ekran görüntüsü al
    driver.get(product_url)
    driver.save_screenshot(output_file)
    driver.quit()
    return output_file

def extract_rating_from_image(image_path):
    """Görüntüden yıldız ve yorum bilgilerini ayıklar."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Tesseract ile OCR işlemi
    text = pytesseract.image_to_string(gray, lang='eng')

    # Değerlendirme bilgilerini bul
    rating, reviews = None, None
    for line in text.split('\n'):
        if "stars" in line.lower():  # Yıldız bilgisi
            rating = line.split()[0]
        if "reviews" in line.lower() or "yorum" in line.lower():  # Yorum sayısı
            reviews = line.split()[0]

    return rating, reviews

def get_global_rating(product_name):
    """Ürünün global değerlendirme bilgilerini döndürür."""
    base_url = "https://example.com"  # Hedef site URL'si
    try:
        # Ürün detay sayfasının URL'sini al
        product_url = get_product_url(base_url, product_name)

        # Ürün detay sayfasının ekran görüntüsünü al
        screenshot_path = capture_screenshot(product_url)

        # Görüntüden yıldız ve yorum bilgilerini çıkar
        rating, reviews = extract_rating_from_image(screenshot_path)
        return {"rating": rating, "reviews": reviews}
    except Exception as e:
        return {"error": str(e)}
