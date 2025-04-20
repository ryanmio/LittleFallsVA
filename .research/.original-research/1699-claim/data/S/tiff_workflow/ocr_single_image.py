#!/usr/bin/env python3
"""
OCR Single Image - Script to test OpenAI Vision model OCR on grant images

This script takes a single PNG file from the png_grants directory,
sends it to OpenAI's GPT-4o-mini model for OCR, and saves the transcription
as markdown.
"""

import os
import sys
import base64
import json
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file if present
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check for API key
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY not found in environment variables or .env file")
    sys.exit(1)

# Constants
MARKDOWN_DIR = Path('./markdown_grants')
CACHE_DIR = Path('./ocr_cache')

def encode_image(image_path):
    """Convert image to base64 encoding for API request"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def ocr_image_with_openai(image_path, prompt=None):
    """
    Use OpenAI's GPT-4o-mini model to OCR the given image
    
    Args:
        image_path: Path to the PNG image
        prompt: Optional custom prompt to use
        
    Returns:
        Transcribed text from the image
    """
    # Default prompt for historical handwritten documents
    if prompt is None:
        prompt = """
You are a professional paleographer specializing in 17th and 18th century English handwriting.

Please transcribe all text in this image of a historical grant document.

Guidelines:
1. Maintain original spelling, capitalization, and punctuation
2. Organize by columns - the page has two columns
3. For each column, preserve the line breaks as they appear
4. Expand common abbreviations only when unambiguous, marking expansions with [brackets]
5. Indicate unclear text with [?]
6. Include page numbers or annotations if visible
7. Do not modernize the text
8. Use "[...]" to indicate text that is cut off or illegible due to damage

Please start with "### Left Column" and "### Right Column" headings to separate content.
"""

    base64_image = encode_image(image_path)
    client = OpenAI(api_key=OPENAI_API_KEY)
    
    try:
        logger.info(f"Sending image to OpenAI: {image_path}")
        
        response = client.responses.create(
            model="o4-mini-2025-04-16",  # Using the mini version for cost efficiency
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"  # Use high detail for better accuracy on historical text
                        }
                    ]
                }
            ]
        )
        
        transcription = response.output_text
        
        # Cache the response
        cache_dir = CACHE_DIR
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        cache_file = cache_dir / f"{Path(image_path).stem}_response.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({"image_path": str(image_path), "transcription": transcription}, f, indent=2)
            
        return transcription
    
    except Exception as e:
        logger.error(f"Error with OpenAI API: {str(e)}")
        return None

def save_as_markdown(image_path, transcription, volume_info=None):
    """
    Save the transcription as a markdown file
    
    Args:
        image_path: Path to the original PNG image
        transcription: OCR'd text to save
        volume_info: Optional dictionary with volume metadata
    """
    if not transcription:
        logger.error("No transcription to save")
        return
    
    # Create base markdown directory
    MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate filename from original image path
    image_path = Path(image_path)
    parent_dirs = list(image_path.parents)[1:-1]  # Get volume and subfolder dirs
    
    # Expected path format: png_grants/Volume_Name_Years/subfolder/image.png
    relative_dirs = []
    for parent in parent_dirs:
        relative_dirs.insert(0, parent.name)
    
    # Create directory structure
    output_dir = MARKDOWN_DIR
    for dir_name in relative_dirs:
        output_dir = output_dir / dir_name
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create markdown file
    output_file = output_dir / f"{image_path.stem}.md"
    
    # Prepare front matter
    front_matter = "---\n"
    front_matter += f"source_image: \"{image_path.name}\"\n"
    
    if volume_info:
        for key, value in volume_info.items():
            front_matter += f"{key}: \"{value}\"\n"
    
    front_matter += "---\n\n"
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(front_matter)
        f.write(transcription)
    
    logger.info(f"Saved transcription to {output_file}")
    return output_file

def extract_volume_info_from_path(image_path):
    """Extract volume information from the image path"""
    # Expected path: png_grants/Volume_Name_Years/subfolder/image.png
    path_parts = Path(image_path).parts
    
    if len(path_parts) < 4:
        return None
    
    # Parse volume name and years from directory name
    # Example format: Grants_No.1_1690_1692
    volume_dir = path_parts[-3]
    parts = volume_dir.split('_')
    
    if len(parts) < 3:
        return None
    
    # Handle the format "Grants_No.1_1690_1692"
    if parts[0] == "Grants" and parts[1].startswith("No"):
        name = f"Grants {parts[1]}"
        year_start = parts[2]
        year_end = parts[3]
    # Handle the format "Grants_A_1722_1726"
    elif parts[0] == "Grants" and len(parts[1]) == 1:
        name = f"Grants {parts[1]}"
        year_start = parts[2]
        year_end = parts[3]
    else:
        name = volume_dir
        year_start = "Unknown"
        year_end = "Unknown"
    
    # Extract page number from filename
    page_num = "Unknown"
    filename = path_parts[-1]
    page_match = filename.split('_')
    if len(page_match) > 1:
        page_num = page_match[1].split('.')[0]
    
    return {
        "volume": name,
        "years": f"{year_start}-{year_end}",
        "page": page_num,
        "subfolder": path_parts[-2]
    }

def main():
    parser = argparse.ArgumentParser(description='OCR a single PNG image using OpenAI Vision')
    parser.add_argument('image_path', help='Path to the PNG image to OCR')
    parser.add_argument('--prompt', help='Custom prompt to use for OCR')
    
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.exists(args.image_path):
        logger.error(f"Image not found: {args.image_path}")
        sys.exit(1)
    
    # Extract volume information from path
    volume_info = extract_volume_info_from_path(args.image_path)
    
    # OCR the image
    transcription = ocr_image_with_openai(args.image_path, args.prompt)
    
    if transcription:
        # Save as markdown
        output_file = save_as_markdown(args.image_path, transcription, volume_info)
        print(f"\nTranscription complete! Saved to: {output_file}")
    else:
        logger.error("OCR failed, no transcription generated")

if __name__ == "__main__":
    main() 