# parser.py

import os
import re
import logging
import csv
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pdfminer.high_level import extract_text
import glob

# Configure Logging
logging.basicConfig(
    filename="parser.log",
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
    "2023": ["Empirical Novelty And Significance", "Technical Novelty And Significance", "Recommendation", "Confidence"],
    "2022": ["Empirical Novelty And Significance", "Technical Novelty And Significance", "Recommendation", "Confidence"],
    "2021": ["Rating", "Confidence"]
}

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

    return paper_info

def extract_sections_from_pdf(pdf_path):
    """Extracts the abstract and introduction from the PDF."""
    try:
        logging.info(f"Extracting sections from PDF: {pdf_path}")
        text = extract_text(pdf_path)

        # Preprocess text to remove page numbers and unwanted paragraphs
        # 1. Remove standalone page numbers (e.g., '1', '2') possibly surrounded by whitespace or newlines
        text = re.sub(r'\n\s*\d+\s*\n', '\n', text)

        # 2. Remove paragraphs containing the word "figures" (case-insensitive)
        # Split the text into paragraphs
        paragraphs = text.split('\n\n')
        cleaned_paragraphs = [para for para in paragraphs if not re.search(r'\bfigures\b', para, re.IGNORECASE)]
        cleaned_text = '\n\n'.join(cleaned_paragraphs)

        # Normalize whitespace
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        # Improved regex patterns to accurately capture Abstract and Introduction
        abstract_match = re.search(
            r'(?i)\babstract\b\s*[:\-]?\s*(.*?)\s*(?=\bintroduction\b|\b1\.\s*Introduction\b|\b\d+\.\s*\w+)',
            cleaned_text
        )
        introduction_match = re.search(
            r'(?i)\bintroduction\b\s*[:\-]?\s*(.*?)\s*(?=\bconclusion\b|\brelated work\b|\bmethods\b|\backnowledgments\b|\breferences\b|\b\d+\.\s*\w+)',
            cleaned_text
        )

        abstract = abstract_match.group(1).strip() if abstract_match else "N/A"
        introduction = introduction_match.group(1).strip() if introduction_match else "N/A"

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
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Saved Markdown to {filename}")
    except Exception as e:
        logging.error(f"Error saving Markdown file {filename}: {e}")

def extract_reviewer_responses(soup, year):
    """Extracts all notes (reviews, meta-reviews, decisions, comments) in order based on the year."""
    responses = []

    # Define metric terms based on the year
    METRIC_TERMS = {
        "2024": ["Soundness", "Presentation", "Contribution", "Rating", "Confidence"],
        "2023": ["Empirical Novelty And Significance", "Technical Novelty And Significance", "Recommendation", "Confidence"],
        "2022": ["Empirical Novelty And Significance", "Technical Novelty And Significance", "Recommendation", "Confidence"],
        "2021": ["Rating", "Confidence"]
    }

    # Get the relevant metrics for the given year
    relevant_metrics = METRIC_TERMS.get(year, [])

    # Find all notes (reviews, meta-reviews, decisions, comments)
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
            author_tags = signatures_span.find_all("span")
            if author_tags:
                author = author_tags[-1].text.strip()
            else:
                author = signatures_span.text.strip()

        # Extract content fields
        content_div = note.find("div", class_="note-content")
        content_dict = {}
        if content_div:
            content_fields = content_div.find_all("div", recursive=False)
            for field in content_fields:
                field_name_tag = field.find("strong", class_="note-content-field")
                if not field_name_tag:
                    continue
                field_name = field_name_tag.text.strip(":").strip()
                field_value_div = field.find("div", class_="note-content-value")
                field_value_span = field.find("span", class_="note-content-value")
                field_value = ""
                if field_value_div:
                    field_value = md(str(field_value_div)).strip()
                elif field_value_span:
                    field_value = md(str(field_value_span)).strip()
                content_dict[field_name] = field_value

        # Determine the note type based on the presence of relevant metrics
        if any(metric in content_dict for metric in relevant_metrics):
            note_type = "Official Review"
        else:
            note_type = invitation_type  # Use the invitation type as the note type

        # Append the note
        responses.append(
            {"type": note_type, "author": author, "content": content_dict}
        )

        # Handle nested comments (e.g., author responses)
        nested_comments = note.find_all(
            "div", class_="note", attrs={"data-id": re.compile(".*")}
        )
        for comment in nested_comments:
            comment_invitation = comment.find("span", class_="invitation")
            if comment_invitation:
                comment_type = comment_invitation.text.strip()
                comment_author_span = comment.find("span", class_="signatures")
                comment_author = "N/A"
                if comment_author_span:
                    author_tags = comment_author_span.find_all("span")
                    if author_tags:
                        comment_author = author_tags[-1].text.strip()
                    else:
                        comment_author = comment_author_span.text.strip()

                comment_content_div = comment.find("div", class_="note-content")
                comment_content_dict = {}
                if comment_content_div:
                    content_fields = comment_content_div.find_all("div", recursive=False)
                    for field in content_fields:
                        field_name_tag = field.find("strong", class_="note-content-field")
                        if not field_name_tag:
                            continue
                        field_name = field_name_tag.text.strip(":").strip()
                        field_value_div = field.find("div", class_="note-content-value")
                        field_value_span = field.find("span", class_="note-content-value")
                        field_value = ""
                        if field_value_div:
                            field_value = md(str(field_value_div)).strip()
                        elif field_value_span:
                            field_value = md(str(field_value_span)).strip()
                        comment_content_dict[field_name] = field_value

                responses.append(
                    {"type": comment_type, "author": comment_author, "content": comment_content_dict}
                )

    return responses

