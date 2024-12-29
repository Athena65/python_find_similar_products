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
    "https://www.hepsiburada.com/"
]

def get_chrome_options():
    """
    Chrome için gerekli Selenium ayarlarını döndürür.
    """
    chrome_options = Options()
    arguments = [
        '--headless',
        '--disable-gpu',
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        'start-maximized',
        'enable-automation',
        '--disable-infobars',
        'window-size=1920,1080',
        '--disable-browser-side-navigation',
        '--disable-extensions',
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    ]
    for arg in arguments:
        chrome_options.add_argument(arg)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    return chrome_options


def get_search_urls(base_url, product_name):
    """
    Arama URL'sini belirler.
    """
    if "trendyol" in base_url:
        return f"{base_url.strip('/')}/sr?q={product_name.replace(' ', '%20')}"
    elif "hepsiburada" in base_url:
        return f"{base_url.strip('/')}/ara?q={product_name.replace(' ', '+')}"
    else:
        raise Exception("Desteklenmeyen bir URL")

def get_product_detailed_link(driver, base_url, search_url):
    """
    Ürün detay sayfasının linkini döndürür.
    """
    driver.get(search_url)
    try:
        # Cloudflare veya sayfa yükleme engellerini aşmak için bekle
        time.sleep(10)  # Sayfanın tamamen yüklenmesi için sabit bekleme

        # Trendyol veya Hepsiburada'ya göre uygun linki bul
        link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-card-wrppr a" if "trendyol" in base_url else "a.moria-ProductCard-gyqBb"))
        )

        if link_element:
            return link_element.get_attribute('href')
        else:
            raise Exception("Ürün linki bulunamadı.")
    except Exception as e:
        raise Exception(f"Ürün linki bulunamadı: {str(e)}")

def get_product_url(base_url, product_name):
    """Ürün adını arayıp ürün detay sayfasının URL'sini alır."""
    search_url = get_search_urls(base_url, product_name)
    chrome_options = get_chrome_options()
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    try:
        product_link = get_product_detailed_link(driver, base_url, search_url)
    finally:
        driver.quit()

    # Tam URL'yi döndür
    if product_link and not product_link.startswith("http"):
        return base_url.strip('/') + product_link
    elif product_link:
        return product_link
    else:
        raise Exception("Geçerli bir ürün linki bulunamadı.")


def get_product_detailed_page_html(product_url):
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

def extract_rating_from_html(html_content, base_url):
    """
    HTML içeriğinden "product-rating-score" sınıfındaki değeri çıkarır.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Rating değerini içeren elementi bul
    if "trendyol" in base_url:
        # Trendyol için "product-rating-score" sınıfındaki değeri al
        rating_element = soup.find('div', class_='product-rating-score')
        if rating_element:
            value_element = rating_element.find('div', class_='value')
            if value_element:
                return value_element.text.strip()
    elif "hepsiburada" in base_url:
        # Hepsiburada için "JYHIcZ8Z_Gz7VXzxFB96" sınıfındaki değeri al
        rating_element = soup.find('span', class_='JYHIcZ8Z_Gz7VXzxFB96')
        if rating_element:
            return rating_element.text.strip()

    return "Not Found"


def get_global_rating(product_name):
    """Ürünün global değerlendirme bilgilerini döndürür."""
    results = {}
    for base_url in BASE_URLS:
        try:
            # Ürün detay sayfasının URL'sini al
            product_url = get_product_url(base_url, product_name)

            # Ürün detay sayfasının HTML içeriğini al
            html_content = get_product_detailed_page_html(product_url)

            # HTML içeriğinden yıldız bilgisini çıkar
            rating = extract_rating_from_html(html_content, base_url)
            results[base_url] = {"rating": rating}
        except Exception as e:
            results[base_url] = {"error": str(e)}

    return results
