# Northern Neck Grant OCR Workflow

This toolset processes historical grant documents from the Library of Virginia's Northern Neck collection (1690-1729) by:

1. Downloading TIFF images from the Library of Virginia website
2. Converting and rotating them to properly oriented PNG files
3. Using OpenAI's Vision models to OCR the handwritten text
4. Saving the transcribed text as Markdown files

## Setup

### Prerequisites

- Python 3.8+ 
- An OpenAI API key with access to Vision models

### Installation

1. Install required Python packages:

```bash
pip install openai python-dotenv pillow requests beautifulsoup4 tqdm
```

2. Create a `.env` file with your OpenAI API key:

```bash
cp .env.example .env
```

3. Edit the `.env` file and add your OpenAI API key.

## Usage

### Downloading and Converting Grant Images

Run the main workflow script to download TIFFs and convert them to PNGs:

```bash
python fetch_and_ocr_grants.py
```

This script:
- Crawls the Library of Virginia website to find grant volumes
- Downloads TIFF files
- Rotates and converts them to PNG format
- Organizes them in a structured directory layout

In test mode (default), the script only processes a small subset of pages. Edit the constants at the top of the script to process more pages.

### OCR a Single Image

To test OCR on a single PNG file:

```bash
python ocr_single_image.py path/to/image.png
```

This will:
1. Send the image to OpenAI's o4-mini vision model
2. Extract the text using a specialized paleography prompt
3. Save the transcription as a markdown file with appropriate YAML front matter
4. Cache the API response to avoid duplicate requests

You can also specify a custom prompt:

```bash
python ocr_single_image.py path/to/image.png --prompt "Your custom OCR prompt here"
```

## Directory Structure

- `tiff_grants/`: Downloaded TIFF files
- `png_grants/`: Converted and rotated PNG files
- `markdown_grants/`: OCR'd text in Markdown format
- `ocr_cache/`: Cached API responses

## Notes

- OCR quality will vary based on handwriting clarity and image quality
- The script is designed to be rerunnable, skipping files that have already been processed
- The handwriting in these grants is from the 17th-18th century and can be challenging even for modern AI

## License

This project is for research purposes only. The original grant documents are owned by the Library of Virginia. 