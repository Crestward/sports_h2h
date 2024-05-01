import os
import glob
import csv
from datetime import datetime

comp = 'league2'
# Set the directory where the CSV files are located
directory = f'data/{comp}/'

# Get a list of all CSV files in the directory
csv_files = glob.glob(os.path.join(directory, '*.csv'))

# Create a new CSV file to store the merged data
output_file = f'data/{comp}/{comp}_merged_data.csv'

# List of possible date formats
date_formats = ['%m/%d/%y', '%d/%m/%Y', '%d/%m/%y', '%m/%d/%Y']

# Function to convert date string to datetime object
def convert_date(date_str):
    for date_format in date_formats:
        try:
            return datetime.strptime(date_str, date_format).date()
        except ValueError:
            pass
    return None

# List to store all rows
all_rows = []

# List to store all column names
all_columns = []

# Loop through each CSV file and append its rows
for csv_file in csv_files:
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Read the header of each file
        header = next(reader)
        # Update the list of all columns
        all_columns.extend([col for col in header if col not in all_columns])
        # Find the index of the date column
        date_col_index = header.index('date') if 'date' in header else None
        # Check if the file has a 'Time' column
        has_time_column = 'Time' in header

        # Loop through each row
        for row in reader:
            # Convert the date column to datetime object
            if date_col_index is not None:
                date_str = row[date_col_index]
                date_obj = convert_date(date_str)
                if date_obj:
                    row[date_col_index] = date_obj.isoformat()
                else:
                    row[date_col_index] = 'NaN'

            # Insert 'NaN' for the 'Time' column if the file doesn't have it
            if not has_time_column:
                row.insert(2, 'NaN')

            # Fill missing values with 'NaN' for that cell
            for index, value in enumerate(row):
                if not value.strip():
                    row[index] = 'NaN'

            # Append the modified row to the list
            all_rows.append(row)

# Sort the list based on the date column
all_rows.sort(key=lambda x: x[date_col_index] if date_col_index is not None else '')

# Insert the 'Time' column at index 2 in all_columns
all_columns.insert(2, 'Time')

# Write the merged data to the new CSV file
with open(output_file, 'w', newline='') as output_file:
    # Initialize a writer object
    writer = csv.writer(output_file)
    # Write the merged header
    writer.writerow(all_columns)
    # Write the sorted rows
    writer.writerows(all_rows)

print(f"Merged data has been written to {output_file}")