#!/usr/bin/env python3

import json
import urllib.parse
import re

def load_citations(file_path):
    """Load citations from JSON file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_text_fragments(url):
    """Extract text fragments from URL"""
    fragments = []
    
    # Extract all the relevant parts from text= fragments
    if 'text=' in url or 'text =' in url:
        # Extract text after text= parameter with support for spaces
        matches = re.findall(r'text\s*=([^&#]+)', url)
        for encoded_text in matches:
            # Decode the text (possibly multiple times)
            decoded = urllib.parse.unquote(encoded_text)
            while '%' in decoded:
                decoded = urllib.parse.unquote(decoded)
            # Clean up any leading/trailing punctuation
            decoded = decoded.strip().strip(',.;:()[]{}"\'"')
            fragments.append(decoded)
    
    # Also extract text between commas in the text anchor part
    comma_parts = re.findall(r'#:~:text\s*=([^,]+),([^&#,]+)', url)
    if comma_parts:
        for start, end in comma_parts:
            start_decoded = urllib.parse.unquote(start)
            end_decoded = urllib.parse.unquote(end)
            while '%' in start_decoded:
                start_decoded = urllib.parse.unquote(start_decoded)
            while '%' in end_decoded:
                end_decoded = urllib.parse.unquote(end_decoded)
            # Clean up any leading/trailing punctuation
            start_decoded = start_decoded.strip().strip(',.;:()[]{}"\'"')
            end_decoded = end_decoded.strip().strip(',.;:()[]{}"\'"')
            if start_decoded:
                fragments.append(f"Start: {start_decoded}")
            if end_decoded:
                fragments.append(f"End: {end_decoded}")
    
    return fragments

def decode_citation(text):
    """Decode URL encoded text and normalize Unicode characters"""
    # Decode URL encoding (multiple times if needed)
    decoded = urllib.parse.unquote(text)
    while '%' in decoded:
        decoded = urllib.parse.unquote(decoded)
    
    # Normalize Unicode apostrophes and quotes
    decoded = decoded.replace('\u2019', "'").replace('\u2018', "'")
    decoded = decoded.replace('\u201c', '"').replace('\u201d', '"')
    
    # Remove escape characters
    decoded = decoded.replace('\\n', ' ').replace('\\r', ' ')
    
    # Special case for ",nBy the time of" -> "By the time of"
    if decoded.startswith(',n'):
        decoded = decoded[2:]
    
    return decoded.strip()

def get_main_search_terms(text):
    """Extract useful search terms from citation text"""
    # Special case for ",nBy the time of" -> "By the time of"
    if text.startswith(',n'):
        text = text[2:]
        
    # Remove leading/trailing punctuation and whitespace
    text = text.strip().strip(',.;:()[]{}"\'"')
    
    # Split by comma and get the best part
    if ',' in text:
        parts = [p.strip().strip(',.;:()[]{}"\'"') for p in text.split(',')]
        # Filter out very short parts and empty parts
        parts = [p for p in parts if len(p) >= 3]
        if not parts:
            return text
        # Get the longest part that's at least 10 chars (if any)
        long_parts = [p for p in parts if len(p) >= 10]
        if long_parts:
            return max(long_parts, key=len)
        return parts[0]  # Use first part if no good long parts
    
    # Remove URLs or markdown links
    cleaned = re.sub(r'\[|\]|\(|\)|https?://[^\s]+', '', text)
    cleaned = re.sub(r'#:~:text\s*=.*', '', cleaned)
    
    return cleaned.strip()

def main():
    # Load citations
    try:
        citations = load_citations("citations.json")
        print(f"Loaded {len(citations)} citations\n")
        
        print("=== SEARCH TERMS FOR MANUAL LOOKUP ===\n")
        
        # Process and print each citation
        for i, citation in enumerate(citations, 1):
            text_anchor = citation.get('text_anchor', '')
            full_citation = citation.get('full_citation', '')
            
            decoded_text = decode_citation(text_anchor)
            main_term = get_main_search_terms(decoded_text)
            
            # Extract any text fragments from the URL
            fragments = extract_text_fragments(full_citation)
            
            print(f"{i}. Main search term: {main_term}")
            if main_term != decoded_text:
                print(f"   Full decoded citation: {decoded_text}")
            
            # Print fragments if found
            if fragments:
                print("   Text fragments from URL:")
                for j, fragment in enumerate(fragments, 1):
                    print(f"      {j}. {fragment}")
            
            print()
            
        print("\nAll citations extracted and decoded.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 