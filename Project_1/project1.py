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

def extract_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    all_links = []

    for link in soup.find_all("a"):
        href = link.get("href")
        if href is None:
            continue   
        if href.startswith("#"):
            continue
        full_link = urljoin(base_url, href)
        if full_link.startswith("http"):
            all_links.append(full_link)

    return all_links

def get_words_list(text):
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return words

def cal_frequency(text):
    words = get_words_list(text)
    frequency = {}

    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency



