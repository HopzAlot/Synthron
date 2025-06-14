from api.agents.llama import generate_llama_response

class RAMAgent:
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
- Use case: {self.use_case}

You must recommend a single RAM module.

You are a PC building expert.

Given the following requirements, recommend the best RAM available within the budget. Scrap the web and find the best most cheapest yet perfect RAM option off the internet in the given region. And Give real valid links to that website. Only recommend the parts which are available.

Use this exact format:
{{
    "name": "Kingston Fury Beast 16GB DDR4",
    "ram_type": "DDR4",
    "price": 100,
    "performance": 97,
    "vendor": "Flipkart India",
    "url": "https://example.com/kingston16gb"
}}
"""
        response = generate_llama_response(prompt)
        print("🧠 Raw RAM LLaMA Response:", response)
        return response
