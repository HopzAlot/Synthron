from api.agents.llama import generate_llama_response  # sync version
from api.agents.url_finder import find_product_urls    # sync version
import json

class RAMAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}

    def recommend(self):
        # Step 1: Ask LLaMA for RAM name
        name_prompt = f"""
You're a PC building expert.

Suggest the best RAM module within this budget and use-case for the region. Respond ONLY with the RAM name and model. No explanation, no JSON, no extra text.

Budget: {self.budget}
Region: {self.region}
Preferences: {self.preferences}
Use case: {self.use_case}
"""
        raw_name = generate_llama_response(name_prompt)
        ram_name = raw_name.strip().strip('"')

        # Step 2: Find product info via scraping
        product_data = find_product_urls(f"{ram_name} buy online in {self.region}")
        url = product_data.get("url") or "https://example.com"
        price = product_data.get("price")

        # Step 3: Ask LLM to generate specs JSON
        details_prompt = f"""
You are a PC building expert.

Here is a RAM module: "{ram_name}"

The product was found at: {url}
The actual price listed there is: {price if price is not None else "null"}



Return a valid minified JSON with realistic specs, using the given price and URL.

Format:
{{
    "name": "{ram_name}",
    "ram_type": "...",
    "price": {price if price else "null"},
    "performance": ...,
    "vendor": "...",
    "url": "{url}"
}}

Only return JSON. No explanation.
"""
        final_response = generate_llama_response(details_prompt)

        try:
            parsed = json.loads(final_response)
        except Exception as e:
            print("❌ Failed to parse final LLaMA JSON:", e)
            parsed = {
                "name": ram_name,
                "ram_type": None,
                "price": price,
                "performance": None,
                "vendor": None,
                "url": url
            }

        print("🧠 Final RAM recommendation with scraped price:", parsed)
        return json.dumps(parsed)
