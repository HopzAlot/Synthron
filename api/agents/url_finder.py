import os
import httpx
from api.agents.playwright_scraper import scrape_urls  # Sync version
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY") or "2f785bf2e3aee6866cce15ccff80cc7c8a63549a"

# List of allowed e-commerce domains
TRUSTED_DOMAINS = [
    "amazon.com", "amazon.co.uk",
    "bestbuy.com",
    "newegg.com",
    "scan.co.uk",
    "microcenter.com",
    "ebuyer.com"
]

def is_trusted_url(url):
    return any(domain in url for domain in TRUSTED_DOMAINS)

def is_product_in_stock(page_text: str) -> bool:
    """
    Heuristically checks whether product is likely in stock by avoiding common out-of-stock phrases.
    """
    page_text = page_text.lower()
    return not any(keyword in page_text for keyword in [
        "currently unavailable",
        "out of stock",
        "temporarily unavailable",
        "notify me",
        "sold out"
    ])

def find_product_urls(query):
    if not SERPER_API_KEY:
        raise ValueError("Missing SERPER_API_KEY in environment variables.")
    
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.post("https://google.serper.dev/search", json={"q": query}, headers=headers)
            response.raise_for_status()
            data = response.json()

        raw_urls = []
        if data.get("shopping"):
            raw_urls.extend([item.get("link") for item in data["shopping"] if item.get("link")])
        if data.get("organic"):
            raw_urls.extend([item.get("link") for item in data["organic"] if item.get("link")])

        # Filter trusted sources and deduplicate
        trusted_urls = [url for url in raw_urls if is_trusted_url(url)]
        trusted_urls = list(dict.fromkeys(trusted_urls))[:3]  # Max 3

        if not trusted_urls:
            return {"url": None, "price": None}

        # Scrape prices & HTML pages
        results = scrape_urls(trusted_urls)

        # Filter in-stock items
        in_stock_results = []
        for res in results:
            if res.get("page_text") and is_product_in_stock(res["page_text"]):
                in_stock_results.append(res)

        # Find cheapest in-stock result
        best = None
        for res in in_stock_results:
            if res["price"] is not None:
                if best is None or (res["price"] < best["price"]):
                    best = res

        if best is None:
            # Return the first in-stock URL at least
            return in_stock_results[0] if in_stock_results else {"url": trusted_urls[0], "price": None}

        return best

    except Exception as e:
        print("❌ Error in find_product_urls:", e)
        return {"url": None, "price": None}
