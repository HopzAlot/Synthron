from api.agents.llama import generate_llama_response

class CPUAgent:
    def __init__(self, budget, region, preferences, use_case):
        self.budget = budget
        self.region = region
        self.preferences = preferences or {}
        self.use_case = use_case

    def recommend(self):
        prompt = f"""
You are a PC building expert.

Given the following requirements, recommend the best CPU available within the budget. Scrap the web and find the best most cheapest yet perfect cpu option off the internet in the given region. And Give real valid links to that website. Only recommend the parts which are available.

Respond ONLY with a valid, minified JSON object like:
{{"name":"AMD Ryzen 5 5600","socket":"AM4","price":160,"performance":85,"vendor":"Amazon India","url":"https://example.com/ryzen5600"}}

Requirements:
- Budget: {self.budget}
- Region: {self.region}
- Preferences: {self.preferences}
- Use case: {self.use_case}

Do NOT return the input data or explain anything. Only the recommended CPU object.
"""
        response = generate_llama_response(prompt)
        print("🧠 Raw CPU LLaMA Response:", response)  # For debugging
        return response
