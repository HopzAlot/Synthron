from dotenv import load_dotenv
load_dotenv()
import os
from scrapegraph_py import Client
from scrapegraph_py.logger import sgai_logger

sgai_logger.set_logging(level="INFO")

SGAI_API_KEY = os.getenv("SCRAPEGRAPH_API_KEY")
if not SGAI_API_KEY:
    raise ValueError("❌ SCRAPEGRAPH_API_KEY is missing from .env")

client = Client(api_key=SGAI_API_KEY)


def scrape_with_scrapegraph(urls: list[str], prompt: str) -> list[dict]:
    results = []

    for url in urls:
        try:
            response = client.smartscraper(
                website_url=url,
                user_prompt=prompt
            )
            if isinstance(response, dict):
                response["url"] = url
                results.append(response)
        except Exception as e:
            print(f"❌ Error scraping {url}: {str(e)}")

    return results
