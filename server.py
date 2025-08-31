import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from chaldal_selenium_scraper import scrape_chaldal_deals
from daraz_selenium_scraper import scrape_daraz_deals

app = Flask(__name__)
CORS(app)

@app.get("/")
def root():
    return {
        "ok": True,
        "service": "khoroch-deals-scraper",
        "endpoints": ["/api/deals"]
    }

@app.get("/api/deals")
def get_deals():
    query = request.args.get('q', 'rice')
    # choose source by name: 'daraz' or 'chaldal'
    source = request.args.get('region', 'daraz').lower()

    try:
        if source == 'chaldal':
            deals = scrape_chaldal_deals(query)
        elif source == 'daraz':
            # country code stays 'bd' unless you want to pass it from client
            deals = scrape_daraz_deals(query, 'bd')
        else:
            return jsonify({'error': 'Unsupported source'}), 400

        return jsonify({'deals': deals})
    except Exception as e:
        return jsonify({'error': 'Scraping failed', 'details': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
