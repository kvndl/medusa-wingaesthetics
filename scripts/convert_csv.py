import csv
import re
import collections

# Define the headers for the input and output CSV files
squarespace_headers = [
    'Token', 'Item Name', 'Variation Name', 'SKU', 'Description', 'Category', 'SEO Title', 'SEO Description',
    'Permalink', 'GTIN', 'Square Online Item Visibility', 'Item Type', 'Weight (lb)', 'Shipping Enabled',
    'Self-serve Ordering Enabled', 'Delivery Enabled', 'Pickup Enabled', 'Price', 'Online Sale Price', 'Sellable',
    'Stockable', 'Skip Detail Screen in POS', 'Option Name 1', 'Option Value 1', 'Current Quantity Wing Aesthetics & Acne Clinic',
    'New Quantity Wing Aesthetics & Acne Clinic', 'Stock Alert Enabled Wing Aesthetics & Acne Clinic',
    'Stock Alert Count Wing Aesthetics & Acne Clinic', 'Tax - Sales Tax (7%)'
]

medusajs_headers = [
    'Product Handle', 'Product Id', 'Product Title', 'Product Subtitle', 'Product Description', 'Product Status',
    'Product Thumbnail', 'Image 1 Url', 'Product Weight', 'Product Length', 'Product Width', 'Product Height',
    'Product HS Code', 'Product Origin Country', 'Product MID Code', 'Product Material', 'Product Discountable',
    'Product External Id', 'Product Profile Name', 'Product Profile Type', 'Product Collection Title',
    'Product Collection Handle', 'Product Type', 'Product Tags', 'Option 1 Name', 'Option 1 Value', 'Variant Id',
    'Variant Title', 'Variant SKU', 'Variant Barcode', 'Variant Inventory Quantity', 'Variant Allow Backorder',
    'Variant Manage Inventory', 'Variant Weight', 'Variant Length', 'Variant Width', 'Variant Height',
    'Variant HS Code', 'Variant Origin Country', 'Variant MID Code', 'Variant Material', 'Price USD',
    'Sales Channel 1 Id', 'Sales Channel 1 Name', 'Sales Channel 1 Description'
]

# Map Squarespace headers to MedusaJS headers
header_mapping = {
    'Item Name': 'Product Title',
    'Variation Name': 'Variant Title',
    'SKU': 'Variant SKU',
    'Description': 'Product Description',
    'Weight (lb)': 'Product Weight',
    'Price': 'Price USD',
    'Option Name 1': 'Option 1 Name',
    'Option Value 1': 'Option 1 Value'
}

# Default values for mandatory fields
default_values = {
    'Product Handle': 'unknown-handle',
    'Product Discountable': 'true',
    'Product Status': 'published',
    'Variant Inventory Quantity': '0',
    'Variant Manage Inventory': 'true',
    'Variant Allow Backorder': 'false'
}

# Function to generate product handle from title
def generate_handle(title):
    handle = title.lower()
    handle = re.sub(r'[^a-z0-9\s-]', '', handle)
    handle = re.sub(r'[\s-]+', '-', handle)
    return handle

def ensure_unique_variant_title(variant_titles, base_title):
    base_title = sanitize_variant_title(base_title)
    unique_title = base_title
    counter = 1
    while unique_title in variant_titles:
        unique_title = f"{base_title}-{counter}"
        counter += 1
    variant_titles.add(unique_title)
    return unique_title

def sanitize_variant_title(title):
    title = re.sub(r'\b(Color|Size|Material)\b', '', title, flags=re.IGNORECASE).strip()
    return title

def convert_squarespace_to_medusajs(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile, fieldnames=squarespace_headers)
        writer = csv.DictWriter(outfile, fieldnames=medusajs_headers)

        writer.writeheader()

        next(reader)  # Skip the header row of the input file

        variant_titles = set()

        for row in reader:
            new_row = {header: default_values.get(header, None) for header in medusajs_headers}  # Initialize fields with None or default values

            # Generate handle from product title
            new_row['Product Handle'] = generate_handle(row['Item Name']) if row['Item Name'] else default_values['Product Handle']

            # Map relevant fields from Squarespace to MedusaJS
            for ss_header, mj_header in header_mapping.items():
                if ss_header in row and row[ss_header]:
                    new_row[mj_header] = row[ss_header]

            # Ensure required fields are set to default values if missing
            new_row['Variant Inventory Quantity'] = new_row.get('Variant Inventory Quantity', default_values['Variant Inventory Quantity'])
            new_row['Variant Manage Inventory'] = new_row.get('Variant Manage Inventory', default_values['Variant Manage Inventory'])
            new_row['Variant Allow Backorder'] = new_row.get('Variant Allow Backorder', default_values['Variant Allow Backorder'])

            # Ensure unique variant titles
            base_variant_title = row.get('Variation Name', 'Regular')
            unique_variant_title = ensure_unique_variant_title(variant_titles, base_variant_title)
            new_row['Variant Title'] = unique_variant_title

            # Set Option Name and Value if they are empty
            if 'Option 1 Name' not in new_row or not new_row['Option 1 Name']:
                new_row['Option 1 Name'] = 'Color'  # Default to 'Color'
            if 'Option 1 Value' not in new_row or not new_row['Option 1 Value']:
                new_row['Option 1 Value'] = base_variant_title

            # Write the new row to the output CSV
            writer.writerow(new_row)

# Example usage
convert_squarespace_to_medusajs('input.csv', 'output.csv')
