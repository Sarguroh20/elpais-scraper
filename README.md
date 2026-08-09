# 🇪🇸 El País Opinion Scraper

> A Python-based Selenium web scraping project that extracts, translates, and analyzes articles from the El País Opinion section, with BrowserStack cross-browser testing.

---

## 📌 Overview

This project automates the following workflow:

- 📰 Scrapes the first 5 articles from the **El País Opinion** section
- 🇪🇸 Extracts article titles and content in Spanish
- 🖼️ Downloads available cover images
- 🇬🇧 Translates article titles from Spanish to English using a translation API
- 🔤 Analyzes translated titles for repeated words
- ⚡ Uses parallel execution for scraping
- 🧪 Performs cross-browser testing using BrowserStack
- 💾 Stores the final results in `output.json`

## ✨ Workflow

```text
                    🇪🇸 El País
                         │
                         ▼
                 📰 Opinion Section
                         │
                         ▼
                  First 5 Articles
                         │
                         ▼
                 ⚡ Parallel Scraping
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
       📰 Title       📝 Content      🖼️ Image
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                 🌐 Translation API
                         │
                         ▼
                  🇬🇧 English Titles
                         │
                         ▼
                  🔤 Word Analysis
                         │
                         ▼
                    💾 output.json
                         │
                         ▼
                 🧪 BrowserStack
                Cross-Browser Tests
```

## 🛠️ Tech Stack

- **Python**
- **Selenium WebDriver**
- **BeautifulSoup4**
- **Requests**
- **BrowserStack** — cross-browser testing

## ✅ Requirements Checklist

- [x] Visit El País with Spanish content
- [x] Scrape first 5 Opinion articles (title + content)
- [x] Download cover images
- [x] Translate titles via translation API
- [x] Identify words repeated more than twice across translated headlines
- [x] Run locally to verify functionality
- [x] Execute on BrowserStack across 5 parallel threads
- [x] Cross-browser/device coverage: Chrome, Firefox, Edge, Safari, and a real iOS device

## 📄 Sample Output

```json
{
  "articles": [
    {
      "url": "https://elpais.com/opinion/2026-08-09/el-eclipse-de-todos.html",
      "title": "El eclipse de todos",
      "content": "La mayor cita astronómica en décadas unirá al país...",
      "image": "https://imagenes.elpais.com/resizer/v2/2ZVPD2G52JHUVEXBH2DJ272ZYQ.jpg?auth=416a7afb535ea520fb6ad1ff64ba2980b6d205fd5eecb21fd07c292dcb1d1c39&width=414",
      "translated_title": "everyone's eclipse"
    },
    {
      "url": "https://elpais.com/opinion/2026-08-09/la-democracia-comienza-donde-termina-el-enemigo.html",
      "title": "La democracia comienza donde termina el enemigo",
      "content": "La democracia no elimina los conflictos, los transforma...",
      "image": "https://imagenes.elpais.com/resizer/v2/YNYXLAZOCJATDIDWP5VE3V5GMA.jpg?auth=b3105c2bdc2a6044891886035d630198aaecc937315cdb6e238cc340d41ce6fe&width=414",
      "translated_title": "Democracy begins where the enemy ends"
    }
  ],
  "repeated_words": {}
}
```

## 🔗 BrowserStack Build

👉 [BrowserStack Build](https://automate.browserstack.com/projects/Default+Project/builds/ElPais+Scraper+Test/5?tab=sessions&sessionStatus=Unmarked&match=%7B%22sessionStatus%22%3A%22OR%22%7D&bls_projects=2653530%7CDefault%2520Project&public_token=31246ecbcefe90617754d49bb5a51578a2430fc23362463cef98db8e16eb1774)

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sarguroh20/elpais-scraper.git
cd elpais-scraper
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a .env file in the root directory

```bash
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
```

### 4. Run the Project

```bash
python main.py
```
