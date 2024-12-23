import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import cv2
import pytesseract

# URLS to fetch datas
BASE_URLS = [
    "https://www.hepsiburada.com/",
    "https://www.trendyol.com/",
    "https://www.n11.com/"
]


def get_product_url(base_url, product_name):
    """Ürün adını arayıp ürün detay sayfasının URL'sini alır."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    """Ürün adını arayıp ürün detay sayfasının URL'sini alır."""
    if "hepsiburada" in base_url:
        search_url = f"{base_url}ara?q={product_name.replace(' ', '+')}"
    elif "trendyol" in base_url:
        search_url = f"{base_url}sr?q={product_name.replace(' ', '+')}"
    elif "n11" in base_url:
        search_url = f"{base_url}arama?q={product_name.replace(' ', '+')}"
    else:
        raise Exception("Desteklenmeyen bir URL")

    response = requests.get(search_url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_link = None
    if "hepsiburada" in base_url:
        product_link = soup.find('a', {'class': 'product-card-wrapper'})['href']
    elif "trendyol" in base_url:
        product_link = soup.find('a', {'class': 'p-card-wrppr'})['href']
    elif "n11" in base_url:
        product_link = soup.find('a', {'class': 'pro'})['href']

    if not product_link:
        raise Exception(f"Ürün linki bulunamadı: {base_url}")

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
    results = {}
    for base_url in BASE_URLS:
        try:
            # Ürün detay sayfasının URL'sini al
            product_url = get_product_url(base_url, product_name)

            # Ürün detay sayfasının ekran görüntüsünü al
            screenshot_path = capture_screenshot(product_url)

            # Görüntüden yıldız ve yorum bilgilerini çıkar
            rating, reviews = extract_rating_from_image(screenshot_path)
            results[base_url] = {"rating": rating, "reviews": reviews}
        except Exception as e:
            results[base_url] = {"error": str(e)}

    return results