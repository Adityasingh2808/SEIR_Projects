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

def rolling_hash(word):
    base = 53
    mod = 2**64
    hash_value = 0

    for char in word:
        hash_value = (hash_value * base + ord(char)) % mod

    return hash_value

def simhash(text):
    freq = cal_frequency(text)
    bit_vector = [0] * 64 

    for word in freq:
        h = rolling_hash(word)
        for i in range(64):
            bit = (h >> i) & 1
            if bit == 1:
                bit_vector[i] += freq[word]
            else:
                bit_vector[i] -= freq[word]

    final_hash = 0
    for i in range(64):
        if bit_vector[i] > 0:
            final_hash |= (1 << i)

    return final_hash

def cal_hamming(hash1, hash2):
    xor_value = hash1 ^ hash2
    count = 0

    while xor_value > 0:
        if xor_value % 2 == 1:
            count += 1
        xor_value = xor_value // 2

    return count
