import json
import os
from supabase import create_client
import time
import glob

# Supabase configuration
SUPABASE_URL = "https://vysolznykhmtyyfwetwn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ5c29sem55a2htdHl5ZndldHduIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDAyMjg4OTYsImV4cCI6MjA1NTgwNDg5Nn0.4MM0v4LkYHxm62-TMNwDyauZ-H62mJJNNac2GvJhMqA"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def process_json_file(json_file):
    try:
        # Extract source name from filename
        source_name = json_file.split('IIIFScribe_')[1].split('_2025')[0]
        print(f"\nProcessing {source_name}...")

        # Read JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)
            print(f"Successfully loaded {len(data)} records from {json_file}")

        # Process data for Supabase
        processed_data = []
        for item in data:
            record = {
                'record_number': item.get('number', ''),
                'title': item.get('title', ''),
                'date': item.get('date', ''),
                'document_owner': item.get('documentOwner', ''),
                'graphics': item.get('graphics', ''),
                'physical': item.get('physical', ''),
                'subject': item.get('subject', []),  # Supabase handles arrays directly
                'location': item.get('location', []),  # Supabase handles arrays directly
                'category': item.get('category', ''),
                'date_entered': item.get('dateEntered', ''),
                'date_modified': item.get('dateModified', ''),
                'source_file': source_name
            }
            processed_data.append(record)

        # Insert data in batches
        batch_size = 50
        total_records = len(processed_data)
        successful_inserts = 0

        print(f"Inserting {total_records} records in batches of {batch_size}...")

        for i in range(0, total_records, batch_size):
            batch = processed_data[i:i + batch_size]
            try:
                response = supabase.table('littlefalls_history_room_index').insert(batch).execute()
                successful_inserts += len(batch)
                print(f"Inserted batch {i//batch_size + 1}/{(total_records + batch_size - 1)//batch_size} - Progress: {successful_inserts}/{total_records}")
                time.sleep(0.5)  # Small delay to avoid overwhelming the server
            except Exception as e:
                print(f"Error inserting batch {i//batch_size + 1}: {str(e)}")

        print(f"Completed processing {source_name}. Successfully inserted {successful_inserts} records.")
        return successful_inserts

    except Exception as e:
        print(f"Error processing {json_file}: {str(e)}")
        return 0

def main():
    # Find all JSON files matching the pattern
    json_files = glob.glob('IIIFScribe_General_Index_FCHR_Vol_*_2025*.json')
    
    if not json_files:
        print("No matching JSON files found!")
        return

    print(f"Found {len(json_files)} JSON files to process:")
    for file in json_files:
        print(f"- {file}")

    total_records_inserted = 0
    for json_file in sorted(json_files):  # Process files in order
        records_inserted = process_json_file(json_file)
        total_records_inserted += records_inserted

    print(f"\nImport completed! Total records inserted: {total_records_inserted}")

if __name__ == "__main__":
    main() 