from selenium.webdriver.common.by import By
from utils_browser import make_chromium_driver
import time

def scrape_chaldal_deals(query='rice'):
    driver = make_chromium_driver()
    try:
        search_url = f"https://chaldal.com/search/{query}"
        driver.get(search_url)
        time.sleep(5)  # simple wait for client-side rendering

        results = []
        products = driver.find_elements(By.CSS_SELECTOR, 'div.product')
        for p in products:
            try:
                title = p.find_element(By.CSS_SELECTOR, '.name').text
                price = p.find_element(By.CSS_SELECTOR, '.price').text
                image = p.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                link = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
                results.append({
                    'title': title,
                    'price': price,
                    'image': image,
                    'link': link,
                })
            except Exception:
                continue

        return results
    finally:
        driver.quit()
