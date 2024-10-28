# get_links.py

import os
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Configure Logging
logging.basicConfig(
    filename="get_links.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

# Constants
BASE_URL = "https://openreview.net"
CONFERENCE_URL = "https://openreview.net/group?id=ICLR.cc/2024/Conference"
DOWNLOAD_DIR = "data/iclr_2024"
URLS_FILE = os.path.join(DOWNLOAD_DIR, "urls.txt")

# Create directories if they don't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def setup_selenium():
    """Sets up Selenium with headless Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Initialize Service with ChromeDriver
    service = Service(ChromeDriverManager().install())
    
    # Initialize WebDriver with Service and Options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_paper_urls_from_page(driver, page_url):
    """Extract all unique paper URLs from the given OpenReview page."""
    try:
        logging.info(f"Accessing page: {page_url}")
        driver.get(page_url)
        time.sleep(5)  # Wait for the page to load completely

        soup = BeautifulSoup(driver.page_source, "html.parser")
        paper_links = soup.find_all("a", href=True)

        # Filter out URLs with '&noteId=' and ensure they contain 'forum?id='
        paper_urls = [
            link["href"]
            for link in paper_links
            if "forum?id=" in link["href"] and "&noteId=" not in link["href"]
        ]

        unique_paper_urls = list(set(paper_urls))
        logging.info(f"Found {len(unique_paper_urls)} unique paper URLs on the page.")
        return unique_paper_urls
    except Exception as e:
        logging.error(f"Error extracting paper URLs from {page_url}: {e}")
        return []

def save_urls(urls, filename):
    """Saves the list of URLs to a text file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for url in urls:
                f.write(f"{BASE_URL}{url}\n")
        logging.info(f"Saved {len(urls)} URLs to {filename}")
    except Exception as e:
        logging.error(f"Error saving URLs to {filename}: {e}")

def main():
    driver = setup_selenium()
    try:
        all_paper_urls = []
        # If there are multiple pages, iterate over them
        # For ICLR, typically all papers are on a single page, but adjust if necessary
        paper_urls = get_paper_urls_from_page(driver, CONFERENCE_URL)
        all_paper_urls.extend(paper_urls)
        
        # Save the collected URLs to a file
        save_urls(all_paper_urls, URLS_FILE)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
