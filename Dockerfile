# ---- Python + Chromium + Chromedriver image for Selenium scraping ----
FROM python:3.11-slim

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system deps, Chromium and Chromedriver
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates gnupg unzip wget \
    chromium chromium-driver fonts-liberation \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Make sure chromedriver is on PATH and chromium alias exists
ENV CHROME_BIN=/usr/bin/chromium \
    CHROMEDRIVER=/usr/bin/chromedriver \
    PATH="/usr/local/bin:${PATH}"

# Workdir
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy app source
COPY server.py /app/server.py
COPY daraz_selenium_scraper.py /app/daraz_selenium_scraper.py
COPY chaldal_selenium_scraper.py /app/chaldal_selenium_scraper.py

# Render provides PORT env; default to 3000 locally
ENV PORT=3000

# Healthcheck (optional)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD curl --fail http://localhost:${PORT}/api/deals || exit 1

# Start the app
CMD ["python", "-u", "server.py"]