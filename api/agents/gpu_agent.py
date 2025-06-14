from api.agents.llama import generate_llama_response

class GPUAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}

    def recommend(self):
        prompt = f"""
Only respond with a single minified JSON object. No markdown, no explanation, no array.

Requirements:
- Budget: {self.budget}
- Region: {self.region}
- Preferences: {self.preferences}
- Use case: {self.use_case}

Given the following requirements, recommend the best GPU available within the budget. Scrap the web and find the best most cheapest yet perfect gpu option off the internet in the given region. And Give real valid links to that website. Only recommend the parts which are available.

Format:
{{
    "name": "NVIDIA RTX 4060",
    "power_draw": 500,
    "price": 320,
    "performance": 88,
    "vendor": "Flipkart India",
    "url": "https://example.com/rtx4060"
}}
"""
        response = generate_llama_response(prompt)
        print("🎮 Raw GPU LLaMA Response:", response)  # For debugging
        return response
