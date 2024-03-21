import csv


def combine_csv(csv1_file, csv2_file, output_file):
    # Read data from csv1
    with open(csv1_file, 'r', newline='', encoding='ISO-8859-1') as file1:
        csv1_reader = csv.DictReader(file1)
        csv1_data = list(csv1_reader)

    # Read data from csv2
    with open(csv2_file, 'r', newline='', encoding='ISO-8859-1') as file2:
        csv2_reader = csv.DictReader(file2)
        csv2_data = {row['Course code'] + row['Course number']: (row['Description'], row['Website']) for row in
                     csv2_reader}

    # Combine data and write to new csv
    with open(output_file, 'w', newline='', encoding='utf-8') as combined_file:
        fieldnames = list(csv1_data[0].keys()) + ['Description', 'Website']  # Add Description and Website headers
        writer = csv.DictWriter(combined_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in csv1_data:
            course_id = row['Subject'] + row['Catalog']
            if course_id in csv2_data:
                description, website = csv2_data[course_id]
                row['Description'] = description
                row['Website'] = website
            else:
                row['Description'] = 'Check academic program site'
                row['Website'] = ''
            writer.writerow(row)
# row['Description'] = ''
# row['Website'] = ''
if __name__ == '__main__':
    # Example usage
    csv1_file = 'openData/CU_SR_OPEN_DATA_CATALOG.csv'
    csv2_file = 'openData/CATALOG.csv'
    output_file = 'openData/OPENDATACOMBINED.csv'
    combine_csv(csv1_file, csv2_file, output_file)
