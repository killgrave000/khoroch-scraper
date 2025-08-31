import time
from selenium.webdriver.common.by import By
from utils_browser import make_chromium_driver

def scrape_chaldal_deals(query='rice'):
    d = make_chromium_driver()
    try:
        d.get(f"https://chaldal.com/search/{query}")
        time.sleep(5)
        results = []
        products = d.find_elements(By.CSS_SELECTOR, 'div.product')
        for p in products:
            try:
                title = p.find_element(By.CSS_SELECTOR, '.name').text
                price = p.find_element(By.CSS_SELECTOR, '.price').text
                image = p.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                link = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
                results.append({'title': title, 'price': price, 'image': image, 'link': link})
            except Exception:
                continue
        return results
    finally:
        d.quit()
