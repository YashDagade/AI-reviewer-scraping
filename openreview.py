# %% [markdown]
# # Scraper for ICLR Papers through OpenReview

# %%
import os
import re
import time
import logging
import csv
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pdfminer.high_level import extract_text
from webdriver_manager.chrome import ChromeDriverManager
import glob

# %%
# Setting up

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
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0; +https://yourdomain.com/)"
}
DOWNLOAD_DIR = "data/iclr_2024"
HTML_DIR = os.path.join(DOWNLOAD_DIR, "HTML")
PDF_DIR = os.path.join(DOWNLOAD_DIR, "PDF")
MARKDOWN_DIR = os.path.join(DOWNLOAD_DIR, "Markdown")
IMAGES_DIR = os.path.join(DOWNLOAD_DIR, "Image")

# Create directories if they don't exist
for directory in [DOWNLOAD_DIR, HTML_DIR, PDF_DIR, MARKDOWN_DIR, IMAGES_DIR]:
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

def fetch_html(driver, url, timeout=30):
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

def extract_sections_from_pdf(pdf_path):
    """Extracts the abstract and introduction from the PDF."""
    try:
        logging.info(f"Extracting sections from PDF: {pdf_path}")
        text = extract_text(pdf_path)
        # Normalize whitespace
        text = re.sub(r"\s+", " ", text)

        # Improved regex patterns to accurately capture Abstract and Introduction
        abstract_match = re.search(
            r"(?is)abstract\s*(.*?)\s*(?:(introduction|1\.\s*Introduction|2\.\s*Methods|methods|conclusion|related work|acknowledgments|references|$))",
            text
        )
        introduction_match = re.search(
            r"(?is)(introduction|1\.\s*Introduction)\s*(.*?)\s*(?:(conclusion|related work|methods|acknowledgments|references|2\.\s*Methods|$))",
            text
        )

        abstract = abstract_match.group(1).strip() if abstract_match else "N/A"
        introduction = introduction_match.group(2).strip() if introduction_match else "N/A"

        logging.info(f"Extracted Abstract and Introduction from {pdf_path}")
        return abstract, introduction
    except Exception as e:
        logging.error(f"Error extracting text from PDF {pdf_path}: {e}")
        return "N/A", "N/A"

def convert_to_markdown(text, header):
    """Converts plain text to Markdown with a specified header."""
    if text == "N/A":
        markdown = f"## {header}\n\nN/A\n"
    else:
        markdown = f"## {header}\n\n{text}\n"
    return markdown

