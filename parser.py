# parser.py

import os
import re
import logging
import csv
import glob
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from pdfminer.high_level import extract_text

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
DOWNLOAD_DIR = "data/iclr_2024"
HTML_DIR = os.path.join(DOWNLOAD_DIR, "HTML")
PDF_DIR = os.path.join(DOWNLOAD_DIR, "PDF")
MARKDOWN_DIR = os.path.join(DOWNLOAD_DIR, "Markdown")
CSV_FILE = os.path.join(DOWNLOAD_DIR, "decisions_and_scores.csv")

# Create directories if they don't exist
for directory in [DOWNLOAD_DIR, HTML_DIR, PDF_DIR, MARKDOWN_DIR]:
    os.makedirs(directory, exist_ok=True)

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
    """Extracts all notes (reviews, meta-reviews, decisions, comments) in order."""
    responses = []

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

        # Determine the note type
        if "Soundness" in content_dict:
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

def aggregate_csv(csv_filename=CSV_FILE):
    """Aggregates decisions and scores from all *_responses.md files into a CSV."""
    csv_path = csv_filename
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
                
                # Initialize lists
                decision = "N/A"
                soundness_list = []
                presentation_list = []
                contribution_list = []
                rating_list = []
                confidence_list = []
                
                # Read responses to get decision and reviews
                try:
                    with open(resp_file, "r", encoding="utf-8") as f:
                        responses_md = f.read()
                    
                    # Split the responses_md into sections
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
                                # Extract review fields
                                soundness = re.search(r"\*\*Soundness:\*\*\s*(\d+)", content, re.IGNORECASE)
                                presentation = re.search(r"\*\*Presentation:\*\*\s*(\d+)", content, re.IGNORECASE)
                                contribution = re.search(r"\*\*Contribution:\*\*\s*(\d+)", content, re.IGNORECASE)
                                rating = re.search(r"\*\*Rating:\*\*\s*(\d+)", content, re.IGNORECASE)
                                confidence = re.search(r"\*\*Confidence:\*\*\s*(\d+)", content, re.IGNORECASE)
                                
                                soundness_list.append(soundness.group(1) if soundness else "N/A")
                                presentation_list.append(presentation.group(1) if presentation else "N/A")
                                contribution_list.append(contribution.group(1) if contribution else "N/A")
                                rating_list.append(rating.group(1) if rating else "N/A")
                                confidence_list.append(confidence.group(1) if confidence else "N/A")
                            else:
                                # Other types, ignore for CSV
                                pass
                    
                except Exception as e:
                    logging.error(f"Error reading responses for {paper_id}: {e}")
                
                # Compile row data
                row = {
                    "paperid": paper_id,
                    "title": title,
                    "decision": decision,
                    "soundness": str(soundness_list),
                    "presentation": str(presentation_list),
                    "contribution": str(contribution_list),
                    "review_rating": str(rating_list),
                    "confidence": str(confidence_list)
                }
                
                # Write to CSV
                writer.writerow(row)
        
        logging.info(f"Aggregated CSV saved to {csv_path}")
    except Exception as e:
        logging.error(f"Error creating CSV file {csv_path}: {e}")

def main():
    """Main function to orchestrate parsing and aggregation."""
    # Get all HTML files
    html_files = glob.glob(os.path.join(HTML_DIR, "*.html"))
    logging.info(f"Found {len(html_files)} HTML files to parse.")

    # Parse each paper
    for html_file in html_files:
        paper_id = os.path.basename(html_file).replace(".html", "")
        parse_paper(paper_id)
    
    # Aggregate all data into CSV
    aggregate_csv()

if __name__ == "__main__":
    main()
