#!/usr/bin/env python3

import os
import json
import urllib.parse
import unicodedata
import re

def load_json_file(json_file):
    """Load the research JSON file"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return None

def normalize_text(text):
    """Normalize text for better matching"""
    # Replace common Unicode characters
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    # Convert to lowercase for case-insensitive matching
    text = text.lower()
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    return text

def extract_search_text(text_anchor):
    """Extract and clean search text from citation anchor"""
    # URL decode the text (twice if needed) to get proper characters
    decoded_text = urllib.parse.unquote(text_anchor)
    # Double decode in case of double encoding
    if '%' in decoded_text:
        decoded_text = urllib.parse.unquote(decoded_text)
    
    # If there's a comma, just use the first part (which is usually the main quote)
    if ',' in decoded_text:
        # If the second part is longer and seems more useful, use it
        parts = [p.strip() for p in decoded_text.split(',')]
        if len(parts) > 1 and len(parts[0]) < 10 and len(parts[1]) > 15:
            decoded_text = parts[1]
        else:
            decoded_text = parts[0]
    
    # Handle special cases
    if "origin of today" in decoded_text:
        return "origin of today's falls"
    
    # Clean up the text
    decoded_text = decoded_text.replace('\\n', ' ').replace('\\r', ' ')
    
    # Remove any remaining URL or Markdown formatting
    decoded_text = re.sub(r'\[|\]|\(|\)|file://|https?://[^ ]+', '', decoded_text)
    
    # Remove any '#:~:text=' fragments
    decoded_text = re.sub(r'#:~:text=.*', '', decoded_text)
    
    # Remove common problem characters
    decoded_text = decoded_text.strip('.,;:()[]{}"\' \t\n\r')
    
    # Make sure it's at least 5 characters to avoid false matches
    if len(decoded_text) < 5:
        return None
    
    # Normalize for better matching
    decoded_text = normalize_text(decoded_text)
    
    print(f"Extracted search text: '{decoded_text}'")
    return decoded_text

def find_source_for_text(json_data, text_anchor):
    """Find source information for a given text anchor"""
    try:
        # Extract search text
        search_text = extract_search_text(text_anchor)
        if not search_text:
            print(f"Could not extract usable search text from: '{text_anchor}'")
            return None
        
        # Search through each entry in the JSON
        for file_path, content in json_data.items():
            # Skip non-markdown files
            if not file_path.endswith('.md'):
                continue
            
            # Normalize content for better matching
            normalized_content = normalize_text(content)
            
            # Check if the text appears in the content
            if search_text in normalized_content:
                print(f"Match found in: {file_path}")
                
                # Extract metadata from frontmatter
                frontmatter = {}
                content_lines = content.split('\n')
                if content_lines[0].strip() == '---':
                    for i, line in enumerate(content_lines[1:]):
                        if line.strip() == '---':
                            break
                        if ':' in line:
                            key, value = line.split(':', 1)
                            frontmatter[key.strip()] = value.strip().strip('"')
                
                # Find the position in the normalized content
                match_pos = normalized_content.find(search_text)
                
                # Get the context (100 chars before and after)
                start_idx = max(0, match_pos - 100)
                end_idx = min(len(normalized_content), match_pos + len(search_text) + 100)
                context = normalized_content[start_idx:end_idx]
                
                # Return source information
                return {
                    'file': file_path,
                    'title': frontmatter.get('title', 'Unknown'),
                    'author': frontmatter.get('author', 'Unknown'),
                    'date': frontmatter.get('date', 'Unknown'),
                    'source': frontmatter.get('source', 'Unknown'),
                    'text_context': context,
                    'search_text': search_text
                }
        
        print(f"No match found for: '{search_text}'")
    except Exception as e:
        print(f"Error processing text anchor: {e}")
        import traceback
        traceback.print_exc()
    
    return None

def main():
    # Load citations from previous script
    citations_file = "citations.json"
    if os.path.exists(citations_file):
        with open(citations_file, 'r') as f:
            citations = json.load(f)
    else:
        print(f"Error: {citations_file} not found")
        return

    # Load research JSON
    json_file = "../../little_falls_research.json"
    json_data = load_json_file(json_file)
    if not json_data:
        return

    # Process each citation
    results = []
    for citation in citations:
        text_anchor = citation['text_anchor']
        print(f"\nProcessing citation: '{text_anchor}'")
        source_info = find_source_for_text(json_data, text_anchor)
        
        if source_info:
            results.append({
                'original_citation': citation['full_citation'],
                'source_info': source_info
            })
            print(f"Found source: {source_info['title']} ({source_info['file']})")
        else:
            print(f"No source found for text anchor: '{text_anchor}'")

    # Save results
    with open('citation_sources.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nProcessed {len(results)} citations with found sources out of {len(citations)} total")
    print(f"Results saved to citation_sources.json")

if __name__ == "__main__":
    main() 