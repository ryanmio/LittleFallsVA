#!/usr/bin/env python3

import os
import sys
import json
import requests
import argparse
import re
from datetime import datetime
from pathlib import Path

# Output directory
OUTPUT_DIR = ".research/images"

def sanitize_filename(title):
    """Convert title to a safe filename"""
    # Remove special characters and replace spaces with underscores
    # First remove any brackets or parentheses
    title = re.sub(r'[\[\]\(\)]', '', title)
    # Then remove other special characters and replace spaces with underscores
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[\s]+', '_', filename)
    # Limit filename length to avoid issues
    if len(filename) > 50:
        filename = filename[:50]
    return filename

def create_markdown_from_manifest(manifest_url):
    """Process a IIIF manifest URL and create a markdown file with image information"""
    print(f"Processing manifest: {manifest_url}")
    
    try:
        # Download the manifest JSON
        response = requests.get(manifest_url)
        response.raise_for_status()
        manifest = response.json()
        
        # Extract metadata
        label = manifest.get("label", "Unknown Title")
        if isinstance(label, dict):
            label = label.get("@value", "Unknown Title")
        elif isinstance(label, list):
            label = label[0].get("@value", "Unknown Title") if label else "Unknown Title"
        # For string labels, no processing needed
        
        print(f"Found label: {label}")
        
        # Get description if available
        description = ""
        if "description" in manifest:
            desc = manifest.get("description", "")
            if isinstance(desc, dict):
                description = desc.get("@value", "")
            elif isinstance(desc, list):
                description = desc[0].get("@value", "") if desc else ""
            elif isinstance(desc, str):
                description = desc
        
        # Get metadata fields
        metadata_dict = {}
        if "metadata" in manifest:
            for item in manifest.get("metadata", []):
                # Handle label
                label_key = item.get("label", "")
                if isinstance(label_key, dict):
                    label_key = label_key.get("@value", "")
                elif isinstance(label_key, list):
                    label_key = label_key[0].get("@value", "") if label_key else ""
                # For string labels, no processing needed
                
                # Handle value
                value = item.get("value", "")
                if isinstance(value, dict):
                    value = value.get("@value", "")
                elif isinstance(value, list):
                    if value and isinstance(value[0], dict):
                        value = value[0].get("@value", "") 
                    elif value:
                        value = value[0]  # If it's a list of strings
                # For string values, no processing needed
                
                if label_key and value:
                    metadata_dict[label_key] = value
        
        # Get first image URL (if available)
        image_url = ""
        if "sequences" in manifest and manifest["sequences"]:
            if "canvases" in manifest["sequences"][0] and manifest["sequences"][0]["canvases"]:
                first_canvas = manifest["sequences"][0]["canvases"][0]
                if "images" in first_canvas and first_canvas["images"]:
                    resource = first_canvas["images"][0].get("resource", {})
                    if isinstance(resource, dict):
                        image_url = resource.get("@id", "")
        
        # Create front matter content
        front_matter = {}
        
        # Extract important metadata for front matter
        # Title - from Title metadata or from manifest label
        front_matter["title"] = metadata_dict.get("Title", label)
        
        # Date 
        front_matter["date"] = metadata_dict.get("Date", "unknown")
        
        # Subject
        if "Subject" in metadata_dict:
            front_matter["subject"] = metadata_dict.get("Subject")
            
        # Creator
        if "Creator" in metadata_dict:
            front_matter["creator"] = metadata_dict.get("Creator")
            
        # Place
        if "Place" in metadata_dict:
            front_matter["location"] = metadata_dict.get("Place")
            
        # Format
        if "Format" in metadata_dict:
            front_matter["format"] = metadata_dict.get("Format")
            
        # Collection
        front_matter["source"] = metadata_dict.get("Collection", "Mary Riley Styles Public Library")
        
        # Identifier
        if "Identifier" in metadata_dict:
            front_matter["identifier"] = metadata_dict.get("Identifier")
            
        # Description
        if description or "Description" in metadata_dict:
            front_matter["description"] = metadata_dict.get("Description", description)
            
        # Color
        if "Color" in metadata_dict:
            front_matter["color"] = metadata_dict.get("Color")
            
        # Dimensions
        if "Dimensions" in metadata_dict:
            front_matter["dimensions"] = metadata_dict.get("Dimensions")
            
        # Always include these fields
        front_matter["digitized"] = True
        front_matter["manifest_url"] = manifest_url
        
        # If there's an image URL available
        if image_url:
            front_matter["image_url"] = image_url
        
        # Create filename from title instead of label
        title_for_filename = front_matter["title"]
        safe_title = sanitize_filename(title_for_filename)
        
        # If the sanitized title is empty (for example if the title was just '[  ]'), 
        # fall back to using the label or identifier
        if not safe_title:
            if "identifier" in front_matter:
                safe_title = f"item_{front_matter['identifier']}"
            else:
                safe_title = sanitize_filename(label)
        
        filename = f"{safe_title}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        print(f"Using filename: {filename}")
        
        # Create the markdown content
        markdown_content = "---\n"
        for key, value in front_matter.items():
            # Sanitize the value for YAML
            if isinstance(value, str):
                # Escape quotes in the string
                value = value.replace('"', '\\"')
                markdown_content += f'{key}: "{value}"\n'
            else:
                markdown_content += f"{key}: {value}\n"
        markdown_content += "---\n\n"
        
        # Add content sections
        markdown_content += f"# {front_matter['title']}\n\n"
        
        if "description" in front_matter and front_matter["description"]:
            markdown_content += f"## Description\n\n{front_matter['description']}\n\n"
        
        # Add metadata section
        markdown_content += "## Metadata\n"
        for key, value in metadata_dict.items():
            markdown_content += f"\n- **{key}**: {value}"
        
        # Add image link if available
        if image_url:
            markdown_content += f"\n\n## Image\n\nA digital version of this historical image is available at:\n[{front_matter['title']} Image]({image_url})\n"
        
        # Add manifest link
        markdown_content += f"\n## Digital Manifest\n\nThe full IIIF manifest for this item is available at:\n[IIIF Manifest]({manifest_url})\n"
        
        # Add historical significance section (placeholder)
        markdown_content += "\n## Historical Significance\n\n*Note: Add historical significance details here.*\n"
        
        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Created markdown file: {filepath}")
        return filepath
    
    except Exception as e:
        print(f"Error processing manifest {manifest_url}: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="Process IIIF manifest URLs and create markdown files")
    parser.add_argument("urls", nargs="+", help="One or more IIIF manifest URLs to process")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Process each URL
    for url in args.urls:
        create_markdown_from_manifest(url)

if __name__ == "__main__":
    main() 