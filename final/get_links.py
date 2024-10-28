# get_links.py

import os
import re
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Define metrics per year
METRICS_BY_YEAR = {
    "2024": ["Soundness", "Presentation", "Contribution", "Rating", "Confidence"],
    "2023": ["Correctness", "Technical Novelty And Significance", "Empirical Novelty And Significance", "Recommendation", "Confidence"],
    "2022": ["Correctness", "Technical Novelty And Significance", "Empirical Novelty And Significance", "Recommendation", "Confidence"],
    "2021": ["Rating", "Confidence"]
}

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
        driver.get(page_url)
        time.sleep(3)  # Allow some time for the page to load
        soup = BeautifulSoup(driver.page_source, "html.parser")
        paper_links = soup.find_all("a", href=True)

        # Filter out URLs with '&noteId=' and ensure they contain 'forum?id='
        paper_urls = [
            link["href"]
            for link in paper_links
            if "forum?id=" in link["href"] and "&noteId=" not in link["href"]
        ]

        logging.info(f"Found {len(paper_urls)} paper URLs on page: {page_url}")
        return paper_urls
    except Exception as e:
        logging.error(f"Error extracting URLs from page {page_url}: {e}")
        return []

def switch_to_tab_with_js(driver, tab_id):
    """Use JavaScript to switch to the desired tab to avoid click interception."""
    try:
        logging.info(f"Switching to {tab_id} tab using JavaScript...")
        driver.execute_script(f"document.querySelector('a[href=\"#{tab_id}\"]').click();")
        time.sleep(5)  # Allow time for the page to update after clicking the tab
    except Exception as e:
        logging.error(f"Failed to switch to {tab_id} tab: {e}")

def go_to_next_page(driver):
    """Navigate to the next page in pagination."""
    try:
        # Look for the "Next" button in the pagination section and click it
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.right-arrow > a'))
        )
        next_button.click()
        time.sleep(3)  # Allow some time for the next page to load
        return True
    except Exception:
        logging.info("No more pages to navigate.")
        return False

def scrape_all_pages(driver, year, base_url, tab_id):
    """Scrapes all pages from a single tab."""
    switch_to_tab_with_js(driver, tab_id)
    
    all_paper_urls = set()
    page_count = 1

    while True:
        logging.info(f"Scraping page {page_count} of {tab_id} tab for year {year}...")
        paper_urls = get_paper_urls_from_page(driver, base_url)
        all_paper_urls.update(paper_urls)
        
        if not go_to_next_page(driver):  # Stop if there are no more pages
            break
        
        page_count += 1

    return all_paper_urls

def scrape_multiple_tabs(year, base_url, tabs):
    """Scrapes multiple tabs for a given year."""
    driver = setup_selenium()
    driver.get(base_url)
    time.sleep(5)  # Give the page some time to load

    combined_paper_urls = set()
    
    for tab_id in tabs:
        logging.info(f"Scraping {tab_id} tab for year {year}...")
        paper_urls = scrape_all_pages(driver, year, base_url, tab_id)
        combined_paper_urls.update(paper_urls)
    
    driver.quit()

    # Return a list of (year, formatted_url)
    formatted_urls = [f"https://openreview.net{url}" for url in combined_paper_urls]
    return [(year, url) for url in formatted_urls]

def save_urls_to_file(filename, urls):
    """Saves the paper URLs to a text file."""
    try:
        with open(filename, 'w') as f:
            for url in urls:
                f.write(f"{url}\n")
        logging.info(f"Saved {len(urls)} URLs to {filename}")
    except Exception as e:
        logging.error(f"Error saving URLs to file {filename}: {e}")

def main():
    """Main function to orchestrate scraping of paper URLs."""
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

    # Scrape paper URLs for each group
    for group in groups:
        year = group["year"]
        base_url = group["base_url"]
        tabs = group["tabs"]
        logging.info(f"Starting URL scraping for year {year}...")
        papers = scrape_multiple_tabs(year, base_url, tabs)
        all_papers.extend(papers)
        save_urls_to_file(f"{year}_paper_urls.txt", [url for _, url in papers])
        logging.info(f"Completed URL scraping for year {year}.")

    logging.info(f"Total papers scraped: {len(all_papers)}")

if __name__ == "__main__":
    main()
