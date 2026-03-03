from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def fetch_page(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(3)
    html = driver.page_source
    driver.quit()
    return html

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
    text = text.lower()
    words = []
    current_word = ""
    for char in text:
        if char.isalnum():
            current_word += char
        else:
            if current_word != "":
                words.append(current_word)
                current_word = ""
                
    if current_word != "":
        words.append(current_word)

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

def process_single(url):
    html = fetch_page(url)
    title = extract_title(html)
    body = extract_body(html)
    links = extract_links(html, url)
    print("\nWebsite Title:", title)
    print("\nFirst 1000 characters of body:")
    print(body[:1000])
    print("\nTotal Links Found:", len(links))
    for i in range(len(links)):
        print(i + 1, links[i])

def valid_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def main():
    if len(sys.argv) == 2:
        url = valid_url(sys.argv[1])
        process_single(url)
    else:
        print("Use : python project.py <URL>")

if __name__ == "__main__":
    main()
