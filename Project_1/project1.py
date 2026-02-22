import requests
from bs4 import BeautifulSoup
import re
import sys
from urllib.parse import urljoin

def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error: Unable to fetch page")
        sys.exit()

    return response.text

def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.find("title")

    if title_tag:
        return title_tag.text.strip()
    else:
        return "No Title Found"

def extract_body(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text()
    text = " ".join(text.split())

    return text
