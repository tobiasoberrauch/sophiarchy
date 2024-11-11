import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

# Load the combined CSV file
csv_filename = "./data/silver/Abgeordnete_Bundestag_All_Wahlperiode.csv"
df = pd.read_csv(csv_filename)

# Create the directory for saving the data if it doesn't exist
output_dir = "data/bronze"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each link in the "Link" column
for index, row in df.iterrows():
    person_name = row.get("Mitglied des Bundestages", row.get("Name"))  # Fallback if "Name" column is missing
    link = row.get("Link", None)
    
    if not link or link == "Kein Link verfügbar":
        print(f"Skipping {person_name} - no valid link available.")
        continue
    
    try:
        # Fetch the Wikipedia page for the person
        response = requests.get(link)
        response.raise_for_status()  # Check for HTTP errors
        
        # Parse the page content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the main content - usually found in the "mw-parser-output" div
        content_div = soup.find("div", {"class": "mw-parser-output"})
        if not content_div:
            print(f"No content found for {person_name} at {link}")
            continue
        
        # Collect all paragraphs of text within this section
        paragraphs = content_div.find_all("p")
        person_content = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # Save the extracted data to a text file named after the person
        filename = f"{person_name.replace(' ', '_')}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(person_content)
        
        print(f"Data for {person_name} has been saved to {filepath}.")
    
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred for {person_name}: {http_err}")
    except Exception as err:
        print(f"An error occurred for {person_name}: {err}")
