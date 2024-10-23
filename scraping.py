import os
import re
import time
import logging
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

# Configure Logging
logging.basicConfig(
    filename='scraper.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Constants
BASE_URL = "https://openreview.net"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DataScraper/1.0; +https://yourdomain.com/)"
}
DOWNLOAD_DIR = "ICLR_Papers_Scrape"
PDF_DIR = os.path.join(DOWNLOAD_DIR, "PDFs")
MARKDOWN_DIR = os.path.join(DOWNLOAD_DIR, "Markdown")
IMAGES_DIR = os.path.join(DOWNLOAD_DIR, "Images")

# Create directories if they don't exist
for directory in [DOWNLOAD_DIR, PDF_DIR, MARKDOWN_DIR, IMAGES_DIR]:
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
    title_tag = soup.find('h2', class_='citation_title')
    paper_info['title'] = title_tag.text.strip() if title_tag else "N/A"

    # Extract Authors
    authors_tag = soup.find('div', class_='forum-authors')
    if authors_tag:
        authors = [author.text.strip() for author in authors_tag.find_all('a')]
        paper_info['authors'] = authors
    else:
        paper_info['authors'] = []

    # Extract Publication Date
    pub_date_tag = soup.find('span', class_='glyphicon-calendar')
    if pub_date_tag and pub_date_tag.parent:
        dates_text = pub_date_tag.parent.text.strip()
        publication_date = re.search(r'Published:\s*(.*?)(?:,|$)', dates_text)
        paper_info['publication_date'] = publication_date.group(1) if publication_date else "N/A"
    else:
        paper_info['publication_date'] = "N/A"

    # Extract Decision
    decision = "N/A"
    decision_sections = soup.find_all('div', class_='note', attrs={'data-id': re.compile('.*')})
    for section in decision_sections:
        heading = section.find('h4')
        if heading and 'Paper Decision' in heading.text:
            decision_field = section.find('strong', string='Decision:')
            if decision_field and decision_field.next_sibling:
                decision = decision_field.next_sibling.strip()
                break
    paper_info['decision'] = decision

    # Extract PDF URL
    pdf_link_tag = soup.find('a', class_='citation_pdf_url')
    if pdf_link_tag and 'href' in pdf_link_tag.attrs:
        pdf_url = pdf_link_tag['href']
        if not pdf_url.startswith('http'):
            pdf_url = BASE_URL + pdf_url
        paper_info['pdf_url'] = pdf_url
    else:
        paper_info['pdf_url'] = None

    return paper_info

def download_pdf(pdf_url, save_path):
    """Downloads the PDF from the given URL to the specified path."""
    try:
        logging.info(f"Downloading PDF: {pdf_url}")
        response = requests.get(pdf_url, headers=HEADERS)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
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
        text = re.sub(r'\s+', ' ', text)
        
        # Improved regex patterns to accurately capture Abstract and Introduction
        abstract_match = re.search(
            r'(?is)abstract\s*(.*?)\s*(?:(introduction|1\.\s*Introduction|2\.\s*Methods|methods|conclusion|related work|acknowledgments|references|$))',
            text
        )
        # introduction_match = re.search(
        #     r'(?is)(introduction|1\.\s*Introduction)\s*(.*?)\s*(?:(conclusion|related work|methods|acknowledgments|references|2\.\s*Methods|$))',
        #     text
        # )
        
        
        introduction_match = re.search(r'(?is)(introduction|1\.\s*Introduction)\s*(.*?)\s*(?:(\n2\s)|$)', text, re.DOTALL)

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
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Saved Markdown to {path}")
    except Exception as e:
        logging.error(f"Error saving Markdown file {filename}: {e}")

