import os
import json
import requests
import time

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from scraper.extractor import (
    accept_cookies,
    get_driver,
    get_article_urls,
    extract_content,
    get_article_data,
    get_image,
    close_driver,
    quit_driver
)
from scraper.translator import translate_title
from scraper.analyzer import analyze_titles
from scraper.config import HEADERS
from scraper.browsers import BROWSER_CAPS

os.makedirs("images", exist_ok=True)

urls = get_article_urls(BROWSER_CAPS[0])

def process_url(idx, url, cap):

    driver = get_driver(cap)  
    try:      
        driver.get(url)
        accept_cookies(cap)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title_tag = soup.select_one("h1") or soup.select_one("header h1")
        title = title_tag.text.strip() if title_tag else "N/A"
        content = extract_content(soup)

        if title == "N/A" and content == "":
            print("⚠️ Skipping empty article")
            return None

        image = get_image(soup)

        if image:
            try:
                img_response = requests.get(image, headers=HEADERS, timeout=15)
                img_response.raise_for_status()

                filename = os.path.join("images", f"article_{idx}.jpg")

                with open(filename, "wb") as f:
                    f.write(img_response.content)

                print("Saved:", filename)

            except Exception as e:
                print("Image download failed:", e)

        print("\nTITLE:", title)
        print("CONTENT:", content[:200])
        print("IMAGE:", image)

        return {
            "url": url,
            "title": title,
            "content": content,
            "image": image
        }
    except Exception as e:
        print("Error processing URL:", url, e)
        return None
    finally:
        quit_driver(driver)

articles_data = []

# PARALLEL EXECUTION (5 THREADS)
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {
        executor.submit(process_url, idx, url, BROWSER_CAPS[(idx - 1) % len(BROWSER_CAPS)]): idx
        for idx, url in enumerate(urls, start=1)
    }

    for future in as_completed(futures):
        result = future.result()
        if result:
            articles_data.append(result)

# scrape order
url_order = {url: i for i, url in enumerate(urls)}
articles_data.sort(key=lambda a: url_order[a["url"]])

print("\nTotal articles stored:", len(articles_data))


# TRANSLATION
for article in articles_data:

    english = translate_title(article["title"])
    article["translated_title"] = english

    print("\nSpanish:", article["title"])
    print("English:", english)

# ANALYSIS
result = analyze_titles(articles_data)

print("\nRepeated Words (>2 times):")
print(result)

# SAVE JSON
final_output = {
    "articles": articles_data,
    "repeated_words": result
}

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(final_output, f, indent=2, ensure_ascii=False)
    
close_driver()