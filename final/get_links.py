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
BASE_DOWNLOAD_DIR = "data/iclr"  # Base directory for all years

# Define metrics per year (used in parser.py)
METRICS_BY_YEAR = {
    "2024": ["Soundness", "Presentation", "Contribution", "Rating", "Confidence"],
    "2023": ["Correctness", "Technical Novelty And Significance", "Empirical Novelty And Significance", "Recommendation", "Confidence"],
    "2022": ["Correctness", "Technical Novelty And Significance", "Empirical Novelty And Significance", "Recommendation", "Confidence"],
    "2021": ["Rating", "Confidence"]
}

# Ensure base directory exists
os.makedirs(BASE_DOWNLOAD_DIR, exist_ok=True)

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

def scrape_multiple_tabs(driver, year, base_url, tabs):
    """Scrapes multiple tabs for a given year and returns a list of (year, url) tuples."""
    combined_paper_urls = set()
    
    for tab_id in tabs:
        try:
            logging.info(f"Scraping tab: {tab_id} for year: {year}")
            driver.execute_script(f"document.querySelector('a[href=\"#{tab_id}\"]').click();")
            time.sleep(5)  # Allow time for the tab to load
            
            all_paper_urls = get_paper_urls_from_page(driver, base_url)
            combined_paper_urls.update(all_paper_urls)
        except Exception as e:
            logging.error(f"Error scraping tab {tab_id} for year {year}: {e}")
    
    # Format URLs with year
    formatted_urls = [f"{BASE_URL}{url}" for url in combined_paper_urls]
    return [(year, url) for url in formatted_urls]

def save_urls_to_file(filename, urls):
    """Saves the paper URLs to a text file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for _, url in urls:
                f.write(f"{url}\n")
        logging.info(f"Saved {len(urls)} URLs to {filename}")
    except Exception as e:
        logging.error(f"Error saving URLs to file {filename}: {e}")

def main():
    """Main function to orchestrate URL scraping."""
    # Define the groups per year with their respective tabs
    groups = [
        {
            "year": "2024",
            "base_url": "https://openreview.net/group?id=ICLR.cc/2024/Conference",
            "tabs": ["accept-oral", "accept-spotlight", "accept-poster", "reject"]
        },
        {
            "year": "2023",
            "base_url": "https://openreview.net/group?id=ICLR.cc/2023/Conference",
            "tabs": ["notable-top-25-", "poster", "submitted"]
        },
        {
            "year": "2022",
            "base_url": "https://openreview.net/group?id=ICLR.cc/2022/Conference",
            "tabs": ["spotlight-submissions", "poster-submissions", "submitted-submissions"]
        },
        {
            "year": "2021",
            "base_url": "https://openreview.net/group?id=ICLR.cc/2021/Conference",
            "tabs": ["submitted-submissions", "spotlight-presentations", "poster-presentations"]
        }
    ]

    all_papers = []

    driver = setup_selenium()
    try:
        # Scrape paper URLs for each group
        for group in groups:
            year = group["year"]
            base_url = group["base_url"]
            tabs = group["tabs"]
            logging.info(f"Starting URL scraping for year {year}...")
            papers = scrape_multiple_tabs(driver, year, base_url, tabs)
            all_papers.extend(papers)
            # Save URLs to a file per year
            save_urls_to_file(f"{BASE_DOWNLOAD_DIR}/iclr_{year}_paper_urls.txt", papers)
            logging.info(f"Completed URL scraping for year {year}.")
    finally:
        driver.quit()

    logging.info(f"Total papers scraped: {len(all_papers)}")

if __name__ == "__main__":
    main()
