#!/usr/bin/env python3

import json
import re
import urllib.parse

def simplify_text(text):
    """Strip all URLs, markdown, and technical notation from text"""
    # Decode URL encoding
    text = urllib.parse.unquote(text)
    while '%' in text:
        text = urllib.parse.unquote(text)
    
    # Remove common prefixes
    if text.startswith(',n'):
        text = text[2:]
    
    # Remove markdown links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    
    # Remove URLs, hash fragments, and technical notation
    text = re.sub(r'https?://[^\s,]+', '', text)
    text = re.sub(r'#:~:text[^,]*', '', text)
    text = re.sub(r'\.pdf[^,]*', '', text)
    text = re.sub(r'\.htm[^,]*', '', text)
    
    # Clean up technical patterns
    text = re.sub(r'site\)\)', '', text)
    text = re.sub(r'\d+gathered', 'gathered', text)
    text = re.sub(r'ite\.\s+\\n\\n', '', text)
    
    # Remove any remaining parentheses, brackets and other punctuation
    text = re.sub(r'[\[\]\(\)\{\}]', '', text)
    
    # Normalize apostrophes and quotes
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    
    # Split by commas and take the most meaningful part
    parts = [p.strip() for p in text.split(',')]
    parts = [p for p in parts if len(p) > 5 and not re.search(r'(RCP|site\)|^\))', p)]
    
    # Special case for citation 14
    if "neighbors have not survived in" in text:
        return "neighbors have not survived in"
    
    # Special case for citation 4 and 5
    if "Early Americans came to this" in text:
        return "Early Americans came to this"
    if "excavations indicate several prehistoric" in text:
        return "excavations indicate several prehistoric"
        
    if "John Smith's expedition" in text:
        return "Captain John Smith's expedition"
    
    if parts:
        # Find parts that seem like natural language
        natural_parts = []
        for part in parts:
            # Skip obvious non-text parts
            if re.search(r'(\.pdf|\.htm|#|http|site\)|^\))', part):
                continue
                
            # Skip parts with less than 5 letters
            letters = sum(c.isalpha() for c in part)
            if letters < 5:
                continue
                
            natural_parts.append(part)
        
        if natural_parts:
            # Return the longest natural language part
            return max(natural_parts, key=len).strip()
        
        # If no natural parts, return the longest part
        return max(parts, key=len).strip()
    
    # If no parts after filtering, return cleaned text
    cleaned = re.sub(r'[^\w\s\'\-\.,;:]', ' ', text)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def main():
    try:
        # Load citations
        with open("citations.json", 'r', encoding='utf-8') as f:
            citations = json.load(f)
        
        output_lines = []
        print(f"CITATION LOOKUP DETAILS (from {len(citations)} citations):\n")
        
        for i, citation in enumerate(citations, 1):
            raw_text = citation.get('text_anchor', '')
            full_citation = citation.get('full_citation', '')
            clean_term = simplify_text(raw_text)
            
            # Prepare output lines
            output_lines.append(f"Citation #{i}:")
            output_lines.append(f"  Original Text: {raw_text}")
            output_lines.append(f"  Full Citation: {full_citation}")
            output_lines.append(f"  Search Term: {clean_term}")
            output_lines.append("")  # blank line
            
            # Print to console
            print(f"Citation #{i}:")
            print(f"  Original Text: {raw_text}")
            print(f"  Full Citation: {full_citation}")
            print(f"  Search Term: {clean_term}")
            print()  # blank line
        
        # Save to file
        with open("citation_lookup_details.txt", "w", encoding="utf-8") as f:
            f.write(f"CITATION LOOKUP DETAILS (from {len(citations)} citations):\n\n")
            f.write("\n".join(output_lines))
            
        print(f"Full citation details saved to citation_lookup_details.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 