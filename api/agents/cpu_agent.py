from api.agents.llama import generate_llama_response  # <== must be sync
from api.agents.url_finder import find_product_urls   # <== must be sync
import json

class CPUAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.preferences = preferences or {}
        self.use_case = use_case

    def recommend(self):
        # Step 1: Ask LLM for CPU name (sync)
        name_prompt = f"""
You're a PC building expert.

Constraints:
Budget: {self.budget}
Region: {self.region}
Preferences: {self.preferences}
Use case: {self.use_case}

Suggest the best CPU within this budget, comply with the preference and use-case for the region. Respond ONLY with the CPU name and model. No explanation, no JSON, no extra text.
"""
        raw_name = generate_llama_response(name_prompt)
        cpu_name = raw_name.strip().strip('"')

        # Step 2: Sync find product URL + price
        product_data = find_product_urls(f"{cpu_name} buy online in {self.region}")
        url = product_data.get("url") or "https://example.com"
        price = product_data.get("price")

        # Step 3: Ask LLM for details (sync)
        details_prompt = f"""
You are a PC building expert.

Here is a CPU: "{cpu_name}"

The product was found at: {url}
The actual price listed there is: {price if price is not None else "null"}

Now based on this, return a valid, minified JSON object with realistic specs. Use the provided price and URL directly.

Format:
{{
    "name": "{cpu_name}",
    "socket": "...",
    "price": {price if price is not None else 'null'},
    "performance": ...,
    "vendor": "...",
    "url": "{url}"
}}

Only return JSON. No explanation.
"""
        final_response_raw = generate_llama_response(details_prompt)

        try:
            parsed = json.loads(final_response_raw)
        except Exception as e:
            print("❌ Failed to parse final LLaMA JSON:", e)
            parsed = {
                "name": cpu_name,
                "price": price,
                "performance": None,
                "socket": None,
                "vendor": None,
                "url": url
            }

        print("🧠 Final CPU Recommendation with scraped price:", parsed)
        return json.dumps(parsed)
