import re
import json
import redis
from playwright.sync_api import sync_playwright

# Local in-memory cache
_cache = {}

# Redis client (shared across processes, survives restarts)
try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    redis_client.ping()
    USE_REDIS= True
except Exception as e:
    print(f"Redis not available, falling back to local cache: {e}")
    redis_client= None
    USE_REDIS= False

# TTL in seconds (e.g., cache for 24 hours)
CACHE_TTL = 24 * 60 * 60


def extract_price_from_text(texts):
    for text in texts:
        text = text.strip().replace("\n", ".")
        if any(s in text for s in ["₹", "$", "€", "£"]) and any(c.isdigit() for c in text):
            return text
    return None


def extract_price_and_url(page):
    selectors = [
        '.a-price .a-offscreen', '.priceblock_ourprice', '.price .amount',
        '[class*="price"]', '[id*="price"]', '[class*="Price"]', '[id*="Price"]',
        '[class*="our-price"]', '[class*="offer-price"]', '[class*="a-price"]',
        '[class*="a-offscreen"]'
    ]
    for selector in selectors:
        try:
            elements = page.locator(selector).all_text_contents()
            price_text = extract_price_from_text(elements)
            if price_text:
                return price_text
        except:
            continue
    return None


def parse_price(price_str):
    if not price_str:
        return None
    price_str = price_str.replace("\n", ".")
    currency_match = re.search(r'[\$€₹£]\s?[\d\.,]+', price_str)
    if currency_match:
        raw = currency_match.group(0)
    else:
        match = re.search(r'[\d\.,]+', price_str)
        if not match:
            return None
        raw = match.group(0)

    cleaned = re.sub(r"[^\d.,]", "", raw)
    if re.match(r"^\d{1,3}(,\d{3})*(\.\d+)?$", cleaned):
        cleaned = cleaned.replace(",", "")
    elif re.match(r"^\d{1,3}(\.\d{3})*(,\d+)?$", cleaned):
        cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "," in cleaned and "." not in cleaned:
        cleaned = cleaned.replace(",", ".")

    try:
        return round(float(cleaned), 2)
    except:
        return None


def fetch_price_and_url(url):
    # 1. Check in-memory cache
    if url in _cache:
        print(f"🔒 Local cache hit for {url}")
        return _cache[url]

    # 2. Check Redis cache
    if USE_REDIS:
         redis_data = redis_client.get(url)
         if redis_data:
            result = json.loads(redis_data)
            _cache[url] = result  # warm local cache
            print(f"📦 Redis cache hit for {url}")
            return result

    # 3. Scrape if not found in either cache
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.route("**/*.{png,jpg,jpeg,css,js,woff2,woff,svg,eot}", lambda route: route.abort())
            page.goto(url, timeout=10000, wait_until="domcontentloaded")
            page.wait_for_selector('[class*="price"], [id*="price"]', timeout=10000)
            raw_price = extract_price_and_url(page)
            parsed_price = parse_price(raw_price)
            result = {"url": url, "price": parsed_price}

            # Store in both caches
            _cache[url] = result
            if USE_REDIS:
                try:
                    redis_client.setex(url, CACHE_TTL, json.dumps(result))
                except Exception as e:
                    print(f"Failed to save to Redis, continuing with local cache: {e}")

            print(f"🔍 Scraped from {url} → parsed: {parsed_price}")
            return result

        except Exception as e:
            print(f"❌ Failed to fetch {url}: {e}")
            return {"url": url, "price": None}

        finally:
            page.close()
            browser.close()


def scrape_urls(urls):
    results = []
    for url in urls:
        results.append(fetch_price_and_url(url))
    return results