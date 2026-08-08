import os
import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv

from scraper.utils import get_page
from scraper.config import BASE_URL

load_dotenv()

# driver = webdriver.Chrome()
USERNAME = os.environ.get("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY")

_thread_local = threading.local()
_all_drivers = []
_lock = threading.Lock()

def get_driver(cap):
    if not hasattr(_thread_local, "driver"):
        opts = Options()
        for key, value in cap.items():
            opts.set_capability(key, value)

        opts.set_capability("bstack:options", {
            
            **cap.get("bstack:options", {}),
            "buildName": "ElPais Scraper Test",
            "sessionName": f"ElPais Scraper - {threading.current_thread().name}"
        })
        d = webdriver.Remote(
            command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub",
            options=opts
        )
        _thread_local.driver = d
        with _lock:
            _all_drivers.append(d)
    return _thread_local.driver


# def accept_cookies():
#     try:
#         button = WebDriverWait(get_driver(), 5).until(
#             EC.element_to_be_clickable(
#                 (By.XPATH, "//button[contains(., 'Aceptar') or contains(., 'Accept')]")
#             )
#         )
#         button.click()
#         print("✅ Cookies accepted")
#     except:
#         print("⚠️ No cookie button found")

def accept_cookies(cap):
    driver = get_driver(cap)

    try:
        buttons = driver.find_elements(By.TAG_NAME, "button")

        for button in buttons:
            text = button.text.strip().lower()

            if "aceptar" in text or "accept" in text:
                driver.execute_script(
                    "arguments[0].click();",
                    button
                )

                print("✅ Cookies accepted")
                return True

        print("⚠️ No cookie button found")
        return False

    except Exception as e:
        print("⚠️ Cookie handling failed:", e)
        return False

def get_article_urls(cap):
    driver = get_driver(cap)
    driver.get(BASE_URL)
    accept_cookies(cap)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # retry cookie page
    if "cookies" in soup.text.lower():
        print("⚠️ Cookie page detected, retrying...")
        time.sleep(3)
        driver.get(BASE_URL)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    links = soup.select("h2 a")
    urls = []

    for a in links:
        href = a.get("href")
        if href and "/opinion/" in href:
            if href.startswith("/"):
                href = "https://elpais.com" + href
            urls.append(href)

    return list(dict.fromkeys(urls))[:5]

def extract_content(soup):
    article = soup.find("article")

    if article:
        paragraphs = article.find_all("p")
    else:
        # fallback: get all visible paragraphs
        paragraphs = soup.select("p")


    content = " ".join([
        p.get_text().strip()
        for p in paragraphs
        if len(p.get_text().strip()) > 40
         and "cookie" not in p.get_text().lower()
        and "consent" not in p.get_text().lower()
    ])

    return content

def get_article_data(url, cap):

    print("\nOpening:", url)

    html = get_page(url)

    if html:
        soup = BeautifulSoup(html, "html.parser")
    else:
        print("⚠️ Switching to Selenium:", url)

        driver = get_driver(cap)
        driver.get(url)
        accept_cookies(cap)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "article p"))
            )
        except:
            print("⚠️ Page load timeout, continuing...")
        
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    title_tag = soup.select_one("h1") or soup.select_one("header h1")

    if not title_tag:
        print("⚠️ Requests failed. Using Selenium...")
    
        driver = get_driver(cap)
        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        title_tag = soup.find("h1") or soup.select_one("header h1")

    title = title_tag.text.strip() if title_tag else "N/A"
    content = extract_content(soup)

    return title, content, soup

def get_image(soup):
    img = soup.select_one("figure img") or soup.select_one("img")

    if img:
        return img.get("src") or img.get("data-src") or img.get("srcset")

    return None

def quit_driver(driver):
    try:
        driver.quit()
    except Exception:
        pass
    with _lock:
        if driver in _all_drivers:
            _all_drivers.remove(driver)

def close_driver():
    with _lock:
        for d in _all_drivers:
            try:
                d.quit()
            except Exception:
                pass
        _all_drivers.clear()