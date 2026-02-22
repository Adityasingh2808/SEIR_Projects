# Project 1: Web Page Similarity Checker using SimHash

## Objective
The goal of this project is to **analyze and compare two web pages** to determine how similar their content is.  
It uses **SimHash**, a fingerprinting technique that efficiently detects near-duplicate content.

This tool extracts web page text, computes word frequencies, generates SimHash fingerprints, and compares them using **Hamming distance**.

## Key Concepts

| Concept                 | Description |
|-------------------------|-------------|
| Web Crawling            | Fetch live web pages via HTTP requests |
| HTML Parsing            | Extract titles, body text, and links from HTML |
| Text Tokenization       | Convert text to lowercase and extract words manually |
| Term Frequency (TF)     | Count occurrences of each word |
| Hashing                 | Use polynomial rolling hash for word representation |
| Document Fingerprinting | Generate SimHash values for the page |
| Similarity Measurement  | Use Hamming distance to compare fingerprints |

## Technologies Used
- Python 3.x  
- `requests` for fetching pages  
- `BeautifulSoup` (`bs4`) for HTML parsing  
- Standard Python libraries (`sys`, `urllib.parse`)  

## How It Works

### 1. Fetching Web Pages
- Sends HTTP requests with a custom **User-Agent** to avoid blocking.  
- Downloads the HTML content of the page.  

### 2. Extracting Content
- Removes `<script>` and `<style>` tags.  
- Extracts visible text from the page.  
- Collects all hyperlinks from `<a>` tags.

### 3. Tokenization
- Converts text to lowercase.  
- Extracts alphanumeric words manually.  

### 4. Word Frequency
- Counts the number of occurrences of each word in the page.  

### 5. SimHash Computation
- Computes a **64-bit fingerprint** of the page based on word frequency.  

### 6. Comparing Pages
- Computes **Hamming distance** between the two SimHash values.  
- Determines **common bits** and calculates a **similarity percentage**.

## Usage

### Analyze a Single Page
```bash
python project.py <URL>
```
### Compare two urls
```bash
python project.py <URL1> <URL2>
```
