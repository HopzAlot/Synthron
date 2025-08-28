from api.agents.llama import generate_llama_response 
from api.agents.url_finder import find_product_urls  
import json

class GPUAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}

    def recommend(self):
        name_prompt = f"""
You're a PC building expert.

Suggest the best GPU within this budget and use-case for the region. Respond ONLY with the GPU name and model. No explanation, no JSON, no extra text.

Budget: {self.budget}
Region: {self.region}
Preferences: {self.preferences}
Use case: {self.use_case}
"""
        raw_name = generate_llama_response(name_prompt)
        gpu_name = raw_name.strip().strip('"')

        product_data = find_product_urls(f"{gpu_name} buy online in {self.region}")
        url = product_data.get("url") or "https://example.com"
        price = product_data.get("price")
        power_draw= product_data.get('power_draw')
        vendor=product_data.get('vendor') or 'not provided'
        performance=product_data.get('performance')
        name=product_data.get('name')


        
        details_prompt = f"""
You are a PC building expert.

Here is a GPU: "{gpu_name}"

The product was found at: {url}
The actual price listed there is: {price if price is not None else "null"}

Now based on this, return a valid, minified JSON object with realistic specs. Use the provided details directly.

Format:
{{
    "name": "{name}",
    "power_draw": {power_draw} or 0,
    "price": {price if price is not None else 'null'},
    "performance": "{performance}" or "not provided",
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
                "name": gpu_name,
                "power_draw": None,
                "price": price,
                "performance": None,
                "vendor": None,
                "url": url
            }

        print("🎮 Final GPU Recommendation with scraped price:", parsed)
        return json.dumps(parsed)