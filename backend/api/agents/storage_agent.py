from api.agents.llama import generate_llama_response 
from api.agents.url_finder import find_product_urls   
import json

class STORAGEAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}

    def recommend(self):
        
        name_prompt = f"""
You're a PC building expert.

Suggest the best storage device within this budget and use-case for the region. Respond ONLY with the storage device name and model. No explanation, no JSON, no extra text.

Budget: {self.budget}
Region: {self.region}
Preferences: {self.preferences}
Use case: {self.use_case}
"""
        raw_name = generate_llama_response(name_prompt)
        storage_name = raw_name.strip().strip('"')

        
        product_data = find_product_urls(f"{storage_name} buy online in {self.region}")
        url = product_data.get("url") or "https://example.com"
        price = product_data.get("price")
        vendor=product_data.get('vendor') or 'not provided'
        performance=product_data.get('performance')
        name=product_data.get('name')
        
        details_prompt = f"""
You are a PC building expert.

Here is a storage device: "{storage_name}"

The product was found at: {url}
The actual price listed there is: {price if price else "unknown"}

Return a valid minified JSON with realistic specs and price, using the given details.

Format:
{{
    "name": "{name}" or "not provided",
    "price": {price if price else "null"},
    "performance": '{performance}' or "not provided",
    "vendor": "{vendor}" or "not provided",
    "url": "{url}" or "not provided"
}}

Only return JSON. No explanation.
"""
        final_response = generate_llama_response(details_prompt)

        try:
            parsed = json.loads(final_response)
        except Exception as e:
            print("❌ Failed to parse final LLaMA JSON:", e)
            parsed = {
                "name": storage_name,
                "price": price,
                "vendor": None,
                "url": url
            }

        print("💾 Final STORAGE recommendation with scraped price:", parsed)
        return json.dumps(parsed)