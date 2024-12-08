import pandas as pd

# File paths
data_paths = {
    "Benin": r"D:\Kifya_training\Week 0\data\benin-malanville.csv",
    "Sierra Leone": r"D:\Kifya_training\Week 0\data\sierraleone-bumbuna.csv",
    "Togo": r"D:\Kifya_training\Week 0\data\togo-dapaong_qc.csv"
}

# Function to load and clean a dataset
def clean_dataset(file_path, country_name):
    print(f"Cleaning data for {country_name}...")
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Drop the Comments column (it contains no useful data)
    if 'Comments' in data.columns:
        data.drop(columns=['Comments'], inplace=True)
    
    # Replace negative values in solar radiation columns with 0
    solar_columns = ['GHI', 'DNI', 'DHI']
    for col in solar_columns:
        if col in data.columns:
            data[col] = data[col].apply(lambda x: max(x, 0))
    
    # Convert Timestamp column to datetime format
    if 'Timestamp' in data.columns:
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    
    # Display cleaning summary
    print(f"{country_name} - Data cleaned:")
    print(data.info())
    print(data.describe())
    print("-" * 50)
    
    return data

# Clean datasets
benin_data = clean_dataset(data_paths["Benin"], "Benin")
sierraleone_data = clean_dataset(data_paths["Sierra Leone"], "Sierra Leone")
togo_data = clean_dataset(data_paths["Togo"], "Togo")

# Combine datasets (optional)
all_data = pd.concat([benin_data, sierraleone_data, togo_data], ignore_index=True)
print("Combined Dataset:")
print(all_data.info())

# Save cleaned data to new files
benin_data.to_csv(r"D:\Kifya_training\Week 0\data\benin_cleaned.csv", index=False)
sierraleone_data.to_csv(r"D:\Kifya_training\Week 0\data\sierraleone_cleaned.csv", index=False)
togo_data.to_csv(r"D:\Kifya_training\Week 0\data\togo_cleaned.csv", index=False)
all_data.to_csv(r"D:\Kifya_training\Week 0\data\all_cleaned.csv", index=False)

print("Cleaned data saved to the 'data' folder.")
