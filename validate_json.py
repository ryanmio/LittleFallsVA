import json

file_path = 'IIIFScribe_General_Index_FCHR_Vol_1_2025-04-01T12-28-45.json'

try:
    with open(file_path, 'r') as file:
        data = json.load(file)
        print("JSON is valid.")
        
        if isinstance(data, list):
            print(f"Number of records: {len(data)}")
            if len(data) > 0:
                print("\nSample of first record:")
                # Print only a part of the first record to avoid overwhelming output
                sample = json.dumps(data[0], indent=2)[:500]
                print(f"{sample}...")
                # Print keys in the first record
                print("\nKeys in first record:")
                for key in data[0].keys():
                    print(f"- {key}")
        else:
            print(f"JSON content structure: {type(data)}")
            
except json.JSONDecodeError as e:
    print(f"JSON is invalid: {e}")
except Exception as e:
    print(f"Error: {e}") 