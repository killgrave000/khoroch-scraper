from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def _make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    # faster loads; don’t wait for images/ads
    opts.page_load_strategy = "eager"
    return webdriver.Chrome(options=opts)

def _ensure_area_selected(driver, area="Dhanmondi"):
    """Open the area picker (if shown), type area, pick first suggestion."""
    # Common openers for the area modal
    openers = [
        (By.XPATH, '//button[contains(., "Deliver to") or contains(., "Change") or contains(., "Select your area")]'),
        (By.CSS_SELECTOR, 'button[aria-label*="Deliver"], [data-testid*="deliver"]'),
    ]
    opened = False
    for by, sel in openers:
        try:
            btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((by, sel)))
            btn.click()
            opened = True
            break
        except Exception:
            continue
    if not opened:
        return  # already set or UI variant without a gate

    # Try a few likely inputs
    inputs = [
        'input[placeholder*="area"]',
        'input[placeholder*="location"]',
        'input[type="text"]'
    ]
    for css in inputs:
        try:
            inp = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))
            inp.clear()
            inp.send_keys(area)
            time.sleep(0.5)
            inp.send_keys(Keys.DOWN)
            inp.send_keys(Keys.RETURN)
            break
        except Exception:
            continue

    # Confirm if a confirm/save button appears
    confirms = [
        (By.XPATH, '//button[contains(., "Save") or contains(., "Deliver here") or contains(., "Confirm")]'),
        (By.CSS_SELECTOR, 'button[type="submit"]'),
    ]
    for by, sel in confirms:
        try:
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((by, sel))).click()
            break
        except Exception:
            continue

def scrape_chaldal_deals(query='rice', area='Dhanmondi'):
    driver = _make_driver()
    try:
        search_url = f"https://chaldal.com/search/{query}"
        driver.get(search_url)

        # handle the delivery-area gate quickly (if present)
        try:
            _ensure_area_selected(driver, area=area)
        except Exception:
            pass

        # wait briefly for products to appear
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.product'))
            )
        except TimeoutException:
            return []

        results = []
        products = driver.find_elements(By.CSS_SELECTOR, 'div.product')[:40]  # cap for memory

        for p in products:
            try:
                title = p.find_element(By.CSS_SELECTOR, '.name').text
                price = p.find_element(By.CSS_SELECTOR, '.price').text
                image = p.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                link = p.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if title and price and link:
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
