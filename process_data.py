import csv
import os

# Define paths for input and output directories/files
data_path = 'data'
output_path = 'data/processed_sales_data.csv'

# Read all three CSV files and combine them into a single list of rows
# Each row is stored as a dictionary with column names as keys
combined_rows = []
for i in range(3):
    # Build the file path for each of the three daily sales CSV files
    file_path = os.path.join(data_path, f'daily_sales_data_{i}.csv')
    # Open each file in read mode with UTF-8 encoding
    with open(file_path, 'r', newline='', encoding='utf-8') as f:
        # Create a DictReader to access columns by their header names
        reader = csv.DictReader(f)
        # Add each row from the file to our combined list
        for row in reader:
            combined_rows.append(row)

# Filter the combined data to keep only "pink morsel" products
# This removes rows for other products (gold, magenta, chartreuse, periwinkle)
filtered_rows = [row for row in combined_rows if row['product'] == 'pink morsel']

# Calculate the sales for each filtered row
# Sales = price multiplied by quantity
for row in filtered_rows:
    # Remove the '$' symbol from price and convert to float for calculations
    price = float(row['price'].replace('$', ''))
    # Convert quantity from string to integer
    quantity = int(row['quantity'])
    # Calculate and add the sales value to the row
    row['sales'] = price * quantity

# Select only the required columns (Sales, Date, Region) for output
# Reformat each row to use capitalized column names as specified
output_rows = [{'Sales': row['sales'], 'Date': row['date'], 'Region': row['region']} for row in filtered_rows]

# Write the processed data to the output CSV file
with open(output_path, 'w', newline='', encoding='utf-8') as f:
    # Create a DictWriter with the specified column order
    writer = csv.DictWriter(f, fieldnames=['Sales', 'Date', 'Region'])
    # Write the header row first
    writer.writeheader()
    # Write all the data rows
    writer.writerows(output_rows)

#  Print summary information about the data processing
print(f"Total rows in combined data: {len(combined_rows)}")
print(f"Rows after filtering for pink morsel: {len(output_rows)}")
print(f"\nOutput saved to: {output_path}")
print(f"\nSample of output data:")
# Print the first 10 rows as a sample of the output
for row in output_rows[:10]:
    print(row)
