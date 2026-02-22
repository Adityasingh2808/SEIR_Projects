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

def process_single(url):
    html = fetch_page(url)
    title = extract_title(html)
    body = extract_body(html)
    links = extract_links(html, url)

    frequency = cal_frequency(body)

    print("\nWebsite Title:", title)

    print("\nFirst 1000 characters of body:")
    print(body[:1000])

    print("\nTotal Links Found:", len(links))
    for i in range(len(links)):
        print(i + 1, links[i])

    print("\nCount Words:")
    sorted_words = sorted(frequency.items(), key=lambda x: x[1], reverse=True)

    for word, count in sorted_words[:]:
        print(word, ":", count)

    print("\nSimhash Value:", simhash(body))

def compare_two(url1, url2):
    html1 = fetch_page(url1)
    html2 = fetch_page(url2)

    title1 = extract_title(html1)
    title2 = extract_title(html2)

    body1 = extract_body(html1)
    body2 = extract_body(html2)

    links1 = extract_links(html1, url1)
    links2 = extract_links(html2, url2)

    freq1 = cal_frequency(body1)
    freq2 = cal_frequency(body2)

    hash1 = simhash(body1)
    hash2 = simhash(body2)

    distance = cal_hamming(hash1, hash2)
    total_bits = 64
    common_bits = total_bits - distance
    similarity = (common_bits / total_bits) * 100
    
    print("Title:", title1)
    print("\nBody (first 1000 chars):")
    print(body1[:1000])
    print("\nWord Frequency:")
    for word, count in sorted(freq1.items(), key=lambda x: x[1], reverse=True):
        print(word, ":", count)
    print("\nTotal Links Found:", len(links1))
    count = 1
    for link in links1:
        print(count, link)
        count += 1
    print("Simhash:", hash1)
    
    print("Title:", title2)
    print("\nBody (first 1000 chars):")
    print(body2[:1000])
    print("\nWord Frequency:")
    for word, count in sorted(freq2.items(), key=lambda x: x[1], reverse=True):
        print(word, ":", count)
    print("\nTotal Links Found:", len(links2))
    count = 1
    for link in links2:
        print(count, link)
        count += 1
    print("Simhash:", hash2)

    print("\n    Comparison     ")
    print("Hamming Distance:", distance)
    print("Common Bits:", common_bits)
    print(f"Similarity: {similarity:.2f}%")

def main():
    if len(sys.argv) == 2:
        process_single(sys.argv[1])

    elif len(sys.argv) == 3:
        compare_two(sys.argv[1], sys.argv[2])

    else:
        print("Usage:")
        print("python project.py <URL>")
        print("python project.py <URL1> <URL2>")


if __name__ == "__main__":
    main()
