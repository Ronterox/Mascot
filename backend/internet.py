import os
import requests
from bs4 import BeautifulSoup

LOG_PATH = "logs/soup.html"

def fetch_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"

    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                      "Accept-language": "en-US,en;q=0.9"})
    s.cookies.update({"CONSENT": "YES+cb.20201218-17-p0.en+FX+999"})

    response = s.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # find links with role heading
    titles = soup.find_all("div", {"role": "heading"})

    if not titles:
        open(LOG_PATH, "w").write(soup.prettify())
        os.system(f"xdg-open {LOG_PATH}")

    news = []
    for title in titles:
        desc = title.find_next_sibling("div")
        news.append((title.text, desc.text if desc is not None else ""))

    return news

if __name__ == "__main__":
    news = fetch_news("video games")
    for title, desc in news:
        print(f"{title:-^100}")
        print(desc)
        print()
