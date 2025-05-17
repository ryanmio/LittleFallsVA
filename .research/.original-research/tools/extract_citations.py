#!/usr/bin/env python3
import re
import json
import urllib.parse
from pathlib import Path

def extract_citations(markdown_file):
    """Extract all citations from the markdown file."""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match citations
    pattern = r'\(\[little_falls_research_2025-04-08\.json\]\(file://.*?text=([^)]+)\)\)'
    
    # Find all matches
    matches = re.finditer(pattern, content)
    
    # Store citations as list of dictionaries
    citations = []
    for match in matches:
        encoded_text = match.group(1)
        # Double decode to handle doubly-encoded characters
        text_anchor = urllib.parse.unquote(urllib.parse.unquote(encoded_text))
        full_citation = match.group(0)
        
        if not any(c['text_anchor'] == text_anchor for c in citations):
            citations.append({
                'text_anchor': text_anchor,
                'original_encoded': encoded_text,
                'full_citation': full_citation
            })
    
    return citations

def main():
    # Extract citations from the file
    markdown_file = '../../content/english/research/s1-a1-ancient-crossroads.md'
    citations = extract_citations(markdown_file)
    
    # Save citations to JSON file
    with open('citations.json', 'w', encoding='utf-8') as f:
        json.dump(citations, f, indent=2)
    
    # Print results
    print(f"Found {len(citations)} unique citations:")
    print("\nText Anchors (Decoded):")
    for i, citation in enumerate(citations, 1):
        print(f"\n{i}. Decoded Text: {citation['text_anchor']}")
        print(f"   Original Encoded: {citation['original_encoded']}")
        print(f"   Full Citation: {citation['full_citation']}")
    
    print(f"\nCitations saved to citations.json")

if __name__ == "__main__":
    main() 