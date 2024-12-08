import streamlit as st
import pandas as pd
import os

# Dashboard title
st.title("Solar Energy Analysis Dashboard")

# Sidebar for selecting country
st.sidebar.header("Select Country")
selected_country = st.sidebar.selectbox("Choose a country:", list(["Benin", "Sierra Leone", "Togo"]), key="country_selectbox")

# Define the paths for the cleaned data
cleaned_data_dir = r"D:\Kifya_training\Week 0\solar-energy-analysis\data_cleaned"
cleaned_data_files = {
    "Benin": "benin_cleaned.csv",
    "Sierra Leone": "sierra_leone_cleaned.csv",
    "Togo": "togo_cleaned.csv"
}

# Function to load data for the selected country
@st.cache_data  # Use st.cache_data instead of the deprecated st.cache
def load_data(country):
    file_path = os.path.join(cleaned_data_dir, cleaned_data_files[country])
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])  # Ensure timestamp is in datetime format
    data.set_index('timestamp', inplace=True)  # Set timestamp as index
    return data

# Load and display data for the selected country
st.write(f"Displaying data for {selected_country}")
data = load_data(selected_country)

# Show the first few rows of the data
st.write(data.head())
