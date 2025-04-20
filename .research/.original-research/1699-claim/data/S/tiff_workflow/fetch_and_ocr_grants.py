#!/usr/bin/env python3
"""
Northern Neck Grant Volume Processor

This script downloads TIFF images from the Library of Virginia's Northern Neck
grant volumes (1690-1729), performs OCR on them, and flags pages that mention
specific keywords.

The script:
1. Crawls the Library of Virginia website to discover the correct URLs
2. Downloads TIFFs from the specified volumes
3. Organizes them in a structured directory
4. Performs OCR on each image
5. Searches for keywords in the OCR output
6. Generates a CSV report of pages containing the keywords
"""

import os
import time
import csv
import logging
import requests
from pathlib import Path
from PIL import Image
import pytesseract
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from tqdm import tqdm
import sys
import traceback

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG for more verbose output
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('grants_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path('.')
TIFF_DIR = BASE_DIR / 'tiff_grants'
OCR_DIR = BASE_DIR / 'ocr_output'
RESULTS_FILE = BASE_DIR / 'grant_page_hits.csv'
DEBUG_FILE = BASE_DIR / 'debug_info.log'
METADATA_FILE = BASE_DIR / 'grants_metadata.json'
DOWNLOAD_DELAY = 1.0  # seconds between requests to respect rate limiting
KEYWORDS = ["Falls Church", "Hunting Creek", "Little Falls"]

# URL patterns
BASE_URL = "https://image.lva.virginia.gov/LONN"
MAIN_INDEX_URL = f"{BASE_URL}/NN.html"

# Target volumes we care about (1690-1729)
TARGET_VOLUMES = [
    {"name": "Grants No.1", "years": "1690-1692"},
    {"name": "Grants No.2", "years": "1694-1700"},
    {"name": "Grants No.3", "years": "1703-1710"},
    {"name": "Grants No.4", "years": "1710-1712"},
    {"name": "Grants No.5", "years": "1713-1719"},
    {"name": "Grants A", "years": "1722-1726"},
    {"name": "Grants B", "years": "1726-1729"}
]

# TEST MODE - Only process a few pages for initial testing
TEST_MODE = True
PAGES_PER_VOLUME = 5  # Number of pages to test per volume in test mode
MAX_PAGE_GROUPS_PER_VOLUME = 2  # Limit the number of page groups to process in test mode

def log_debug(message, file_path=DEBUG_FILE):
    """Write detailed debug information to a separate file."""
    with open(file_path, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def create_directories():
    """Create necessary directories if they don't exist."""
    logger.info("Creating directory structure")
    TIFF_DIR.mkdir(parents=True, exist_ok=True)
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create an empty debug log file
    with open(DEBUG_FILE, 'w') as f:
        f.write(f"Debug log started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"TEST_MODE: {TEST_MODE}\n\n")

def fetch_url(url, retry_count=3, timeout=30):
    """Fetch URL content with retries."""
    for attempt in range(retry_count):
        try:
            logger.debug(f"Fetching URL: {url} (attempt {attempt + 1})")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            logger.debug(f"Successfully fetched {url}")
            return response.text
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {url} (attempt {attempt + 1}): {str(e)}")
            time.sleep(1)  # Wait before retrying
    
    logger.error(f"Failed to fetch {url} after {retry_count} attempts")
    return None

def discover_volume_urls():
    """Discover volume URLs from the main index page."""
    logger.info("Discovering volume URLs from the main index page")
    
    # Fetch the main index page
    html_content = fetch_url(MAIN_INDEX_URL)
    if not html_content:
        logger.error("Failed to fetch main index page")
        return []
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all table rows
    rows = soup.find_all('tr')
    
    discovered_volumes = []
    
    # Process each row to find our target volumes
    for row in rows:
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        
        # Get the link and text from the first cell
        link_elem = cells[0].find('a')
        if not link_elem:
            continue
        
        href = link_elem.get('href', '')
        name = link_elem.text.strip()
        
        # Get the year range from the second cell
        year_elem = cells[1].find('a')
        years = year_elem.text.strip() if year_elem else cells[1].text.strip()
        
        # Check if this is one of our target volumes
        for target in TARGET_VOLUMES:
            if target["name"] in name and target["years"] in years:
                # Extract NN folder from href (like '/LONN/NN-3/288-1')
                match = re.search(r'/LONN/(NN-\d+)/([^/]+)', href)
                if match:
                    nn_folder = match.group(1)
                    subfolder = match.group(2)
                    
                    volume_info = {
                        "name": name,
                        "years": years,
                        "nn_folder": nn_folder,
                        "subfolder": subfolder,
                        "url": f"{BASE_URL}/{nn_folder}/{subfolder}"
                    }
                    
                    logger.info(f"Discovered volume: {name} ({years}) at {volume_info['url']}")
                    discovered_volumes.append(volume_info)
                    break
    
    if TEST_MODE and discovered_volumes:
        logger.info(f"TEST MODE: Limiting to first {min(2, len(discovered_volumes))} volumes")
        discovered_volumes = discovered_volumes[:min(2, len(discovered_volumes))]
    
    return discovered_volumes

def discover_page_groups(volume_url):
    """Discover page groups for a volume."""
    logger.info(f"Discovering page groups for volume at {volume_url}")
    
    html_content = fetch_url(volume_url)
    if not html_content:
        logger.error(f"Failed to fetch volume page at {volume_url}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    page_groups = []
    
    # Look for links like '1-100.html', '101-200.html', etc.
    page_links = soup.find_all('a', href=re.compile(r'^\d+-\d+\.html$'))
    
    for link in page_links:
        href = link.get('href')
        group_url = f"{volume_url}/{href}"
        page_ranges = re.findall(r'(\d+)-(\d+)', href)
        
        if page_ranges:
            start_page, end_page = int(page_ranges[0][0]), int(page_ranges[0][1])
            page_group = {
                "url": group_url,
                "start_page": start_page,
                "end_page": end_page,
                "group_name": href.replace('.html', '')
            }
            
            logger.info(f"Discovered page group: {page_group['group_name']} ({start_page}-{end_page})")
            page_groups.append(page_group)
    
    # Sort page groups by start page
    page_groups.sort(key=lambda x: x["start_page"])
    
    if TEST_MODE and page_groups:
        logger.info(f"TEST MODE: Limiting to first {min(MAX_PAGE_GROUPS_PER_VOLUME, len(page_groups))} page groups")
        page_groups = page_groups[:min(MAX_PAGE_GROUPS_PER_VOLUME, len(page_groups))]
    
    return page_groups

def discover_tiff_urls(page_group_url, volume_subfolder):
    """Discover TIFF URLs from a page group."""
    logger.info(f"Discovering TIFF URLs for page group at {page_group_url}")
    
    html_content = fetch_url(page_group_url)
    if not html_content:
        logger.error(f"Failed to fetch page group at {page_group_url}")
        return []
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    tiff_urls = []
    
    # Extract reel prefix from subfolder like '288-1'
    reel_prefix = volume_subfolder.split('-')[0]
    
    # Look for links to TIFF files
    tiff_links = soup.find_all('a', href=re.compile(rf'{reel_prefix}_\d+\.tif$'))
    
    for link in tiff_links:
        href = link.get('href')
        # Get the page number from the filename (e.g., '288_0234.tif' → '0234')
        page_match = re.search(rf'{reel_prefix}_(\d+)\.tif$', href)
        
        if page_match:
            page_num = int(page_match.group(1))
            
            # Fix the URL construction by using the base domain and appending the href
            # Since href already includes the full path after domain
            tiff_url = f"https://image.lva.virginia.gov{href}"
            
            tiff_info = {
                "url": tiff_url,
                "page_num": page_num,
                "filename": href
            }
            
            logger.debug(f"Discovered TIFF: {tiff_info['filename']} (page {page_num}) at {tiff_url}")
            tiff_urls.append(tiff_info)
    
    if TEST_MODE and tiff_urls:
        logger.info(f"TEST MODE: Limiting to first {min(PAGES_PER_VOLUME, len(tiff_urls))} TIFF files")
        tiff_urls = tiff_urls[:min(PAGES_PER_VOLUME, len(tiff_urls))]
    
    return tiff_urls

def download_tiff(url, output_path):
    """Download a TIFF file from the given URL."""
    try:
        logger.debug(f"Downloading: {url}")
        start_time = time.time()
        
        # Initial HEAD request to check if file exists
        head_response = requests.head(url, timeout=10)
        if head_response.status_code != 200:
            logger.warning(f"File not found at {url} (status code: {head_response.status_code})")
            log_debug(f"HEAD request failed for {url}: {head_response.status_code}")
            return False
        
        # File exists, proceed with download
        file_size = int(head_response.headers.get('content-length', 0))
        logger.debug(f"File exists at URL. Size: {file_size/1024:.2f} KB")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Create parent directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        downloaded_size = 0
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        
        end_time = time.time()
        download_time = end_time - start_time
        download_speed = (downloaded_size / 1024) / download_time if download_time > 0 else 0
        
        logger.debug(f"Downloaded {downloaded_size/1024:.2f} KB in {download_time:.2f}s ({download_speed:.2f} KB/s)")
        log_debug(f"Download successful: {url} -> {output_path}")
        
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download {url}: {str(e)}")
        log_debug(f"Download error: {url}\n{traceback.format_exc()}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while downloading {url}: {str(e)}")
        log_debug(f"Unexpected download error: {url}\n{traceback.format_exc()}")
        return False

def perform_ocr(image_path):
    """Perform OCR on the image and return the text."""
    try:
        logger.debug(f"Starting OCR for: {image_path}")
        start_time = time.time()
        
        # Check if image exists and is readable
        if not os.path.exists(image_path):
            logger.error(f"Image file doesn't exist: {image_path}")
            return ""
        
        # Get image details before OCR
        file_size = os.path.getsize(image_path) / 1024  # KB
        logger.debug(f"Image size: {file_size:.2f} KB")
        
        # Open and process the image
        image = Image.open(image_path)
        logger.debug(f"Image opened: {image.format}, {image.size}, {image.mode}")
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        text_length = len(text)
        
        end_time = time.time()
        ocr_time = end_time - start_time
        
        # Log statistics
        logger.debug(f"OCR completed in {ocr_time:.2f}s. Text length: {text_length} chars")
        log_debug(f"OCR stats for {image_path}: {text_length} chars, {ocr_time:.2f}s")
        
        # Log a sample of the text for debugging
        if text:
            sample = text[:200] + "..." if len(text) > 200 else text
            log_debug(f"OCR text sample from {image_path}:\n{sample}")
        
        return text
    except Exception as e:
        logger.error(f"OCR failed for {image_path}: {str(e)}")
        log_debug(f"OCR error: {image_path}\n{traceback.format_exc()}")
        return ""

def search_keywords(text, keywords, source_info=""):
    """Search for keywords in text and return matches with context."""
    results = []
    
    if not text:
        logger.debug(f"No text to search for keywords in {source_info}")
        return results
    
    logger.debug(f"Searching for {len(keywords)} keywords in text ({len(text)} chars)")
    
    lines = text.split('\n')
    matches_found = 0
    
    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword.lower() in line.lower():
                matches_found += 1
                # Get a few lines before and after for context
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                context = '\n'.join(lines[start:end])
                
                result = {
                    'keyword': keyword,
                    'snippet': context.strip(),
                    'line_number': i + 1,
                    'context_lines': f"{start+1}-{end}"
                }
                
                results.append(result)
                logger.info(f"Found keyword '{keyword}' in {source_info} at line {i+1}")
                log_debug(f"Keyword match in {source_info}:\nKeyword: {keyword}\nContext:\n{context.strip()}")
    
    if matches_found > 0:
        logger.debug(f"Found {matches_found} keyword matches in {source_info}")
    else:
        logger.debug(f"No keyword matches found in {source_info}")
    
    return results

def process_tiff(volume_info, page_group, tiff_info):
    """Process a single TIFF: download, OCR, and search for keywords."""
    volume_name = volume_info["name"]
    volume_years = volume_info["years"]
    nn_folder = volume_info["nn_folder"]
    subfolder = volume_info["subfolder"]
    
    tiff_url = tiff_info["url"]
    page_num = tiff_info["page_num"]
    
    # Extract just the base filename without the path
    filename = os.path.basename(tiff_info["filename"])
    
    # Create a clean slug for directory naming
    volume_slug = f"{volume_name.replace(' ', '_')}_{volume_years.replace('-', '_')}"
    
    # Define paths
    tiff_dir = TIFF_DIR / volume_slug / subfolder
    ocr_dir = OCR_DIR / volume_slug / subfolder
    
    tiff_path = tiff_dir / filename
    ocr_path = ocr_dir / f"{os.path.splitext(filename)[0]}.txt"
    
    logger.info(f"Processing TIFF: {volume_name} ({volume_years}), page {page_num}")
    log_debug(f"===== PROCESSING TIFF: {tiff_url} =====")
    
    # Make sure directories exist
    tiff_dir.mkdir(parents=True, exist_ok=True)
    ocr_dir.mkdir(parents=True, exist_ok=True)
    
    # Download TIFF if needed
    if tiff_path.exists():
        logger.info(f"TIFF already exists: {tiff_path}, skipping download")
    else:
        logger.info(f"Downloading TIFF from {tiff_url}")
        if download_tiff(tiff_url, tiff_path):
            logger.info(f"Successfully downloaded TIFF to {tiff_path}")
            time.sleep(DOWNLOAD_DELAY)  # Respect rate limiting
        else:
            logger.warning(f"Failed to download TIFF from {tiff_url}, skipping")
            return []
    
    # Perform OCR if needed
    if ocr_path.exists():
        logger.info(f"OCR already exists: {ocr_path}, loading from file")
        try:
            with open(ocr_path, 'r', encoding='utf-8') as f:
                ocr_text = f.read()
                logger.debug(f"Loaded {len(ocr_text)} chars of OCR text from {ocr_path}")
        except Exception as e:
            logger.error(f"Failed to read existing OCR: {str(e)}")
            log_debug(f"Error reading OCR file {ocr_path}:\n{traceback.format_exc()}")
            return []
    else:
        logger.info(f"Performing OCR on {tiff_path}")
        ocr_text = perform_ocr(tiff_path)
        
        if ocr_text:
            logger.info(f"Writing OCR text to {ocr_path}")
            with open(ocr_path, 'w', encoding='utf-8') as f:
                f.write(ocr_text)
        else:
            logger.warning(f"OCR produced no text for {tiff_path}")
            return []
    
    # Search for keywords
    source_info = f"{volume_name} ({volume_years}), page {page_num}"
    logger.info(f"Searching for keywords in {source_info}")
    matches = search_keywords(ocr_text, KEYWORDS, source_info)
    
    # Prepare results
    results = []
    for match in matches:
        result = {
            'volume': volume_name,
            'years': volume_years,
            'nn_folder': nn_folder,
            'subfolder': subfolder,
            'page_num': page_num,
            'page_group': page_group["group_name"],
            'filename': filename,
            'url': tiff_url,
            'keyword': match['keyword'],
            'snippet': match['snippet'],
            'line_number': match.get('line_number', 0)
        }
        results.append(result)
    
    if results:
        logger.info(f"Found {len(results)} keyword matches in {source_info}")
    else:
        logger.info(f"No keyword matches found in {source_info}")
    
    log_debug(f"===== COMPLETED TIFF: {tiff_url}, found {len(results)} matches =====\n")
    return results

def process_page_group(volume_info, page_group):
    """Process all TIFFs in a page group."""
    logger.info(f"Processing page group: {page_group['group_name']} for {volume_info['name']} ({volume_info['years']})")
    
    # Discover TIFF URLs in this page group
    tiff_urls = discover_tiff_urls(page_group["url"], volume_info["subfolder"])
    
    if not tiff_urls:
        logger.warning(f"No TIFF files found in page group {page_group['group_name']}")
        return []
    
    logger.info(f"Found {len(tiff_urls)} TIFF files in page group {page_group['group_name']}")
    
    results = []
    for tiff_info in tqdm(tiff_urls, desc=f"Processing {volume_info['name']} {page_group['group_name']}"):
        try:
            tiff_results = process_tiff(volume_info, page_group, tiff_info)
            results.extend(tiff_results)
        except Exception as e:
            logger.error(f"Error processing TIFF {tiff_info['url']}: {str(e)}")
            log_debug(f"Unexpected error processing TIFF:\n{traceback.format_exc()}")
            continue
    
    return results

def process_volume(volume_info):
    """Process all page groups in a volume."""
    logger.info(f"Processing volume: {volume_info['name']} ({volume_info['years']})")
    
    # Discover page groups for this volume
    page_groups = discover_page_groups(volume_info["url"])
    
    if not page_groups:
        logger.warning(f"No page groups found for volume {volume_info['name']}")
        return []
    
    logger.info(f"Found {len(page_groups)} page groups for volume {volume_info['name']}")
    
    results = []
    for page_group in page_groups:
        page_group_results = process_page_group(volume_info, page_group)
        results.extend(page_group_results)
    
    return results

def main():
    """Main function to orchestrate the entire process."""
    start_time = time.time()
    
    logger.info("========================================================")
    logger.info("Starting Northern Neck grant processing")
    logger.info(f"Test mode: {'ENABLED' if TEST_MODE else 'DISABLED'}")
    logger.info(f"Keywords: {KEYWORDS}")
    logger.info("========================================================")
    
    # Create necessary directories
    create_directories()
    
    # Discover volume URLs
    volumes = discover_volume_urls()
    
    if not volumes:
        logger.error("No target volumes found. Exiting.")
        return
    
    logger.info(f"Found {len(volumes)} target volumes")
    
    # Process each volume
    all_results = []
    
    for volume_info in volumes:
        volume_results = process_volume(volume_info)
        all_results.extend(volume_results)
        logger.info(f"Completed volume {volume_info['name']}, found {len(volume_results)} matches")
    
    # Write results to CSV
    if all_results:
        result_file = RESULTS_FILE
        logger.info(f"Writing {len(all_results)} results to {result_file}")
        
        with open(result_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['volume', 'years', 'nn_folder', 'subfolder', 'page_num', 
                         'page_group', 'filename', 'url', 'keyword', 'snippet', 'line_number']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in all_results:
                writer.writerow(result)
        
        logger.info(f"Results saved to {result_file}")
    else:
        logger.info("No pages with keywords found")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    logger.info("========================================================")
    logger.info(f"Processing complete in {int(hours)}h {int(minutes)}m {int(seconds)}s")
    logger.info(f"Processed {len(volumes)} volumes")
    logger.info(f"Found {len(all_results)} keyword matches")
    logger.info("========================================================")
    
    log_debug(f"Script completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log_debug(f"Total runtime: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    log_debug(f"Total results: {len(all_results)}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}")
        log_debug(f"FATAL ERROR:\n{traceback.format_exc()}")
        sys.exit(1) 