def save_markdown(content, filename):
    """Saves the given content to a Markdown file."""
    try:
        path = os.path.join(MARKDOWN_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Saved Markdown to {path}")
    except Exception as e:
        logging.error(f"Error saving Markdown file {filename}: {e}")

def extract_reviewer_responses(soup):
    """Extracts reviewer responses, comments, and other interactions."""
    responses = []

    # Find all notes (reviews, meta-reviews, official comments)
    note_divs = soup.find_all("div", class_="note", attrs={"data-id": re.compile(".*")})

    for note in note_divs:
        # Determine the type of note
        invitation = note.find("span", class_="invitation")
        if not invitation:
            continue
        invitation_type = invitation.text.strip()

        # Extract author
        signatures_span = note.find("span", class_="signatures")
        author = "N/A"
        if signatures_span:
            # The last span usually contains the author
            author_tags = signatures_span.find_all("span")
            if author_tags:
                author = author_tags[-1].text.strip()
            else:
                # Fallback if no span found
                author = signatures_span.text.strip()

        # Extract content fields
        content_div = note.find("div", class_="note-content")
        content_dict = {}
        if content_div:
            # Each content field is typically within a div
            content_fields = content_div.find_all("div", recursive=False)
            for field in content_fields:
                # Field name
                field_name_tag = field.find("strong", class_="note-content-field")
                if not field_name_tag:
                    continue
                field_name = field_name_tag.text.strip(":").strip()
                # Field value
                field_value_div = field.find("div", class_="note-content-value")
                field_value_span = field.find("span", class_="note-content-value")
                field_value = ""
                if field_value_div:
                    field_value = md(str(field_value_div)).strip()
                elif field_value_span:
                    field_value = md(str(field_value_span)).strip()
                content_dict[field_name] = field_value

        # If the note has nested replies (official comments by authors), handle them separately
        nested_comments = note.find_all(
            "div", class_="note", attrs={"data-id": re.compile(".*")}
        )
        for comment in nested_comments:
            comment_invitation = comment.find("span", class_="invitation")
            if (
                comment_invitation
                and "Official Comment" in comment_invitation.text.strip()
            ):
                comment_author = "Authors"
                comment_content_div = comment.find("div", class_="note-content")
                comment_content = (
                    md(str(comment_content_div)) if comment_content_div else "N/A"
                )
                responses.append(
                    {
                        "type": "Official Comment",
                        "author": comment_author,
                        "content": {"Comment": comment_content},
                    }
                )

        # Avoid duplicating comments by checking if it's already appended
        if not (invitation_type == "Official Comment" and author == "Authors"):
            # Check if it's an actual review by checking for 'Soundness' field
            if "Soundness" in content_dict:
                responses.append(
                    {"type": invitation_type, "author": author, "content": content_dict}
                )

    return responses

def save_reviewer_responses(responses, filename):
    """Saves reviewer responses to a Markdown file."""
    try:
        content = f"## Reviewer Responses\n\n"
        for idx, response in enumerate(responses, 1):
            content += f"### {response['type']} {idx}\n"
            content += f"**Author:** {response['author']}\n\n"
            for field_name, field_value in response["content"].items():
                content += f"**{field_name}:**\n{field_value}\n\n"
            content += "\n"
        save_markdown(content, filename)
        logging.info(f"Saved reviewer responses to {filename}")
    except Exception as e:
        logging.error(f"Error saving reviewer responses to {filename}: {e}")

def save_paper_metadata(paper_info, filename):
    """Saves paper metadata to a Markdown file."""
    try:
        content = f"# {paper_info['title']}\n\n"
        content += f"**Authors:** {', '.join(paper_info['authors'])}\n\n"
        content += f"**Publication Date:** {paper_info['publication_date']}\n\n"
        save_markdown(content, filename)
        logging.info(f"Saved metadata to {filename}")
    except Exception as e:
        logging.error(f"Error saving metadata to {filename}: {e}")

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

def parse_paper(paper_id):
    """Parses the scraped HTML and PDF to extract metadata, sections, and reviewer responses."""
    html_filename = os.path.join(HTML_DIR, f"{paper_id}.html")
    pdf_path = os.path.join(PDF_DIR, f"{paper_id}.pdf")
    
    # Read HTML
    try:
        with open(html_filename, "r", encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "html.parser")
    except Exception as e:
        logging.error(f"Error reading HTML file {html_filename}: {e}")
        return
    
    # Parse paper info
    paper_info = parse_paper_info(soup)
    
    # Save metadata
    metadata_filename = f"{paper_id}_metadata.md"
    save_paper_metadata(paper_info, metadata_filename)
    
    # Extract sections from PDF
    if os.path.exists(pdf_path):
        abstract, introduction = extract_sections_from_pdf(pdf_path)
        abstract_md = convert_to_markdown(abstract, "Abstract")
        introduction_md = convert_to_markdown(introduction, "Introduction")
        combined_md = abstract_md + "\n" + introduction_md
        sections_filename = f"{paper_id}_sections.md"
        save_markdown(combined_md, sections_filename)
    else:
        logging.warning(f"PDF not found for paper ID {paper_id}. Skipping section extraction.")
    
    # Extract reviewer responses
    responses = extract_reviewer_responses(soup)
    if responses:
        responses_filename = f"{paper_id}_responses.md"
        save_reviewer_responses(responses, responses_filename)
    else:
        logging.info(f"No reviewer responses found for paper ID {paper_id}.")
    
    logging.info(f"Completed parsing for paper ID: {paper_id}")

def aggregate_csv(csv_filename="decisions_and_scores.csv"):
    """Aggregates decisions and scores from all *_responses.md files into a CSV."""
    csv_path = os.path.join(DOWNLOAD_DIR, csv_filename)
    fieldnames = ["paperid", "title", "decision", "soundness", "presentation", "contribution", "review_rating", "confidence"]

    try:
        with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Get all responses.md files
            responses_files = glob.glob(os.path.join(MARKDOWN_DIR, "*_responses.md"))
            for resp_file in responses_files:
                paper_id = os.path.basename(resp_file).replace("_responses.md", "")
                metadata_file = os.path.join(MARKDOWN_DIR, f"{paper_id}_metadata.md")
                
                # Read metadata to get title
                try:
                    with open(metadata_file, "r", encoding="utf-8") as f:
                        metadata = f.read()
                    title_match = re.search(r"# (.+)", metadata)
                    title = title_match.group(1).strip() if title_match else "N/A"
                except Exception as e:
                    logging.error(f"Error reading metadata for {paper_id}: {e}")
                    title = "N/A"
                
                # Read responses to get decision and reviews
                try:
                    with open(resp_file, "r", encoding="utf-8") as f:
                        responses = f.read()
                    
                    # Extract Decision
                    decision_match = re.search(
                        r"\*\*Decision:\*\*\s*\n*(.+)",
                        responses,
                        re.IGNORECASE
                    )
                    decision = decision_match.group(1).strip() if decision_match else "N/A"
                    
                    # Extract Official Reviews
                    # Find all '### Official Review X' blocks
                    official_reviews = re.findall(
                        r"### Official Review \d+.*?\*\*Author:\*\*.*?\n\n(.*?)(?=###|\Z)",
                        responses,
                        re.DOTALL
                    )
                    
                    soundness_list = []
                    presentation_list = []
                    contribution_list = []
                    rating_list = []
                    confidence_list = []
                    
                    for review in official_reviews:
                        # Extract individual fields
                        soundness = re.search(r"\*\*Soundness:\*\*\s*(\d+)", review, re.IGNORECASE)
                        presentation = re.search(r"\*\*Presentation:\*\*\s*(\d+)", review, re.IGNORECASE)
                        contribution = re.search(r"\*\*Contribution:\*\*\s*(\d+)", review, re.IGNORECASE)
                        rating = re.search(r"\*\*Rating:\*\*\s*(\d+)", review, re.IGNORECASE)
                        confidence = re.search(r"\*\*Confidence:\*\*\s*(\d+)", review, re.IGNORECASE)
                        
                        soundness_list.append(soundness.group(1) if soundness else "N/A")
                        presentation_list.append(presentation.group(1) if presentation else "N/A")
                        contribution_list.append(contribution.group(1) if contribution else "N/A")
                        rating_list.append(rating.group(1) if rating else "N/A")
                        confidence_list.append(confidence.group(1) if confidence else "N/A")
                    
                except Exception as e:
                    logging.error(f"Error reading responses for {paper_id}: {e}")
                    decision = "N/A"
                    soundness_list = []
                    presentation_list = []
                    contribution_list = []
                    rating_list = []
                    confidence_list = []
                
                # Compile row data
                row = {
                    "paperid": paper_id,
                    "title": title,
                    "decision": decision,
                    "soundness": soundness_list,
                    "presentation": presentation_list,
                    "contribution": contribution_list,
                    "review_rating": rating_list,
                    "confidence": confidence_list
                }
                
                # Convert lists to JSON-like string representations
                row["soundness"] = str(row["soundness"])
                row["presentation"] = str(row["presentation"])
                row["contribution"] = str(row["contribution"])
                row["review_rating"] = str(row["review_rating"])
                row["confidence"] = str(row["confidence"])
                
                # Write to CSV
                writer.writerow(row)
        
        logging.info(f"Aggregated CSV saved to {csv_path}")
    except Exception as e:
        logging.error(f"Error creating CSV file {csv_path}: {e}")




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

def process_all_papers_parsing():
    """Parses all scraped papers."""
    html_files = glob.glob(os.path.join(HTML_DIR, "*.html"))
    for html_file in html_files:
        paper_id = os.path.basename(html_file).replace(".html", "")
        parse_paper(paper_id)

def run_aggregation():
    """Runs the CSV aggregation after parsing."""
    aggregate_csv()

def get_paper_urls_from_page(driver, page_url):
    """Extract all unique paper URLs from the given OpenReview page."""
    driver.get(page_url)
    time.sleep(3)  # Give some time for page to load (adjust as necessary)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    paper_links = soup.find_all("a", href=True)

    # Filter out URLs with '&noteId=' and ensure they contain 'forum?id='
    paper_urls = [
        link["href"]
        for link in paper_links
        if "forum?id=" in link["href"] and "&noteId=" not in link["href"]
    ]

    return paper_urls

def url_getter():
    base_url = "https://openreview.net/group?id=ICLR.cc/2024/Conference"  # The URL of the OpenReview ICLR page
    driver = setup_selenium()

    all_paper_urls = []

    # Modify the range as needed to scrape multiple pages
    for page_number in range(1):
        page_url = f"{base_url}&page={page_number}"
        paper_urls = get_paper_urls_from_page(driver, page_url)
        all_paper_urls.extend(paper_urls)

    driver.quit()

    # Create a list with the desired format
    unique_urls = list(set(all_paper_urls))
    # For prototyping, limit to first 5 papers
    formatted_urls = [f"https://openreview.net{url}" for url in unique_urls[:5]]

    return formatted_urls

# %%
# Experimenting with the scraper

# Initial list of paper URLs (you can comment this out if using url_getter)
# paper_urls = [
#     "https://openreview.net/forum?id=KS8mIvetg2",
#     "https://openreview.net/forum?id=7Ttk3RzDeu",
#     "https://openreview.net/forum?id=ANvmVS2Yr0",
#     "https://openreview.net/forum?id=ekeyCgeRfC",
# ]

# Alternatively, get paper URLs from the OpenReview page
paper_urls = url_getter()
print('\n'.join(paper_urls))
process_papers_parallel_scrape(paper_urls, max_workers=8)

# %%
# After scraping, parse all papers and aggregate CSV
process_all_papers_parsing()
aggregate_csv()
