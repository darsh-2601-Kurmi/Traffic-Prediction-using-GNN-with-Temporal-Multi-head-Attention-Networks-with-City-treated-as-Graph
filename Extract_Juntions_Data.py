import xml.etree.ElementTree as ET
import csv

def extract_junction_details(file_path):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # List to store extracted details
    junction_details = []

    # Iterate over each 'junction' element
    for junction in root.findall('.//junction'):
        # Extract 'id', 'x', and 'y' attributes from the junction
        node_id = junction.get('id')
        x = junction.get('x')
        y = junction.get('y')

        # Store the extracted details in a dictionary
        detail = {
            'Node': node_id,
            'x': x,
            'y': y
        }
        junction_details.append(detail)

    return junction_details

def save_junctions_to_csv(details, output_file):
    # Define the CSV column names
    fieldnames = ['Node', 'x', 'y']
    
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
output_csv = 'junctions.csv'  # Specify the output CSV file name

# Extract details from XML
junction_details = extract_junction_details(file_path)

# Save the extracted details to CSV
save_junctions_to_csv(junction_details, output_csv)

print(f"Junction data saved to {output_csv}")