def save_reviewer_responses(responses, filename):
    """Saves reviewer responses to a Markdown file, maintaining the sequential order."""
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

def save_markdown(content, filename):
    """Saves the given content to a Markdown file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Saved Markdown to {filename}")
    except Exception as e:
        logging.error(f"Error saving Markdown file {filename}: {e}")

def parse_paper(paper_id, year):
    """Parses the scraped HTML and PDF to extract metadata, sections, and reviewer responses."""
    year_download_dir = os.path.join(BASE_DOWNLOAD_DIR, f"iclr_{year}")
    html_filename = os.path.join(year_download_dir, "HTML", f"{paper_id}.html")
    pdf_path = os.path.join(year_download_dir, "PDF", f"{paper_id}.pdf")
    markdown_dir = os.path.join(year_download_dir, "Markdown")

    # Create Markdown directory if it doesn't exist
    os.makedirs(markdown_dir, exist_ok=True)

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
    metadata_filename = os.path.join(markdown_dir, f"{paper_id}_metadata.md")
    save_paper_metadata(paper_info, metadata_filename)

    # Extract sections from PDF
    if os.path.exists(pdf_path):
        abstract, introduction = extract_sections_from_pdf(pdf_path)
        abstract_md = convert_to_markdown(abstract, "Abstract")
        introduction_md = convert_to_markdown(introduction, "Introduction")
        combined_md = abstract_md + "\n" + introduction_md
        sections_filename = os.path.join(markdown_dir, f"{paper_id}_sections.md")
        save_markdown(combined_md, sections_filename)
    else:
        logging.warning(f"PDF not found for paper ID {paper_id}. Skipping section extraction.")

    # Extract reviewer responses
    responses = extract_reviewer_responses(soup, year)  # Pass the year here
    if responses:
        responses_filename = os.path.join(markdown_dir, f"{paper_id}_responses.md")
        save_reviewer_responses(responses, responses_filename)
    else:
        logging.info(f"No reviewer responses found for paper ID {paper_id}.")

    logging.info(f"Completed parsing for paper ID: {paper_id} (Year: {year})")

def aggregate_csv(csv_filename="decisions_and_scores.csv"):
    """Aggregates decisions and scores from all *_responses.md files into a CSV."""
    csv_path = os.path.join(BASE_DOWNLOAD_DIR, csv_filename)
    fieldnames = [
        "paperid", "title", "year", "decision",
        "soundness", "presentation", "contribution",
        "correctness", "technical_novelty_and_significance",
        "empirical_novelty_and_significance",
        "review_rating", "recommendation",
        "confidence"
    ]

    try:
        with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            # Iterate over each year directory
            for year in METRICS_BY_YEAR.keys():
                year_download_dir = os.path.join(BASE_DOWNLOAD_DIR, f"iclr_{year}")
                responses_files = glob.glob(os.path.join(year_download_dir, "Markdown", "*_responses.md"))
                for resp_file in responses_files:
                    paper_id = os.path.basename(resp_file).replace("_responses.md", "")
                    metadata_file = os.path.join(year_download_dir, "Markdown", f"{paper_id}_metadata.md")
                    
                    # Read metadata to get title
                    try:
                        with open(metadata_file, "r", encoding="utf-8") as f:
                            metadata = f.read()
                        title_match = re.search(r"# (.+)", metadata)
                        title = title_match.group(1).strip() if title_match else "N/A"
                    except Exception as e:
                        logging.error(f"Error reading metadata for {paper_id}: {e}")
                        title = "N/A"
                    
                    # Initialize metrics
                    decision = "N/A"
                    metrics = {
                        "soundness": [],
                        "presentation": [],
                        "contribution": [],
                        "correctness": [],
                        "technical_novelty_and_significance": [],
                        "empirical_novelty_and_significance": [],
                        "review_rating": [],
                        "recommendation": [],
                        "confidence": []
                    }
                    
                    # Read responses to get decision and reviews
                    try:
                        with open(resp_file, "r", encoding="utf-8") as f:
                            responses_md = f.read()
                        
                        # Split the responses_md into sections based on headers
                        sections = re.split(r"^### ", responses_md, flags=re.MULTILINE)
                        for section in sections:
                            if not section.strip():
                                continue
                            header_match = re.match(r"(\w+.*?)\n", section)
                            if header_match:
                                header = header_match.group(1).strip()
                                content = section[header_match.end():]
                                if header.startswith("Decision"):
                                    # Extract decision
                                    decision_match = re.search(r"\*\*Decision:\*\*\s*\n*(.+?)(?:\n\n|\Z)", content, re.DOTALL)
                                    decision = decision_match.group(1).strip() if decision_match else "N/A"
                                elif header.startswith("Official Review"):
                                    # Extract review fields based on year
                                    for metric in METRICS_BY_YEAR[year]:
                                        metric_key = metric.lower().replace(" ", "_").replace("and_", "_and_")
                                        pattern = rf"\*\*{re.escape(metric)}:\*\*\s*(\d+)"
                                        match = re.search(pattern, content, re.IGNORECASE)
                                        if match:
                                            metrics[metric_key].append(match.group(1))
                                        else:
                                            metrics[metric_key].append("N/A")
                                else:
                                    # Other types (Meta Review, Comments, etc.) are ignored for CSV
                                    pass
                        
                    except Exception as e:
                        logging.error(f"Error reading responses for {paper_id}: {e}")
                    
                    # Compile row data
                    row = {
                        "paperid": paper_id,
                        "title": title,
                        "year": year,
                        "decision": decision,
                        "soundness": ','.join(metrics["soundness"]) if metrics["soundness"] else "N/A",
                        "presentation": ','.join(metrics["presentation"]) if metrics["presentation"] else "N/A",
                        "contribution": ','.join(metrics["contribution"]) if metrics["contribution"] else "N/A",
                        "correctness": ','.join(metrics["correctness"]) if metrics["correctness"] else "N/A",
                        "technical_novelty_and_significance": ','.join(metrics["technical_novelty_and_significance"]) if metrics["technical_novelty_and_significance"] else "N/A",
                        "empirical_novelty_and_significance": ','.join(metrics["empirical_novelty_and_significance"]) if metrics["empirical_novelty_and_significance"] else "N/A",
                        "review_rating": ','.join(metrics["review_rating"]) if metrics["review_rating"] else "N/A",
                        "recommendation": ','.join(metrics["recommendation"]) if metrics["recommendation"] else "N/A",
                        "confidence": ','.join(metrics["confidence"]) if metrics["confidence"] else "N/A"
                    }
                    
                    # Write to CSV
                    writer.writerow(row)
        
        logging.info(f"Aggregated CSV saved to {csv_path}")
    except Exception as e:
        logging.error(f"Error creating CSV file {csv_path}: {e}")

def process_papers_parallel_parse(papers, max_workers=4):
    """Processes multiple papers in parallel for parsing."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for paper_id, year in papers:
            future = executor.submit(parse_paper, paper_id, year)
            futures.append(future)

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logging.error(f"Error parsing a paper: {e}")

def main():
    """Main function to orchestrate parsing of HTML and PDFs."""
    all_papers = []
    
    # Iterate over each year directory
    for year in METRICS_BY_YEAR.keys():
        markdown_dir = os.path.join(BASE_DOWNLOAD_DIR, f"iclr_{year}", "Markdown")
        html_dir = os.path.join(BASE_DOWNLOAD_DIR, f"iclr_{year}", "HTML")
        pdf_dir = os.path.join(BASE_DOWNLOAD_DIR, f"iclr_{year}", "PDF")
        
        # Ensure Markdown directory exists
        os.makedirs(markdown_dir, exist_ok=True)
        
        # Get all HTML files
        html_files = glob.glob(os.path.join(html_dir, "*.html"))
        for html_file in html_files:
            paper_id = os.path.basename(html_file).replace(".html", "")
            all_papers.append((paper_id, year))
    
    logging.info(f"Total papers to parse: {len(all_papers)}")
    
    # Parse all papers in parallel
    process_papers_parallel_parse(all_papers, max_workers=8)
    
    # Aggregate all data into CSV
    aggregate_csv()

if __name__ == "__main__":
    main()
