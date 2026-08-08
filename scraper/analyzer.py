from collections import Counter
import re

def analyze_titles(articles):

    titles = [
        a["translated_title"]
        for a in articles
        if a.get("translated_title") and a["translated_title"] != "N/A"
    ]

    text = " ".join(titles)

    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())

    counter = Counter(words)

    return {word: count for word, count in counter.items() if count > 2}