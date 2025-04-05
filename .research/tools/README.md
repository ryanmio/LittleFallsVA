# Little Falls VA Research Tools

This directory contains tools used for gathering, processing, and organizing research materials for the Little Falls VA renaming initiative.

## Available Tools

### Web Scraping

- **firecrawl-scraper.sh**: Bash script that uses the Firecrawl API to scrape web pages and convert them to markdown format. Useful for collecting articles and historical references from websites related to Falls Church history.

### PDF Processing

- **extract_full_pdf.py**: Python script that extracts text from PDFs, including support for OCR on scanned documents. Creates markdown files with proper front matter from PDF content.
- **extract_pdf_text.py**: Lightweight script for basic PDF text extraction without full document processing.

### Digital Collections Processing

- **process_iiif_manifest.py**: Processes IIIF manifests from digital collections to extract metadata and image information. Creates markdown files with structured information about historical images and documents.
- **batch_process_manifests.py**: Batch processor for handling multiple IIIF manifests concurrently. Uses threading to efficiently process collections of digital assets.

### Markdown Utilities

- **add-frontmatter.sh**: Adds consistent front matter to markdown files, including title, author, date, source URL, and automatically extracted topics based on content.

## Usage Examples

### Web Scraping

```bash
./firecrawl-scraper.sh
```

### PDF Processing

```bash
python extract_full_pdf.py --pdf "path/to/document.pdf" 
# With OCR
python extract_full_pdf.py --pdf "path/to/document.pdf" --ocr
```

### Digital Collection Processing

```bash
python process_iiif_manifest.py "https://iiif.library.example.org/manifest/12345.json"
```

```bash
python batch_process_manifests.py --file manifest_urls.txt --workers 4
```

### Adding Front Matter

```bash
./add-frontmatter.sh file.md "Article Title" "Author Name" "2024-03-26" "https://example.com/article"
```

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - pdfminer.six
  - pytesseract (for OCR)
  - pdf2image (for OCR)
- Bash shell
- curl

## Note on API Keys

Some tools like the Firecrawl scraper require API keys. These should be set within the scripts or as environment variables before use.
