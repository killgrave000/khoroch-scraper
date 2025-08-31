import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

def make_chromium_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")
    opts.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=opts)
