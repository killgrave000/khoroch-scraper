import os, time, threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from chaldal_selenium_scraper import scrape_chaldal_deals
from daraz_selenium_scraper import scrape_daraz_deals

app = Flask(__name__)
CORS(app)

# Prevent overlapping scrapes on low-RAM dyno
_inflight = threading.Semaphore(1)

# Simple in-memory cache: {(source,q): (ts, data)}
_CACHE = {}
_TTL = 300  # 5 minutes

@app.get("/")
def root():
    return {"ok": True, "service": "khoroch-deals-scraper", "endpoints": ["/api/deals"]}

@app.get("/api/deals")
def get_deals():
    q = request.args.get('q', 'rice').strip()
    source = request.args.get('region', 'daraz').lower().strip()
    key = (source, q)

    # Serve warm cache
    now = time.time()
    if key in _CACHE:
        ts, data = _CACHE[key]
        if now - ts < _TTL:
            return jsonify({"deals": data, "cached": True})

    # Only one scrape at a time
    if not _inflight.acquire(blocking=False):
        return jsonify({"error": "Busy, try again shortly"}), 429

    try:
        if source == 'chaldal':
            deals = scrape_chaldal_deals(q)
        elif source == 'daraz':
            deals = scrape_daraz_deals(q, 'bd')
        else:
            return jsonify({"error": "Unsupported source"}), 400

        # store in cache
        _CACHE[key] = (now, deals)
        return jsonify({"deals": deals, "cached": False})
    except Exception as e:
        return jsonify({"error": "Scraping failed", "details": str(e)}), 500
    finally:
        _inflight.release()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
