import requests
import time
from scraper.config import HEADERS

def get_page(url, retries=3):
    for attempt in range(retries):
        print(f"Request attempt {attempt+1} for {url}")

        response = requests.get(url, headers=HEADERS)

        if "h1" in response.text:
            return response.text

        print("⚠️ Possible blocked response")
        time.sleep(5)

    print("❌ Failed after retries")
    return None