def extract_reviewer_responses(soup):
    """Extracts reviewer responses, comments, and other interactions."""
    responses = []

    # Find all notes (reviews, meta-reviews, official comments)
    note_divs = soup.find_all('div', class_='note', attrs={'data-id': re.compile('.*')})

    for note in note_divs:
        # Determine the type of note
        invitation = note.find('span', class_='invitation')
        if not invitation:
            continue
        invitation_type = invitation.text.strip()

        # Extract author
        signatures_span = note.find('span', class_='signatures')
        author = "N/A"
        if signatures_span:
            # The last span usually contains the author
            author_tags = signatures_span.find_all('span')
            if author_tags:
                author = author_tags[-1].text.strip()
            else:
                # Fallback if no span found
                author = signatures_span.text.strip()
        
        # Extract content fields
        content_div = note.find('div', class_='note-content')
        content_dict = {}
        if content_div:
            # Each content field is typically within a div
            content_fields = content_div.find_all('div', recursive=False)
            for field in content_fields:
                # Field name
                field_name_tag = field.find('strong', class_='note-content-field')
                if not field_name_tag:
                    continue
                field_name = field_name_tag.text.strip(':').strip()
                # Field value
                field_value_div = field.find('div', class_='note-content-value')
                field_value_span = field.find('span', class_='note-content-value')
                field_value = ""
                if field_value_div:
                    field_value = md(str(field_value_div)).strip()
                elif field_value_span:
                    field_value = md(str(field_value_span)).strip()
                content_dict[field_name] = field_value

        # If the note has nested replies (official comments by authors), handle them separately
        nested_comments = note.find_all('div', class_='note', attrs={'data-id': re.compile('.*')})
        for comment in nested_comments:
            comment_invitation = comment.find('span', class_='invitation')
            if comment_invitation and 'Official Comment' in comment_invitation.text.strip():
                comment_author = "Authors"
                comment_content_div = comment.find('div', class_='note-content')
                comment_content = md(str(comment_content_div)) if comment_content_div else "N/A"
                responses.append({
                    'type': 'Official Comment',
                    'author': comment_author,
                    'content': {'Comment': comment_content}
                })

        # Avoid duplicating comments by checking if it's already appended
        if not (invitation_type == 'Official Comment' and author == 'Authors'):
            responses.append({
                'type': invitation_type,
                'author': author,
                'content': content_dict
            })

    return responses

def save_reviewer_responses(responses, filename):
    """Saves reviewer responses to a Markdown file."""
    try:
        content = f"## Reviewer Responses\n\n"
        for idx, response in enumerate(responses, 1):
            content += f"### {response['type']} {idx}\n"
            content += f"**Author:** {response['author']}\n\n"
            for field_name, field_value in response['content'].items():
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
        content += f"**Decision:** {paper_info['decision']}\n\n"
        save_markdown(content, filename)
        logging.info(f"Saved metadata to {filename}")
    except Exception as e:
        logging.error(f"Error saving metadata to {filename}: {e}")

def process_paper(driver, paper_url):
    """Processes a single paper: downloads PDF, extracts sections, and scrapes HTML data."""
    logging.info(f"Starting processing for paper: {paper_url}")
    html = fetch_html(driver, paper_url)
    if not html:
        logging.warning(f"Failed to retrieve HTML for {paper_url}. Skipping.")
        return

    soup = BeautifulSoup(html, 'html.parser')
    paper_info = parse_paper_info(soup)
    paper_id_match = re.search(r'id=([A-Za-z0-9]+)', paper_url)
    paper_id = paper_id_match.group(1) if paper_id_match else "unknown"

    # Save metadata
    metadata_filename = f"{paper_id}_metadata.md"
    save_paper_metadata(paper_info, metadata_filename)

    # Download PDF and extract sections
    if paper_info['pdf_url']:
        pdf_filename = f"{paper_id}.pdf"
        pdf_path = os.path.join(PDF_DIR, pdf_filename)
        success = download_pdf(paper_info['pdf_url'], pdf_path)
        if success:
            abstract, introduction = extract_sections_from_pdf(pdf_path)
            abstract_md = convert_to_markdown(abstract, "Abstract")
            introduction_md = convert_to_markdown(introduction, "Introduction")
            combined_md = abstract_md + "\n" + introduction_md
            sections_filename = f"{paper_id}_sections.md"
            save_markdown(combined_md, sections_filename)
    else:
        logging.warning(f"No PDF URL found for {paper_url}. Skipping PDF download and extraction.")

    # Extract reviewer responses
    responses = extract_reviewer_responses(soup)
    if responses:
        responses_filename = f"{paper_id}_responses.md"
        save_reviewer_responses(responses, responses_filename)
    else:
        logging.info(f"No reviewer responses found for {paper_url}.")

    logging.info(f"Completed processing for paper ID: {paper_id}")

def process_papers_parallel(paper_urls, max_workers=4):
    """Processes multiple papers in parallel."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Each thread needs its own Selenium WebDriver
        futures = []
        for url in paper_urls:
            driver = setup_selenium()
            future = executor.submit(process_paper, driver, url)
            futures.append((future, driver))
        
        for future, driver in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error processing a paper: {e}")
            finally:
                driver.quit()

if __name__ == "__main__":
    # List of Paper URLs
    paper_urls = [
        "https://openreview.net/forum?id=KS8mIvetg2",
        "https://openreview.net/forum?id=7Ttk3RzDeu",
        "https://openreview.net/forum?id=ANvmVS2Yr0",
        "https://openreview.net/forum?id=ekeyCgeRfC"
    ]

    # Start parallel processing
    process_papers_parallel(paper_urls, max_workers=8)
