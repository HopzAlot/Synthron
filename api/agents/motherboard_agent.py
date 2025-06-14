from api.agents.llama import generate_llama_response

class MotherboardAgent:
    def __init__(self, budget, region, preferences, use_case, required_socket, required_ram_type):
        self.budget = budget
        self.region = region
        self.use_case = use_case
        self.preferences = preferences or {}
        self.required_socket = required_socket
        self.required_ram_type = required_ram_type

    def recommend(self):
        prompt = f"""
Only respond with a single minified JSON object. No markdown, no explanations.

You're recommending a motherboard based on:
- Budget: {self.budget}
- Region: {self.region}
- Preferences: {self.preferences}
- Use case: {self.use_case}
- Required CPU socket: {self.required_socket}
- Required RAM type: {self.required_ram_type}

You are a PC building expert.

Given the following requirements, recommend the best Motherboard available within the budget. Scrap the web and find the best most cheapest yet perfect motherboard option off the internet in the given region. And Give real valid links to that website. Only recommend the parts which are available.

Respond in this exact format:
{{
    "name": "ASUS ROG B650",
    "socket": "AM5",
    "price": 150,
    "ram_type": "DDR4",
    "vendor": "Amazon India",
    "url": "https://example.com/asus-b650"
}}
"""
        response = generate_llama_response(prompt)
        print("🧩 Raw Motherboard Response:", response)
        return response
