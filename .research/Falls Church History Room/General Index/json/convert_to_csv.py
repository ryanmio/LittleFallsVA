import json
import csv
import os
import glob

# Output CSV file
csv_file = 'merged_history_room_index.csv'

def array_to_json_string(arr):
    if not arr:
        return '[]'
    # Convert array to JSON string format
    return json.dumps(arr)

def extract_volume_number(filename):
    # Extract Vol_X from the filename
    try:
        vol_part = filename.split('Vol_')[1][0]  # Get the number after 'Vol_'
        return f"Volume {vol_part}"
    except:
        return "Unknown Volume"

try:
    # Find all JSON files matching the pattern
    json_files = glob.glob('IIIFScribe_General_Index_FCHR_Vol_*_2025*.json')
    
    if not json_files:
        print("No matching JSON files found!")
        exit(1)

    print(f"Found {len(json_files)} JSON files to process:")
    for file in json_files:
        print(f"- {file}")

    # Define CSV headers based on streamlined Supabase table structure
    headers = [
        'volume',
        'number',
        'title',
        'date_subject',
        'date_published',
        'graphics',
        'physical',
        'subject',
        'location',
        'abstract',
        'notes',
        'catalog_date',
        'catalog_by',
        'date_entered',
        'date_modified',
        'source_file'
    ]

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        
        total_records = 0
        
        # Process files in sorted order to ensure consistent processing
        for json_file in sorted(json_files):
            # Extract source name and volume info
            source_name = json_file.split('IIIFScribe_')[1].split('_2025')[0]
            volume = extract_volume_number(json_file)
            print(f"\nProcessing {source_name}...")
            
            # Read JSON data
            with open(json_file, 'r') as jf:
                data = json.load(jf)
                print(f"Found {len(data)} records in {json_file}")
                
                # Process each record
                for item in data:
                    # Map the fields from the JSON structure to our streamlined schema
                    row = {
                        'volume': volume,
                        'number': item.get('number', ''),
                        'title': item.get('title', ''),
                        'date_subject': item.get('dateSubject', ''),  # Using dateSubject instead of date
                        'date_published': item.get('datePublished', ''),  # Added datePublished mapping
                        'graphics': item.get('graphics', ''),
                        'physical': item.get('physical', ''),
                        'subject': array_to_json_string(item.get('subject', [])),
                        'location': array_to_json_string(item.get('location', [])),
                        'abstract': item.get('category', ''),
                        'notes': item.get('notes', ''),  # Added notes mapping
                        'catalog_date': item.get('catalogDate', ''),  # Fixed catalogDate mapping
                        'catalog_by': item.get('catalogBy', ''),  # Fixed catalogBy mapping
                        'date_entered': item.get('dateEntered', ''),
                        'date_modified': item.get('dateModified', ''),
                        'source_file': source_name
                    }
                    writer.writerow(row)
                    total_records += 1
                
                print(f"Processed {len(data)} records from {source_name}")

    print(f"\nMerge completed! Total records written to {csv_file}: {total_records}")
    print("\nYou can now import this CSV file into Supabase using the Table Editor:")
    print("1. Go to your Supabase project")
    print("2. Click on 'Table Editor'")
    print("3. Select the 'littlefalls_history_room_index' table")
    print("4. Click 'Import data'")
    print("5. Choose the generated CSV file")
    print("6. Make sure the column mappings match")
    print("\nNote: The 'subject' and 'location' columns are formatted as proper JSON arrays")

except Exception as e:
    print(f"Error: {str(e)}") 