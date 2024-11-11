import requests
from bs4 import BeautifulSoup
import csv

# Base URL for the Wikipedia page
base_url = "https://de.wikipedia.org/wiki/Liste_der_Mitglieder_des_Deutschen_Bundestages_({}._Wahlperiode)"

# Function to find the table under a specific heading
def get_table_under_heading(soup, heading_text):
    # Search for all headings and look for the specified heading text
    headings = soup.find_all(["h2", "h3"])  # Adjust depending on the actual heading structure
    
    for heading in headings:
        if heading_text in heading.get_text():
            # The next found "wikitable" after the heading
            next_table = heading.find_next("table", {"class": "wikitable"})
            return next_table
    return None

# Loop through Wahlperiode 1 to 20
for wahlperiode in range(1, 21):
    # Construct the URL for the current Wahlperiode
    url = base_url.format(wahlperiode)
    response = requests.get(url)
    
    # Check if the page was successfully retrieved
    if response.status_code != 200:
        print(f"Page for Wahlperiode {wahlperiode} not found.")
        continue
    
    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Retrieve the table under the "Abgeordnete" heading
    table = get_table_under_heading(soup, "Abgeordnete")
    
    # Check if the table was found
    if not table:
        print(f"No table found for Wahlperiode {wahlperiode}.")
        continue
    
    # CSV file name
    csv_filename = f"./data/bronze/Abgeordnete_Bundestag_{wahlperiode}_Wahlperiode.csv"
    base_link_url = "https://de.wikipedia.org"  # Base URL for relative links
    
    # Extract rows and write to CSV
    rows = table.find_all("tr")
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write the header row
        header = ["Wahlperiode"]  # Add Wahlperiode as the first column
        header.extend([col.get_text(strip=True) for col in rows[0].find_all(["th", "td"])])
        header.append("Link")  # Add a column for Links
        writer.writerow(header)
        
        # Write data rows
        for row in rows[1:]:  # Skip the header row
            columns = row.find_all(["th", "td"])
            row_text = [col.get_text(strip=True) for col in columns]
            
            # Find the name cell and link
            link = "Kein Link verfügbar"
            if len(columns) > 1:
                name_cell = columns[1] if wahlperiode > 18 else columns[0]
                for a_tag in name_cell.find_all("a", href=True):
                    href = a_tag["href"]
                    if not href.endswith((".jpg", ".jpeg", ".png", ".svg")):
                        link = base_link_url + href
                        break
            
            # Prepend the Wahlperiode and append the link to each row
            row_text.insert(0, wahlperiode)  # Insert Wahlperiode as the first column
            row_text.append(link)  # Append link as the last column
            writer.writerow(row_text)
    
    print(f"The table for Wahlperiode {wahlperiode} has been successfully saved as '{csv_filename}'.")
