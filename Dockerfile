# ---- Python + Chromium (no apt chromedriver) for Selenium scraping ----
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps + Chromium (NO 'chromium-driver' to avoid version mismatch)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg unzip wget \
    chromium fonts-liberation xvfb && \
    rm -rf /var/lib/apt/lists/*

# Let Selenium know where Chromium is
ENV CHROME_BIN=/usr/bin/chromium
WORKDIR /app

# Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# App source
COPY server.py /app/server.py
COPY utils_browser.py /app/utils_browser.py
COPY daraz_selenium_scraper.py /app/daraz_selenium_scraper.py
COPY chaldal_selenium_scraper.py /app/chaldal_selenium_scraper.py

# Render provides PORT
ENV PORT=10000

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:${PORT}/api/deals || exit 1

# Use a production WSGI server
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:${PORT}", "server:app"]
