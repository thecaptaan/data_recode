import csv
import os

# Resource Directory
project_dir = os.getcwd()
client_dir = os.path.join(project_dir, "resources", "client")

directories = []
client_record_data = set()


# Collect .csv files only
for entry in os.listdir(client_dir):
    full_path = os.path.join(client_dir, entry)
    if os.path.isfile(full_path) and entry.lower().endswith('.csv'):
        client_record_data.add(full_path)
print(client_record_data)

# csv label
client_csv_label = ['KUNNR', 'Name1',  'Name2']

# open .csv & write headers by stream
for client_csv in client_record_data:
    temp_file_path = client_csv + '.tmp'
    print(f"writing {client_csv}")
    with open(client_csv, mode='r', newline='', encoding='utf-8') as infile, \
            open(temp_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.reader(infile, delimiter='|')
        writer = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(client_csv_label)
        for row in reader:
            # Strip whitespace from each cell but preserve empty columns
            cleaned_row = [cell.strip() for cell in row]
            # Write row only if it has at least one non-empty cell
            if any(cleaned_row):
                writer.writerow(cleaned_row)
    os.replace(temp_file_path, client_csv)
