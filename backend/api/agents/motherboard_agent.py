from api.agents.llama import generate_llama_response  # sync version
from api.agents.url_finder import find_product_urls    # sync version
import json

class MotherboardAgent:
    def __init__(self, budget, region, preferences, use_case, required_socket, required_ram_type):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}
        self.required_socket = required_socket
        self.required_ram_type = required_ram_type

    def recommend(self):
        
        name_prompt = f"""
You're a PC building expert.

Suggest the best Motherboard within this budget and use-case for the region.
It must support socket: {self.required_socket} and RAM type: {self.required_ram_type}.

Respond ONLY with the Motherboard name and model. No explanations or JSON.

Budget: {self.budget}
Region: {self.region}
Preferences: {self.preferences}
Use case: {self.use_case}
"""
        raw_name = generate_llama_response(name_prompt)
        mb_name = raw_name.strip().strip('"')

        
        product_data = find_product_urls(f"{mb_name} buy online in {self.region}")
        url = product_data.get("url") or "https://example.com"
        price = product_data.get("price")
        socket=product_data.get('socket')
        vendor=product_data.get('vendor') or 'not provided'
        performance=product_data.get('performance')
        name=product_data.get('name')
        ram_type=product_data.get('ram_type')

       
        details_prompt = f"""
You are a PC building expert.

Here is a Motherboard: "{mb_name}"

The product was found at: {url}
The actual price listed there is: {price if price is not None else "null"}

Return a valid minified JSON with specs and price, using the given details.

Format:
{{
    "name": "{name}" or "not provided",
    "socket": "{socket}" or "not provided",
    "price": {price if price is not None else "null"},
    "ram_type": "{ram_type}" or "not provided",
    "vendor": '{vendor}' or "not provided",
    "performance": '{performance}' or "not provided",
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
                "name": mb_name,
                "socket": self.required_socket,
                "price": price,
                "ram_type": self.required_ram_type,
                "vendor": None,
                "url": url
            }

        print("🧩 Final Motherboard recommendation with scraped price:", parsed)
        return json.dumps(parsed)