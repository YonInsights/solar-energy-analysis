import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

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

# Time Series Plot
st.subheader("Time Series for Solar Components")

# Create subplots for GHI, DNI, DHI, and Tamb
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle(f"Time Series Analysis for {selected_country}", fontsize=16)

# Plot GHI
data[['ghi']].plot(ax=axes[0, 0], title="Global Horizontal Irradiance (GHI)", legend=False)
axes[0, 0].set_ylabel('Irradiance (W/m²)')

# Plot DNI
data[['dni']].plot(ax=axes[0, 1], title="Direct Normal Irradiance (DNI)", legend=False)
axes[0, 1].set_ylabel('Irradiance (W/m²)')

# Plot DHI
data[['dhi']].plot(ax=axes[1, 0], title="Diffuse Horizontal Irradiance (DHI)", legend=False)
axes[1, 0].set_ylabel('Irradiance (W/m²)')

# Plot Tamb
data[['tamb']].plot(ax=axes[1, 1], title="Ambient Temperature (Tamb)", legend=False)
axes[1, 1].set_ylabel('Temperature (°C)')

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the plot in the Streamlit app
st.pyplot(fig)
