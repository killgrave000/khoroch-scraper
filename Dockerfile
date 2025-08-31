FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    CHROME_BIN=/usr/bin/chromium

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg unzip wget \
    chromium fonts-liberation \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY server.py utils_browser.py daraz_selenium_scraper.py chaldal_selenium_scraper.py ./

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:${PORT}/api/deals || exit 1

# single worker/threads by default; shell form so $PORT expands
ENV WEB_CONCURRENCY=1 GUNICORN_THREADS=1 GUNICORN_TIMEOUT=180
CMD ["sh","-c","exec gunicorn -w ${WEB_CONCURRENCY:-1} --threads ${GUNICORN_THREADS:-1} -b 0.0.0.0:${PORT:-10000} --timeout ${GUNICORN_TIMEOUT:-180} server:app"]
