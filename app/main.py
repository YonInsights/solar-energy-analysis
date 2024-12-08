import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

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

# Calculate KPIs
average_ghi = data['ghi'].mean()
max_ghi = data['ghi'].max()
average_tamb = data['tamb'].mean()
max_tamb = data['tamb'].max()
max_moda = data['moda'].max()

# Display KPIs using st.metric in a horizontal layout box
st.markdown("<h2 style='text-align: center; font-weight: bold;'>Key Performance Indicators (KPIs)</h2>", unsafe_allow_html=True)

# Using columns to display KPIs in horizontal layout
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div style='text-align: center; font-weight: bold;'>Average GHI (W/m²)</div>", unsafe_allow_html=True)
    st.metric("", f"{average_ghi:.2f}", delta="")
    
with col2:
    st.markdown("<div style='text-align: center; font-weight: bold;'>Max Temperature (°C)</div>", unsafe_allow_html=True)
    st.metric("", f"{max_tamb:.2f}", delta="")
    
with col3:
    st.markdown("<div style='text-align: center; font-weight: bold;'>Max ModA (Value)</div>", unsafe_allow_html=True)
    st.metric("", f"{max_moda:.2f}", delta="")

# Time Series Plot
st.subheader("Time Series for Solar Components")

# Create subplots for GHI, DNI, DHI, and Tamb
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle(f"Time Series Analysis for {selected_country}", fontsize=16)

# Plot GHI with attractive color
data[['ghi']].plot(ax=axes[0, 0], title="Global Horizontal Irradiance (GHI)", color='royalblue', legend=False)
axes[0, 0].set_ylabel('Irradiance (W/m²)')

# Plot DNI with attractive color
data[['dni']].plot(ax=axes[0, 1], title="Direct Normal Irradiance (DNI)", color='orange', legend=False)
axes[0, 1].set_ylabel('Irradiance (W/m²)')

# Plot DHI with attractive color
data[['dhi']].plot(ax=axes[1, 0], title="Diffuse Horizontal Irradiance (DHI)", color='green', legend=False)
axes[1, 0].set_ylabel('Irradiance (W/m²)')

# Plot Tamb with attractive color
data[['tamb']].plot(ax=axes[1, 1], title="Ambient Temperature (Tamb)", color='red', legend=False)
axes[1, 1].set_ylabel('Temperature (°C)')

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the plot in the Streamlit app
st.pyplot(fig)

# Correlation Matrix
st.subheader("Correlation Matrix")

# Select columns for correlation analysis
correlation_columns = ['ghi', 'dni', 'dhi', 'moda', 'modb']
correlation_data = data[correlation_columns]

# Calculate correlation matrix
corr_matrix = correlation_data.corr()

# Display the correlation matrix as a heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True, linewidths=0.5, linecolor='black')
plt.title(f"Correlation Matrix for {selected_country} (Solar Radiation & Temperature)", fontsize=14)
st.pyplot(plt)

# Pair Plot
st.subheader("Pair Plot for Solar Components and Temperature")

# Plot pair plot for selected columns
sns.pairplot(correlation_data, kind='scatter', diag_kind='kde', hue='ghi', palette='Blues')
plt.suptitle(f"Pair Plot for {selected_country} (Solar Radiation & Temperature)", fontsize=14)
st.pyplot(plt)

# Impact of Cleaning on ModA and ModB
st.subheader("Impact of Cleaning on Sensor Readings (ModA and ModB)")

# Filter the data for cleaned and uncleaned data
cleaned_data = data[data['cleaning'] == 1]
uncleaned_data = data[data['cleaning'] == 0]

# Create subplots for ModA and ModB
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
fig.suptitle(f"Impact of Cleaning on ModA and ModB for {selected_country}", fontsize=16)

# Plot ModA with attractive color
axes[0].plot(cleaned_data.index, cleaned_data['moda'], label='Cleaned', color='blue')
axes[0].plot(uncleaned_data.index, uncleaned_data['moda'], label='Uncleaned', color='orange')
axes[0].set_title("ModA Sensor Readings")
axes[0].set_ylabel('ModA Value')
axes[0].legend()

# Plot ModB with attractive color
axes[1].plot(cleaned_data.index, cleaned_data['modb'], label='Cleaned', color='blue')
axes[1].plot(uncleaned_data.index, uncleaned_data['modb'], label='Uncleaned', color='orange')
axes[1].set_title("ModB Sensor Readings")
axes[1].set_ylabel('ModB Value')
axes[1].legend()

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Display the plot in the Streamlit app
st.pyplot(fig)
