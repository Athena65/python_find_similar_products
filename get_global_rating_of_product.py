import cv2,pytesseract, time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# URLS to fetch datas
BASE_URLS = [
    "https://www.trendyol.com/",
    #"https://www.n11.com/"
]

def get_chrome_options():
    """
    Chrome için gerekli Selenium ayarlarını döndürür.
    """
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Arka planda çalıştır
    chrome_options.add_argument('--disable-gpu')  # GPU'yu devre dışı bırak
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')  # Bellek sorunları için
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Gerçekçi bir User-Agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    return chrome_options

def get_product_url(base_url, product_name):
    """Ürün adını arayıp ürün detay sayfasının URL'sini alır."""

    # Arama URL'si
    if "trendyol" in base_url:
        """Trendyol'da ürün adını arayıp arama sonucu ilk ürünün detay sayfasının URL'sini alır."""
        search_url = f"{base_url.strip('/')}/sr?q={product_name.replace(' ', '%20')}"
        product_class = 'p-card-wrppr'
    #elif "n11" in base_url:
    #     search_url = f"{base_url}arama?q={product_name.replace(' ', '+')}"
    #     product_class = 'pro'
    else:
        raise Exception("Desteklenmeyen bir URL")

    # Selenium ayarları
    chrome_options = get_chrome_options()

    driver = webdriver.Chrome(chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.get(search_url)

    try:
        # Cloudflare için bekleme
        time.sleep(10)  # Sayfanın tamamen yüklenmesi için sabit bekleme

        # Öğeyi bekle
        link_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-card-wrppr a"))
        )
        product_link = link_element.get_attribute('href')
    except Exception as e:
        raise Exception(f"Ürün linki bulunamadı: {str(e)}")
    finally:
        driver.quit()

    # Tam URL'yi döndür
    if product_link and not product_link.startswith("http"):
        return base_url.strip('/') + product_link
    elif product_link:
        return product_link
    else:
        raise Exception("Geçerli bir ürün linki bulunamadı.")

def get_product_html(product_url):
    """
    Ürün detay sayfasının HTML içeriğini döndürür.
    """
    chrome_options = get_chrome_options()

    driver = webdriver.Chrome(chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    driver.get(product_url)
    try:
        # Sayfanın kaynak kodunu al
        html_content = driver.page_source
    finally:
        driver.quit()

    return html_content

def extract_rating_from_html(html_content):
    """
    HTML içeriğinden "product-rating-score" sınıfındaki değeri çıkarır.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Rating değerini içeren elementi bul
    rating_element = soup.find('div', class_='product-rating-score')
    if rating_element:
        value_element = rating_element.find('div', class_='value')
        if value_element:
            return value_element.text.strip()

    return "Not Found"


def get_global_rating(product_name):
    """Ürünün global değerlendirme bilgilerini döndürür."""
    results = {}
    for base_url in BASE_URLS:
        try:
            # Ürün detay sayfasının URL'sini al
            product_url = get_product_url(base_url, product_name)

            # Ürün detay sayfasının HTML içeriğini al
            html_content = get_product_html(product_url)

            # HTML içeriğinden yıldız bilgisini çıkar
            rating = extract_rating_from_html(html_content)
            results[base_url] = {"rating": rating}
        except Exception as e:
            results[base_url] = {"error": str(e)}

    return results

# resmi on işle
def preprocess_image(image_path):
    """Görseli OCR için işler."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Kenarları daha belirgin hale getirmek için eşikleme
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh
