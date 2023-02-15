import os
import requests
import bs4

def fetch_news(query):
    url = f"https://www.google.com/search?q={query}&tbm=nws"

    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                      "Accept-language": "en-US,en;q=0.9"})
    s.cookies.update({"CONSENT": "YES+cb.20201218-17-p0.en+FX+999"})

    response = s.get(url)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    # find links with role heading
    titles = soup.find_all("div", {"role": "heading"})

    if not titles:
        open("soup.html", "w").write(soup.prettify())
        os.system("xdg-open soup.html")

    news = []
    for title in titles:
        news.append((title.text, title.find_next_sibling("div").text))

    return news

if __name__ == "__main__":
    news = fetch_news("python")
    print(news)