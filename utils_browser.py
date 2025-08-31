import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_chromium_driver():
    opts = Options()
    # Container/Render friendly flags
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    # Point Selenium to the Chromium in the container
    opts.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

    # Selenium Manager (built into Selenium 4.6+) will auto-download the right driver.
    # No Service() and no webdriver-manager needed.
    return webdriver.Chrome(options=opts)
