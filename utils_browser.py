import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def make_chromium_driver():
    opts = Options()
    # Memory-friendly flags
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--disable-extensions")
    opts.add_argument("--disable-background-networking")
    opts.add_argument("--disable-background-timer-throttling")
    opts.add_argument("--disable-breakpad")
    opts.add_argument("--disable-features=site-per-process,Translate,BackForwardCache,InterestFeedContentSuggestions,OptimizationHints")
    opts.add_argument("--no-default-browser-check")
    opts.add_argument("--no-first-run")
    opts.add_argument("--window-size=1200,800")
    # Optional: reduce image/JS cost. If this breaks selectors, remove.
    # opts.add_argument("--blink-settings=imagesEnabled=false")

    opts.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")

    # Selenium Manager (Selenium >= 4.6) will download matching driver automatically.
    return webdriver.Chrome(options=opts)
