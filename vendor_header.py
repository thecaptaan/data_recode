import csv
import os

project_dir = os.getcwd()
resource_dir = os.path.join(project_dir, "resources")
print(resource_dir)

directories = []
records_data = []

skip_directory = {"vendor", "client"}

for entry in os.listdir(resource_dir):
    entry_path = os.path.join(resource_dir, entry)
    if os.path.isdir(entry_path) and entry not in skip_directory:
        directories.append(os.path.abspath(entry_path))
for directory in directories:
    for item in os.listdir(directory):
        if item.lower().endswith('.csv'):
            records_data.append(f"{directory}/{item}")


csv_label = ['RBUKRS', 'GJAHR', 'BELNR', 'DOCLN', 'RACCT', 'HSL',
             'BUDAT', 'BLDAT', 'FISCYEARPER', 'BSCHL', 'KUNNR', 'LIFNR']

for record in records_data:
    temp_file_path = record + '.tmp'
    with open(record, mode='r', newline='', encoding='utf-8') as infile, \
            open(temp_file_path, mode='w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile, delimiter='|')
        writer = csv.writer(outfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)

        writer.writerow(csv_label)

        for row in reader:
            # Strip whitespace from each cell but preserve empty columns
            cleaned_row = [cell.strip() for cell in row]

            # Write row only if it has at least one non-empty cell
            if any(cleaned_row):
                writer.writerow(cleaned_row)

    os.replace(temp_file_path, record)
