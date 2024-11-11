import pandas as pd
import glob

# Load all CSV files from the bronze folder
all_files = glob.glob("./data/bronze/Abgeordnete_Bundestag_*_Wahlperiode.csv")

# List to hold data frames for each CSV file
dataframes = []

# Loop through each file and append its DataFrame to the list
for file in all_files:
    df = pd.read_csv(file)
    dataframes.append(df)

# Concatenate all dataframes into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Save the combined DataFrame to a single CSV file
combined_csv_filename = "./data/silver/Abgeordnete_Bundestag_All_Wahlperiode.csv"
combined_df.to_csv(combined_csv_filename, index=False, encoding="utf-8")

print(f"All CSV files have been combined and saved as '{combined_csv_filename}'.")
