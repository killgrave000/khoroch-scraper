from selenium.webdriver.common.by import By
from utils_browser import make_chromium_driver
import time

def get_daraz_domain(region):
    domains = {
        'bd': 'daraz.com.bd',
        'pk': 'daraz.pk',
        'lk': 'daraz.lk',
        'mm': 'daraz.com.mm',
        'np': 'daraz.com.np',
    }
    return domains.get(region, 'daraz.com.bd')

def scrape_daraz_deals(query='discount', region='bd'):
    domain = get_daraz_domain(region)
    url = f"https://{domain}/catalog/?q={query}"
    driver = make_chromium_driver()

    try:
        driver.get(url)
        time.sleep(3)  # crude wait; replace with WebDriverWait if needed

        deals = []
        cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')
        for card in cards:
            try:
                img = card.find_element(By.TAG_NAME, 'img')
                title = img.get_attribute('alt')
                price_elem = card.find_element(By.CSS_SELECTOR, '.price--NVB62, .ooOxS')
                price = price_elem.text.strip() if price_elem else ''
                image = img.get_attribute('src')
                anchor = card.find_element(By.TAG_NAME, 'a')
                link = anchor.get_attribute('href')
                if link and not link.startswith('http'):
                    link = f"https:{link}"

                if title and price and image and link:
                    deals.append({
                        'title': title,
                        'price': price,
                        'image': image,
                        'link': link
                    })
            except Exception:
                continue

        return deals
    finally:
        driver.quit()
