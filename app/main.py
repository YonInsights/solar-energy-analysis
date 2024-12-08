import streamlit as st
import pandas as pd
import os

# Set up paths
cleaned_data_dir = r"D:\Kifya_training\Week 0\solar-energy-analysis\data_cleaned"
cleaned_data_files = {
    "Benin": "benin_cleaned.csv",
    "Sierra Leone": "sierra_leone_cleaned.csv",
    "Togo": "togo_cleaned.csv"
}

# Load datasets function
@st.cache
def load_data(country):
    file_path = os.path.join(cleaned_data_dir, cleaned_data_files[country])
    data = pd.read_csv(file_path)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)
    return data

# Streamlit dashboard setup
st.title("Solar Energy Analysis Dashboard")
st.sidebar.header("Filter Options")
selected_country = st.sidebar.selectbox("Select Country", list(cleaned_data_files.keys()))

# Load and display data
st.write(f"Displaying data for {selected_country}")
data = load_data(selected_country)
st.write(data.head())
