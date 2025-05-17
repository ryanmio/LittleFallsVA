#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse
import re
import time
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import functions from our existing script
from process_iiif_manifest import create_markdown_from_manifest, sanitize_filename

# Output directory
OUTPUT_DIR = ".research/images"

def process_url_list(url_list, max_workers=4):
    """Process a list of IIIF manifest URLs concurrently"""
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Track successful and failed URLs
    successful = []
    failed = []
    
    # Process URLs concurrently
    print(f"Processing {len(url_list)} URLs with {max_workers} workers...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all URL processing tasks
        future_to_url = {executor.submit(create_markdown_from_manifest, url): url for url in url_list}
        
        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_url), 1):
            url = future_to_url[future]
            try:
                result = future.result()
                if result:
                    successful.append((url, result))
                    print(f"[{i}/{len(url_list)}] Successfully processed: {url} -> {result}")
                else:
                    failed.append((url, "Unknown error"))
                    print(f"[{i}/{len(url_list)}] Failed to process: {url}")
            except Exception as e:
                failed.append((url, str(e)))
                print(f"[{i}/{len(url_list)}] Error processing {url}: {e}")
    
    # Print summary
    print("\n=== Processing Summary ===")
    print(f"Total URLs: {len(url_list)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed URLs:")
        for url, error in failed:
            print(f"- {url}: {error}")

def main():
    parser = argparse.ArgumentParser(description="Process multiple IIIF manifest URLs efficiently")
    parser.add_argument("--file", "-f", help="File containing list of URLs (one per line)")
    parser.add_argument("--urls", "-u", nargs="+", help="One or more IIIF manifest URLs to process")
    parser.add_argument("--workers", "-w", type=int, default=4, help="Number of concurrent workers (default: 4)")
    
    args = parser.parse_args()
    
    urls = []
    
    # Collect URLs from file
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip()]
                print(f"Loaded {len(file_urls)} URLs from {args.file}")
                urls.extend(file_urls)
        except Exception as e:
            print(f"Error reading URL file {args.file}: {e}")
            return 1
    
    # Add URLs from command line
    if args.urls:
        urls.extend(args.urls)
    
    # Make sure we have some URLs to process
    if not urls:
        print("No URLs specified. Use --file or --urls to provide URLs.")
        return 1
    
    # Remove duplicates but maintain order
    unique_urls = []
    for url in urls:
        if url not in unique_urls:
            unique_urls.append(url)
    
    if len(unique_urls) < len(urls):
        print(f"Removed {len(urls) - len(unique_urls)} duplicate URLs.")
    
    # Process the URLs
    process_url_list(unique_urls, max_workers=args.workers)
    return 0

if __name__ == "__main__":
    sys.exit(main()) 