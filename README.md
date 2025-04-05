<h1 align=center>Little Falls, VA Website</h1> 
<p align=center>The Little Falls, VA website advocates for the renaming of Falls Church, Virginia to Little Falls. It's built on Hugo framework using the Vex Hugo theme. </p>
<h2 align="center"> <a target="_blank" href="https://littlefallsva.com" rel="nofollow">Website</a></h2>

<p align=center>
  <a href="https://github.com/ryanmio/Little-Falls-VA">
    <img src="https://img.shields.io/github/license/ryanmio/Little-Falls-VA" alt="license"></a>

  <img src="https://img.shields.io/github/languages/code-size/ryanmio/Little-Falls-VA" alt="code size">

  <a href="https://github.com/ryanmio/Little-Falls-VA/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/ryanmio/Little-Falls-VA" alt="contributors"></a>

</p>

---

<p align="center">
  <img src="https://littlefallsva.com/images/screenshot.png" alt="website screenshot" width="100%">
</p>

---

### Prerequisites

- [Hugo](https://gohugo.io/installation/) (v0.111.3 or higher)
- [Node.js](https://nodejs.org/en/download/) (for npm packages)

### Getting Started

1. Clone this repository
2. Install dependencies with `npm install`
3. Run the development server with `npm run dev`
4. View the site at [http://localhost:1313](http://localhost:1313)

### Building for Production

To build the site for production:

```bash
npm run build
```

The built site will be in the `public` directory.

## Deployment

This site is deployed on Netlify. Any push to the main branch will trigger a new build and deployment.

## Citation Style Guide

When writing research articles, use the following citation shortcode format:

```
{{< cite url="URL" title="Full Title of Source" >}}
```

### Examples:

Single citation:
```markdown
Falls Church became a microcosm of Southern defiance {{< cite url="https://example.com/article#:~:text=relevant,text,here" title="Article Title - Publication Name" >}}.
```

Multiple citations in sequence:
```markdown
This fact is supported by multiple sources {{< cite url="https://example1.com" title="First Source" >}} {{< cite url="https://example2.com" title="Second Source" >}}.
```

### Guidelines:

1. Always include both the `url` and `title` parameters
2. For URLs with text fragments (#:~:text=), include the full URL to reference specific quotes
3. Place citations immediately after the relevant text, before any punctuation
4. For multiple citations supporting the same statement, place them together without spacing
5. Citations will render as clickable chips showing the domain name in uppercase
6. Hovering over a citation will reveal the full title
7. Citations in the Sources section should follow the same format

### Best Practices:

- Be specific with text fragments in URLs to point to exact quotes
- Use descriptive titles that include both the article name and publication
- Place citations logically to clearly indicate which statements they support
- When citing multiple sources, order them by relevance or chronologically
- Include a Sources section at the end of each article listing all citations 

# Falls Church Research Tools

This repository contains tools to help with historical research about Falls Church, Virginia.

## PDF Extraction Tools

These scripts help extract text from PDF documents and add metadata front matter.

### Quick Reference for PDF Text Extraction

#### Script Files:
- `extract_pdf_text.py`: Basic extraction with limited OCR (first 30 pages)
- `extract_full_pdf.py`: Advanced extraction with batch processing for large PDFs

#### Basic Usage:
```bash
# Process a specific PDF with OCR for all pages:
python3 extract_full_pdf.py --pdf "YourPDFFile.pdf" --ocr

# Process a specific page range (for large PDFs):
python3 extract_full_pdf.py --pdf "YourPDFFile.pdf" --ocr --start-page 0 --max-pages 60

# Process the next batch:
python3 extract_full_pdf.py --pdf "YourPDFFile.pdf" --ocr --start-page 60 --max-pages 60
```

#### Script Requirements:
- Python 3.9+
- Tesseract OCR (`brew install tesseract`)
- Poppler (`brew install poppler`)
- Python packages: pytesseract, pdf2image, pdfminer.six

#### Installation:
```bash
# Install required system dependencies
brew install tesseract poppler

# Install required Python packages
python3 -m pip install pytesseract pdf2image pdfminer.six
```

## IIIF Manifest Processing Tool

This script processes IIIF manifest URLs from digital libraries (such as the Mary Riley Styles Public Library) and creates markdown files with metadata and image information.

### Features:
- Extracts comprehensive metadata from IIIF manifests
- Creates markdown files with structured front matter
- Includes links to original images and manifests
- Uses descriptive titles for filenames
- Provides placeholders for adding historical significance notes

### Basic Usage:
```bash
# Process a single IIIF manifest URL
python3 process_iiif_manifest.py "https://iiif.quartexcollections.com/mrspl/iiif/e3970652-8b7e-40e9-a9c9-d6dde46c2b42/manifest"

# Process multiple IIIF manifest URLs
python3 process_iiif_manifest.py "URL1" "URL2" "URL3"

# Process a list of URLs from a file
python3 process_iiif_manifest.py $(cat manifest_urls.txt)
```

### Output:
The script creates markdown files in the `.research/images/` directory with:
- Front matter containing all available metadata
- A description section
- A complete metadata section listing all fields
- Direct links to the full-resolution image
- Links to the original IIIF manifest
- A section for adding historical significance notes

### Metadata Fields:
The script extracts and includes these fields in the front matter when available:
- `title`: The title of the image
- `date`: The date of the image
- `subject`: The subject(s) of the image
- `creator`: The creator/photographer
- `location`: The place where the image was taken
- `format`: The format of the original (e.g., Photographs)
- `source`: The collection source
- `identifier`: The unique identifier
- `description`: A description of the image
- `color`: Color information (b/w or color)
- `dimensions`: The dimensions of the original
- `digitized`: Always set to True
- `manifest_url`: The URL of the IIIF manifest
- `image_url`: The URL to the full-resolution image

### Requirements:
- Python 3.6+
- Python packages: requests

### Installation:
```bash
# Install required Python packages
python3 -m pip install requests
```

## Prompt Template for AI Assistant

```
I need help extracting text from historical PDF documents. I have the following PDFs:

[List your PDFs here]

I've previously used scripts called extract_pdf_text.py and extract_full_pdf.py to extract text from PDFs and add front matter.

The scripts work by:
1. Attempting standard PDF text extraction first
2. Using OCR (Tesseract) if standard extraction fails
3. Processing large documents in batches (10 pages at a time)
4. Adding metadata front matter to the output markdown files

I'd like to extract all pages from [specific PDF] and add the following front matter:
- title: "[Title]"
- creator: "[Creator]"
- date: "[Date]"
- format: "[Format]"
- subject: "[Subject]"
- identifier: "[Identifier]"
- source: "[Source URL]"

Can you help me:
1. Update the script if needed
2. Run the extraction process
3. Combine the output into a single markdown file with proper front matter
```

## IIIF Manifest Processing Prompt

```
I need to create markdown files with metadata from these IIIF manifest URLs:

[List your IIIF manifest URLs here]

I've previously used a script called process_iiif_manifest.py that:
1. Extracts metadata from IIIF manifests
2. Creates markdown files with detailed front matter
3. Includes links to the original images and manifests
4. Creates descriptive filenames based on the title

Can you help me:
1. Process these manifest URLs
2. Organize the resulting markdown files in my .research/images/ directory
3. Check for any errors or missing metadata
``` 