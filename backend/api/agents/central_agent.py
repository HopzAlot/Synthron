import re
import json
from api.agents.cpu_agent import CPUAgent
from api.agents.gpu_agent import GPUAgent
from api.agents.motherboard_agent import MotherboardAgent
from api.agents.ram_agent import RAMAgent
from api.agents.storage_agent import STORAGEAgent
from api.compatibility_checker import check_compatibility
from api.agents.llama import generate_llama_response 

class CentralAgent:
    def __init__(self, prompt):
        self.prompt = prompt

    def clean_llama_output(self, output):
        return output.strip().replace("```json", "").replace("```", "").strip()

    def safe_json_parse(self, json_string):
        try:
            match = re.search(r'\{.*?\}', self.clean_llama_output(json_string), re.DOTALL)
            if match:
                return json.loads(match.group(0))
            else:
                print("No valid JSON object found.")
                return {}
        except Exception as e:
            print("LLaMA response parsing failed:", e)
            return {}

    def parse_prompt(self):
        prompt_text = f"""Extract structured PC build requirements from this prompt:
"{self.prompt}"

Respond only with valid minified JSON like:
{{"budget":1200,"region":"US","preferences":"Intel","use_case":"gaming"}}

No markdown, no explanations, no comments. If extraction fails, return: {{}}
"""
        llama_response = generate_llama_response(prompt_text)  
        print("LLaMA response:", llama_response)
        return self.safe_json_parse(llama_response)

    def get_price(self, component):
        try:
             price = component.get('price', 0)
             return float(price) if isinstance(price, (int, float, str)) and str(price).replace('.', '', 1).isdigit() else 0
        except Exception:
            return 0


    def run(self):
        parsed = self.parse_prompt()
        if not parsed:
            return {"error": "Failed to parse build requirements from prompt."}

        budget = parsed.get("budget", 1000)
        preferences = parsed.get("preferences") or "Intel"
        use_case = parsed.get("use_case") or "general"
        region = parsed.get("region") or "US"

        cpu = self.safe_json_parse(CPUAgent(budget * 0.3, region, preferences, use_case).recommend())
        gpu = self.safe_json_parse(GPUAgent(budget * 0.4, region, preferences, use_case).recommend())
        ram = self.safe_json_parse(RAMAgent(budget * 0.15, region, preferences, use_case).recommend())
        storage = self.safe_json_parse(STORAGEAgent(budget * 0.15, region, preferences, use_case).recommend())
        motherboard = self.safe_json_parse(
            MotherboardAgent(
                budget * 0.15, region, preferences, use_case,
                required_ram_type=ram.get("ram_type"),
                required_socket=cpu.get("socket")
            ).recommend()
        )

        if not isinstance(gpu, list):
            gpu = [gpu]

        try:
            total_cost = (
                self.get_price(cpu) +
                sum(self.get_price(g) for g in gpu) +
                self.get_price(ram) +
                self.get_price(storage) +
                self.get_price(motherboard)
            )
        except Exception as e:
            return {
                "error": "One or more components returned invalid or incomplete data.",
                "details": str(e),
                "build": {
                    "CPU": cpu,
                    "GPU": gpu,
                    "RAM": ram,
                    "Storage": storage,
                    "Motherboard": motherboard
                }
            }

        issues = check_compatibility(cpu, ram, motherboard, gpu) or []

        if total_cost > budget:
            issues.append(f"Total build cost ${total_cost:.2f} exceeds your budget of ${budget:.2f}.")

        consolidated_input = json.dumps({
            "CPU": cpu,
            "GPU": gpu,
            "RAM": ram,
            "Storage": storage,
            "Motherboard": motherboard,
            "issues": issues,
        })

        summary_prompt = f"Here is the build info: {consolidated_input}. Write a detailed but user-friendly summary for the user."
        summary = generate_llama_response(summary_prompt)
        return {
            "summary": summary or "No summary generated.",
            "build": {
                "CPU": cpu,
                "GPU": gpu,
                "RAM": ram,
                "Storage": storage,
                "Motherboard": motherboard
            },
            "total": total_cost,
            "issues": issues
        }