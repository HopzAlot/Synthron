from api.agents.llama import generate_llama_response

class STORAGEAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}

    def recommend(self):
        prompt = f"""
Only respond with a single-line minified JSON object. No markdown, no explanation.

Requirements:
- Budget: {self.budget}
- Region: {self.region}
- Preferences: {self.preferences}
- Use-case: {self.use_case}

Recommend a single best-fit **storage device** under budget.

You are a PC building expert.

Given the following requirements, recommend the best Storage option available within the budget. Scrap the web and find the best most cheapest yet perfect Storage option option off the internet in the given region. And Give real valid links to that website. Only recommend the parts which are available.

Use this exact structure:
{{
    "name": "Samsung 500GB NVMe SSD",
    "price": 120,
    "performance": 90,
    "vendor": "Flipkart India",
    "url": "https://example.com/SSD500GB"
}}
"""
        response = generate_llama_response(prompt)
        print("🧠 Raw STORAGE LLaMA Response:", response)
        return response
