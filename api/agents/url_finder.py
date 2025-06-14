from serpapi import GoogleSearch
import os

SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # Set this in your environment or .env file

def find_product_url_via_serpapi(product_name):
    if not SERPAPI_KEY:
        raise ValueError("SERPAPI_KEY is not set in environment variables.")

    search = GoogleSearch({
        "q": product_name,
        "api_key": SERPAPI_KEY,
        "num": 1
    })

    results = search.get_dict()
    for result in results.get("shopping_results", []) + results.get("organic_results", []):
        if result.get("link"):
            return result["link"]
    return None
