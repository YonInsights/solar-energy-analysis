import pandas as pd

# Load the data
benin_data = pd.read_csv(r'D:\Kifya_training\Week 0\data\benin-malanville.csv')
sierraleone_data = pd.read_csv(r'D:\Kifya_training\Week 0\data\sierraleone-bumbuna.csv')
togo_data = pd.read_csv(r'D:\Kifya_training\Week 0\data\togo-dapaong_qc.csv')

# Display the first few rows of each dataset
print("Benin Data:")
print(benin_data.head())

print("\nSierra Leone Data:")
print(sierraleone_data.head())

print("\nTogo Data:")
print(togo_data.head())

# Check the data types and summary statistics
print("\nBenin Data Info:")
print(benin_data.info())
print("\nBenin Data Description:")
print(benin_data.describe())

print("\nSierra Leone Data Info:")
print(sierraleone_data.info())
print("\nSierra Leone Data Description:")
print(sierraleone_data.describe())

print("\nTogo Data Info:")
print(togo_data.info())
print("\nTogo Data Description:")
print(togo_data.describe())
