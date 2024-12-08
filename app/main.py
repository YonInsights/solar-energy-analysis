import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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
@st.cache_data
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

# Clean data: Handling anomalies and missing values (Comments column, etc.)
if 'Comments' in data.columns:
    data['Comments'].fillna('No Comment', inplace=True)
else:
    st.warning("No 'Comments' column found in the dataset.")

# Drop rows with missing key sensor readings (like GHI, DNI, DHI, etc.)
data.dropna(subset=['ghi', 'dni', 'dhi', 'tamb', 'moda', 'modb'], how='all', inplace=True)

# Calculate KPIs
average_ghi = data['ghi'].mean()
max_ghi = data['ghi'].max()
min_ghi = data['ghi'].min()

average_tamb = data['tamb'].mean()
max_tamb = data['tamb'].max()
min_tamb = data['tamb'].min()

max_moda = data['moda'].max()
max_modb = data['modb'].max()

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

# Time Series Analysis (Line charts)
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

# Evaluate the Impact of Cleaning on Sensor Readings
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

# Wind Analysis: Radial Plot / Wind Rose
st.subheader("Wind Analysis (Wind Speed & Direction)")

# Create a radial plot or wind rose for wind speed and direction
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)
wind_direction = data['wd'].dropna()
wind_speed = data['ws'].dropna()

ax.hist(np.deg2rad(wind_direction), bins=36, weights=wind_speed, color='b', alpha=0.7)
ax.set_title(f"Wind Rose for {selected_country}", fontsize=14)
ax.set_xlabel('Wind Direction (°)')
ax.set_ylabel('Wind Speed (m/s)')
st.pyplot(fig)

# Temperature Analysis: RH influence on temperature and solar radiation
st.subheader("Temperature and Relative Humidity Analysis")

# Scatter plot to examine how RH might influence temperature and solar radiation
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.scatterplot(data=data, x='rh', y='moda', ax=axes[0], color='blue', label='ModA')
sns.scatterplot(data=data, x='rh', y='ghi', ax=axes[1], color='green', label='GHI')
axes[0].set_title("Relative Humidity vs ModA")
axes[1].set_title("Relative Humidity vs GHI")
st.pyplot(fig)

# Histograms: GHI, DNI, DHI, WS, and Temperatures
st.subheader("Histograms of Solar Radiation and Wind Conditions")

# Plot histograms for solar radiation and temperature variables
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.histplot(data['ghi'], kde=True, ax=axes[0, 0], color='royalblue')
sns.histplot(data['dni'], kde=True, ax=axes[0, 1], color='orange')
sns.histplot(data['dhi'], kde=True, ax=axes[1, 0], color='green')
sns.histplot(data['ws'], kde=True, ax=axes[1, 1], color='red')

axes[0, 0].set_title('GHI Distribution')
axes[0, 1].set_title('DNI Distribution')
axes[1, 0].set_title('DHI Distribution')
axes[1, 1].set_title('Wind Speed Distribution')

st.pyplot(fig)

# Z-Score Analysis
st.subheader("Z-Score Analysis")

# Calculate Z-scores
z_scores = (data[correlation_columns] - data[correlation_columns].mean()) / data[correlation_columns].std()
outliers = z_scores[(z_scores > 3) | (z_scores < -3)]

# Plot Z-scores
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for i, col in enumerate(correlation_columns):
    ax = axes[i//3, i%3]
    sns.histplot(z_scores[col], kde=True, ax=ax, color='skyblue')
    ax.set_title(f"Z-scores for {col}")

st.pyplot(fig)

# Bubble Chart: GHI vs Tamb vs WS
st.subheader("Bubble Chart: GHI vs Tamb vs Wind Speed")

# Normalize bubble size (using RH for size)
size = data['rh'] / data['rh'].max() * 1000
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(data['ghi'], data['tamb'], s=size, c=data['ws'], cmap='viridis', alpha=0.6, edgecolors="w", linewidth=0.5)
fig.colorbar(scatter, label='Wind Speed (m/s)')
ax.set_xlabel('GHI (W/m²)')
ax.set_ylabel('Temperature (°C)')
ax.set_title(f"Bubble Chart for {selected_country}")
st.pyplot(fig)
