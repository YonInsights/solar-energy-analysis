import pandas as pd
import os

# File paths for input and output
data_paths = {
    "Benin": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\benin-malanville.csv",
    "Sierra Leone": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\sierraleone-bumbuna.csv",
    "Togo": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\togo-dapaong_qc.csv"
}

output_directory = r"D:\Kifya_training\Week 0\solar-energy-analysis\data_cleaned"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to load and clean a dataset
def clean_dataset(file_path, country_name):
    print(f"Cleaning data for {country_name}...")

    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Standardize column names (lowercase and no spaces)
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]
    
    # Drop unnecessary columns
    if 'comments' in data.columns:
        data.drop(columns=['comments'], inplace=True)
    
    # Handle negative values in solar radiation columns by replacing with 0
    solar_columns = ['ghi', 'dni', 'dhi']
    for col in solar_columns:
        if col in data.columns:
            data[col] = data[col].apply(lambda x: max(x, 0))
    
    # Convert timestamp column to datetime format
    if 'timestamp' in data.columns:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
    
    # Drop duplicate rows
    initial_row_count = len(data)
    data.drop_duplicates(inplace=True)
    duplicate_count = initial_row_count - len(data)
    print(f"Removed {duplicate_count} duplicate rows from {country_name} data.")
    
    # Handle missing values (you can customize this based on business logic)
    data.fillna(method='ffill', inplace=True)  # Forward fill for continuity
    data.fillna(method='bfill', inplace=True)  # Backward fill for remaining gaps

    # Display cleaning summary
    print(f"{country_name} - Data cleaned:")
    print(data.info())
    print(data.describe())
    print("-" * 50)
    
    # Save the cleaned data to the output directory
    output_path = os.path.join(output_directory, f"{country_name.lower().replace(' ', '_')}_cleaned.csv")
    data.to_csv(output_path, index=False)
    print(f"Cleaned data for {country_name} saved to {output_path}")
    print("=" * 50)
    
    return data

# Clean datasets for each country
benin_data = clean_dataset(data_paths["Benin"], "Benin")
sierraleone_data = clean_dataset(data_paths["Sierra Leone"], "Sierra Leone")
togo_data = clean_dataset(data_paths["Togo"], "Togo")
