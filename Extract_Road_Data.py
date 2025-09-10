import xml.etree.ElementTree as ET
import csv

def extract_edge_details(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # List to store extracted details
    edge_details = []

    # Iterate over each 'edge' element
    for edge in root.findall('.//edge'):
        # Extract 'from', 'to', and 'shape' attributes from the edge
        from_id = edge.get('from')
        to_id = edge.get('to')
        shape = edge.get('shape')

        # Store the extracted details in a dictionary
        detail = {
            'From': from_id,
            'To': to_id,
            'Shape': shape
        }
        edge_details.append(detail)

    return edge_details

def save_edges_to_csv(details, output_file):
    # Define the CSV column names
    fieldnames = ['From', 'To', 'Shape']
    
    # Open the output CSV file in write mode
    with open(output_file, mode='w', newline='') as csvfile:
        # Create a writer object with the specified fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the rows of extracted details
        for detail in details:
            writer.writerow(detail)

# Usage
file_path = '31-Cologne1000v.net.xml'  # Replace with your actual XML file path
output_csv = 'edges_data.csv'  # Specify the output CSV file name

# Extract details from XML
edge_details = extract_edge_details(file_path)

# Save the extracted details to CSV
save_edges_to_csv(edge_details, output_csv)

print(f"Edge data saved to {output_csv}")
