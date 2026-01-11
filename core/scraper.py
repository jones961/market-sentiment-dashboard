import requests
from bs4 import BeautifulSoup

def scrape_reuters_finance(limit=None):
    """
    Scrapes finance headlines from Reuters (via CNBC RSS feed).

    Args:
        limit (int, optional): Number of headlines to return. If None, return all.

    Returns:
        list[str]: List of headline strings.
    """
    url = "https://www.cnbc.com/id/100003114/device/rss/rss.html"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "xml")
    headlines = [item.title.text for item in soup.find_all("item")]

    # Apply limit if specified
    if limit is not None:
        headlines = headlines[:limit]

    return headlines
