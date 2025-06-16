import os
import csv
import rarfile
import time
import shutil

# Get Resource Path & Directory
script_dir = os.getcwd()
resource_dir = os.path.join(script_dir, "resources")
output_dir = os.path.join(script_dir, "output")
# os.mkdir(output_dir)


client_array = []

client_dir = os.path.join(resource_dir, "client")

# Check if the vendor directory exists
if os.path.exists(client_dir):
    print("✅ Vendor directory exists.")
    client_csv_files = os.listdir(client_dir)

    for filename in client_csv_files:
        if filename.lower().endswith(".csv"):
            full_path = os.path.join(client_dir, filename)
            print(f"🔎 Processing file: {full_path}")

            with open(full_path, mode="r", newline="", encoding="utf-8-sig") as csvfile:
                reader = csv.DictReader(csvfile, delimiter="|")

                # Normalize headers to strip BOMs and whitespace
                if reader.fieldnames:
                    headers = [
                        header.strip().lstrip("\ufeff") for header in reader.fieldnames
                    ]
                    print(f"📑 Headers: {headers}")

                    # Check for required headers
                    if "KUNNR" in headers and "Name1" in headers:
                        print("Required headers found. Extracting data...")

                        for row in reader:
                            selected_row = {
                                "KUNNR": row.get("KUNNR", "").strip(),
                                "Name1": row.get("Name1", "").strip(),
                            }
                            # print(selected_row)
                            client_array.append(selected_row)

                    else:
                        print(
                            f"Skipping {filename}: Missing 'LIFNR' or 'NAME1' header."
                        )
                else:
                    print(f"Skipping {filename}: No headers found.")
else:
    print("No Vendor File Found.")

for entry in client_array[:20]:
    print(entry)


# Now Loop over directory & Access each of the things
directories = []
skip_directory = {"vendor", "client"}


for entry in os.listdir(resource_dir):
    entry_path = os.path.join(resource_dir, entry)
    if os.path.isdir(entry_path) and entry not in skip_directory:
        directories.append(os.path.abspath(entry_path))

lookup_dict = {item['KUNNR']: item.get('Name1', ' ') for item in client_array}

records_data = set()
# Loop On over .csv and Update
for directory in directories:
    for item in os.listdir(directory):
        if item.lower().endswith(".csv"):
            full_path = os.path.join(directory, item)
            records_data.add(full_path)

for record in records_data:
    tmp_file = f"{record}.tmp"
    updated_rows = []
    print(f"🔧 Processing: {record}")

    with open(record, mode='r', newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        original_fields = [f.strip().lstrip('\ufeff') for f in reader.fieldnames or []]

        # Add 'CName' after 'KUNNR' if not already present
        if 'CName' not in original_fields:
            new_fields = []
            for field in original_fields:
                new_fields.append(field)
                if field == 'KUNNR':
                    new_fields.append('CName')
        else:
            new_fields = original_fields
        
        for row in reader:
            lifnr = row.get('KUNNR')
            row['CName'] = lookup_dict.get(lifnr, '')
            updated_rows.append(row)

    # Write to .tmp file
    with open(tmp_file, mode='w', newline='', encoding='utf-8') as tmp_outfile:
        writer = csv.DictWriter(tmp_outfile, fieldnames=new_fields, delimiter='|')
        writer.writeheader()
        writer.writerows(updated_rows)

    for attempt in range(5):
        try:
            shutil.move(tmp_file, record)
            print(f"✅ Updated: {record}")
            break
        except PermissionError:
            print(f"⏳ File locked. Retrying {attempt + 1}/5...")
            time.sleep(0.5)
    else:
        print(f"❌ Failed to update {record}. File may be in use.")
