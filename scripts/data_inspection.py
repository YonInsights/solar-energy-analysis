import pandas as pd

# File paths
data_paths = {
    "Benin": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\benin-malanville.csv",
    "Sierra Leone": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\sierraleone-bumbuna.csv",
    "Togo": r"D:\Kifya_training\Week 0\solar-energy-analysis\data\togo-dapaong_qc.csv"
}

# Function to inspect the dataset
def inspect_dataset(file_path, country_name):
    print(f"Inspecting data for {country_name}...\n")

    # Load the dataset
    data = pd.read_csv(file_path)
    
    # Display the first few rows
    print(f"{country_name} - First 5 rows:")
    print(data.head(), "\n")

    # Check column names
    print(f"{country_name} - Column Names:")
    print(data.columns, "\n")
    
    # Check for missing values
    print(f"{country_name} - Missing Values:")
    print(data.isnull().sum(), "\n")
    
    # Check for duplicate rows
    duplicates = data.duplicated().sum()
    print(f"{country_name} - Duplicate Rows: {duplicates}\n")
    
    # Check data types and non-null counts
    print(f"{country_name} - Data Types and Non-Null Counts:")
    print(data.info(), "\n")
    
    # Summary statistics for numerical columns
    print(f"{country_name} - Summary Statistics:")
    print(data.describe(), "\n")

    # Investigate potential outliers in key numerical columns (e.g., GHI, DNI, Tamb)
    key_columns = ['GHI', 'DNI', 'DHI', 'Tamb', 'RH', 'WS', 'BP']
    for col in key_columns:
        if col in data.columns:
            outliers = data[col][(data[col] < data[col].quantile(0.01)) | (data[col] > data[col].quantile(0.99))]
            print(f"{country_name} - Outliers in {col}:")
            print(outliers.describe(), "\n")
    
    # Verify Timestamp column format
    if 'Timestamp' in data.columns:
        try:
            data['Timestamp'] = pd.to_datetime(data['Timestamp'])
            print(f"{country_name} - Timestamp column successfully converted to datetime.\n")
        except Exception as e:
            print(f"{country_name} - Error converting Timestamp column to datetime: {e}\n")
    else:
        print(f"{country_name} - No Timestamp column found.\n")
    
    print("=" * 50)

# Inspect datasets for each country
benin_data = inspect_dataset(data_paths["Benin"], "Benin")
sierraleone_data = inspect_dataset(data_paths["Sierra Leone"], "Sierra Leone")
togo_data = inspect_dataset(data_paths["Togo"], "Togo")
