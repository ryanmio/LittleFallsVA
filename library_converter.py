import json
import re
import csv

def parse_library_md(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Initialize data structure
    library_data = []
    current_box = None
    current_series = None
    current_folder = None
    
    # Process each line
    lines = content.strip().split('\n')
    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue
        
        # Box pattern
        box_match = re.match(r'^Box (\d+)$', line)
        if box_match:
            current_box = {"box_number": int(box_match.group(1)), "series": []}
            library_data.append(current_box)
            continue
        
        # Series pattern
        series_match = re.match(r'^Series (\d+): (.+)$', line)
        if series_match:
            current_series = {
                "series_number": int(series_match.group(1)),
                "series_name": series_match.group(2),
                "folders": []
            }
            if current_box:
                current_box["series"].append(current_series)
            continue
        
        # Folder pattern
        folder_match = re.match(r'^Folder (\d+)$', line)
        if folder_match:
            current_folder = {
                "folder_number": int(folder_match.group(1)),
                "folder_content": ""
            }
            if current_series:
                current_series["folders"].append(current_folder)
            continue
        
        # Folder content pattern (anything that follows a folder and isn't a new box/series/folder)
        if current_folder and not (line.startswith('Box ') or line.startswith('Series ') or line.startswith('Folder ')):
            if current_folder["folder_content"]:
                current_folder["folder_content"] += " " + line
            else:
                current_folder["folder_content"] = line
    
    return library_data

def export_to_csv(library_data, output_file):
    """Export the library data to a CSV file"""
    with open(output_file, 'w', newline='') as csvfile:
        # Define the CSV columns
        fieldnames = ['Box Number', 'Series Number', 'Series Name', 'Folder Number', 'Folder Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        for box in library_data:
            box_num = box['box_number']
            for series in box['series']:
                series_num = series['series_number']
                series_name = series['series_name']
                for folder in series['folders']:
                    writer.writerow({
                        'Box Number': box_num,
                        'Series Number': series_num,
                        'Series Name': series_name,
                        'Folder Number': folder['folder_number'],
                        'Folder Content': folder['folder_content']
                    })

def main():
    # Change this path to where your library.md file is located
    input_file = '.research/library.md'
    json_output_file = 'library.json'
    csv_output_file = 'library.csv'
    
    try:
        library_data = parse_library_md(input_file)
        
        # Write to JSON file with nice formatting
        with open(json_output_file, 'w') as file:
            json.dump(library_data, file, indent=2)
        
        # Export to CSV
        export_to_csv(library_data, csv_output_file)
        
        print(f"Successfully converted {input_file} to {json_output_file} and {csv_output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 