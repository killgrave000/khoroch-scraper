FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_BIN=/usr/bin/chromium

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg unzip wget \
    chromium fonts-liberation xvfb \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# app
COPY server.py utils_browser.py daraz_selenium_scraper.py chaldal_selenium_scraper.py ./

# (optional) healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:${PORT}/api/deals || exit 1

# SHELL FORM so $PORT expands (with local default 10000)
CMD ["sh","-c","exec gunicorn -w 2 -b 0.0.0.0:${PORT:-10000} server:app"]
