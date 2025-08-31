import time
from selenium.webdriver.common.by import By
from utils_browser import make_chromium_driver

def get_daraz_domain(region):
    return {
        'bd': 'daraz.com.bd', 'pk': 'daraz.pk', 'lk': 'daraz.lk',
        'mm': 'daraz.com.mm', 'np': 'daraz.com.np'
    }.get(region, 'daraz.com.bd')

def scrape_daraz_deals(query='discount', region='bd'):
    domain = get_daraz_domain(region)
    url = f"https://{domain}/catalog/?q={query}"
    d = make_chromium_driver()
    try:
        d.get(url)
        time.sleep(3)
        deals = []
        cards = d.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')
        for c in cards:
            try:
                img = c.find_element(By.TAG_NAME, 'img')
                title = img.get_attribute('alt')
                price_el = c.find_element(By.CSS_SELECTOR, '.price--NVB62, .ooOxS')
                price = price_el.text.strip() if price_el else ''
                image = img.get_attribute('src')
                a = c.find_element(By.TAG_NAME, 'a')
                link = a.get_attribute('href')
                if link and not link.startswith('http'):
                    link = f"https:{link}"
                if title and price and image and link:
                    deals.append({'title': title, 'price': price, 'image': image, 'link': link})
            except Exception:
                continue
        return deals
    finally:
        d.quit()
