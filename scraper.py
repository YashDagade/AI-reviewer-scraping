# scraper.py

import os
import re
import time
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# Configure Logging
logging.basicConfig(
    filename="scraper.log",
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
DOWNLOAD_DIR = "data/iclr_2024"
HTML_DIR = os.path.join(DOWNLOAD_DIR, "HTML")
PDF_DIR = os.path.join(DOWNLOAD_DIR, "PDF")
URLS_FILE = os.path.join(DOWNLOAD_DIR, "urls.txt")
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0; +https://yourdomain.com/)"
}

# Create directories if they don't exist
for directory in [DOWNLOAD_DIR, HTML_DIR, PDF_DIR]:
    os.makedirs(directory, exist_ok=True)

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

def fetch_html(driver, url, timeout=20):
    """Fetches the fully rendered HTML content of a given URL using Selenium."""
    try:
        logging.info(f"Fetching URL: {url}")
        driver.get(url)

        # Wait until the main content is loaded
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, "note"))
        )

        # Optional: Scroll to the bottom to ensure all lazy-loaded content is fetched
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for additional content to load

        html = driver.page_source
        logging.info(f"Successfully fetched URL: {url}")
        return html
    except TimeoutException:
        logging.error(f"Timeout while loading {url}")
        return None
    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")
        return None

def parse_paper_info(soup):
    """Parses the paper's BeautifulSoup object to extract metadata."""
    paper_info = {}

    # Extract Title
    title_tag = soup.find("h2", class_="citation_title")
    paper_info["title"] = title_tag.text.strip() if title_tag else "N/A"

    # Extract Authors
    authors_tag = soup.find("div", class_="forum-authors")
    if authors_tag:
        authors = [author.text.strip() for author in authors_tag.find_all("a")]
        paper_info["authors"] = authors
    else:
        paper_info["authors"] = []

    # Extract Publication Date
    pub_date_tag = soup.find("span", class_="glyphicon-calendar")
    if pub_date_tag and pub_date_tag.parent:
        dates_text = pub_date_tag.parent.text.strip()
        publication_date = re.search(r"Published:\s*(.*?)(?:,|$)", dates_text)
        paper_info["publication_date"] = (
            publication_date.group(1) if publication_date else "N/A"
        )
    else:
        paper_info["publication_date"] = "N/A"

    # Extract PDF URL
    pdf_link_tag = soup.find("a", class_="citation_pdf_url")
    if pdf_link_tag and "href" in pdf_link_tag.attrs:
        pdf_url = pdf_link_tag["href"]
        if not pdf_url.startswith("http"):
            pdf_url = BASE_URL + pdf_url
        paper_info["pdf_url"] = pdf_url
    else:
        paper_info["pdf_url"] = None

    return paper_info

def download_pdf(pdf_url, save_path):
    """Downloads the PDF from the given URL to the specified path."""
    try:
        logging.info(f"Downloading PDF: {pdf_url}")
        response = requests.get(pdf_url, headers=HEADERS)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        logging.info(f"Downloaded PDF to {save_path}")
        return True
    except requests.RequestException as e:
        logging.error(f"Error downloading PDF from {pdf_url}: {e}")
        return False

def scrape_paper(driver, paper_url):
    """Scrapes a single paper: downloads HTML and PDF."""
    logging.info(f"Starting scraping for paper: {paper_url}")
    html = fetch_html(driver, paper_url)
    if not html:
        logging.warning(f"Failed to retrieve HTML for {paper_url}. Skipping.")
        return
    
    paper_id_match = re.search(r"id=(.+)", paper_url)
    paper_id = paper_id_match.group(1) if paper_id_match else "unknown"
    
    # Save HTML
    html_filename = os.path.join(HTML_DIR, f"{paper_id}.html")
    try:
        with open(html_filename, "w", encoding="utf-8") as f:
            f.write(html)
        logging.info(f"Saved HTML to {html_filename}")
    except Exception as e:
        logging.error(f"Error saving HTML for {paper_url}: {e}")
    
    # Parse paper info to get PDF URL
    soup = BeautifulSoup(html, "html.parser")
    paper_info = parse_paper_info(soup)
    
    # Download PDF
    if paper_info["pdf_url"]:
        pdf_filename = f"{paper_id}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)
        success = download_pdf(paper_info["pdf_url"], pdf_path)
        if success:
            logging.info(f"Successfully scraped paper: {paper_id}")
    else:
        logging.warning(f"No PDF URL found for {paper_url}.")

def process_papers_parallel_scrape(paper_urls, max_workers=4):
    """Processes multiple papers in parallel for scraping."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for url in paper_urls:
            driver = setup_selenium()
            future = executor.submit(scrape_paper, driver, url)
            futures.append((future, driver))

        for future, driver in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error scraping a paper: {e}")
            finally:
                driver.quit()

def main():
    """Main function to orchestrate scraping."""
    # Read URLs from the urls.txt file
    try:
        with open(URLS_FILE, "r", encoding="utf-8") as f:
            paper_urls = [line.strip() for line in f if line.strip()]
        logging.info(f"Loaded {len(paper_urls)} paper URLs from {URLS_FILE}")
    except Exception as e:
        logging.error(f"Error reading URLs from {URLS_FILE}: {e}")
        return

    # Scrape all papers in parallel
    process_papers_parallel_scrape(paper_urls, max_workers=8)

if __name__ == "__main__":
    main()
