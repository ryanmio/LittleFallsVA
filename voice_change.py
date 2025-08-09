import re

def replace_voice(input_file, output_file=None):
    """
    Replace 'we/us' voice with 'I/me' in academic paper
    """
    if output_file is None:
        output_file = input_file
    
    # Read the file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define replacements
    replacements = [
        (r'\bWe\b', 'I'),
        (r'\bwe\b', 'I'),
        (r'\bOur\b', 'My'),
        (r'\bour\b', 'my'),
        (r'\bWe\'ve\b', 'I\'ve'),
        (r'\bwe\'ve\b', 'I\'ve'),
        (r'\bWe\'re\b', 'I\'m'),
        (r'\bwe\'re\b', 'I\'m'),
        (r'\bus\b', 'me'),
        (r'\bUs\b', 'Me'),
        (r'\bourselves\b', 'myself'),
        (r'\bOurselves\b', 'Myself')
    ]
    
    # Apply replacements
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    # Write the modified content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Voice changed in {output_file}")

if __name__ == "__main__":
    input_file = ".research/.original-research/1699-claim/data/S/land-grants/geolocation/paper/main.md"
    replace_voice(input_file) 