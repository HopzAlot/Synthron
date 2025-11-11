import os
import httpx
from api.agents.playwright_scraper import scrape_urls  
from dotenv import load_dotenv

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
SERPER_API_URL = "https://google.serper.dev/search"

TRUSTED_DOMAINS = [
    "amazon.com", "amazon.co.uk",
    "bestbuy.com",
    "newegg.com",
    "scan.co.uk",
    "microcenter.com",
    "ebuyer.com"
]

def is_trusted_url(url: str) -> bool:
    return any(domain in url for domain in TRUSTED_DOMAINS)

def is_product_in_stock(text: str) -> bool:
    text = text.lower()
    return not any(phrase in text for phrase in [
        "currently unavailable", "out of stock",
        "temporarily unavailable", "notify me", "sold out"
    ])

def extract_links(data: dict) -> list[str]:
    links = []
    for section in ("shopping", "organic"):
        links += [item["link"] for item in data.get(section, []) if "link" in item]
    return links

def get_best_in_stock(results: list[dict]) -> dict:
    in_stock = [r for r in results if is_product_in_stock(r.get("page_text", ""))]
    best = None
    for res in in_stock:
        if res.get("price") is not None:
            if best is None or res["price"] < best["price"]:
                best = res
    return best or (in_stock[0] if in_stock else None)

def find_product_urls(query: str) -> dict:
    if not SERPER_API_KEY:
        raise ValueError("❌ Missing SERPER_API_KEY in .env")

    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        with httpx.Client(timeout=10.0) as client:
            res = client.post(SERPER_API_URL, json={"q": query}, headers=headers)
            res.raise_for_status()
            data = res.json()

        # get all links from SERPER results
        all_links = extract_links(data)
        all_links = list(dict.fromkeys(all_links))[:10]  # remove duplicates, limit to top 10

        if not all_links:
            return {"url": None, "price": None}

        # scrape all links and keep only the ones with a valid price
        scraped_results = scrape_urls(all_links)
        valid_results = [r for r in scraped_results if r.get("price") is not None]

        if not valid_results:
            # fallback: return first scraped result even if price is None
            return scraped_results[0] if scraped_results else {"url": None, "price": None}

        # pick the one with lowest price
        best_result = min(valid_results, key=lambda x: x["price"])
        return best_result

    except Exception as e:
        print("❌ Error in find_product_urls:", str(e))
        return {"url": None, "price": None}