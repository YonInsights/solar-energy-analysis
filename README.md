# Solar Energy Analysis and Dashboard Development  

This repository showcases my work on analyzing solar radiation data and developing a user-friendly dashboard. The project highlights my data analysis, visualization, and dashboarding skills using Python and Streamlit. It is part of my professional portfolio and demonstrates my ability to work on real-world datasets to generate actionable insights.

---

## Project Overview  

As part of a challenge, I analyzed solar radiation data from Benin, Sierra Leone, and Togo to identify regions with high potential for solar energy installations. The project included exploratory data analysis (EDA), data cleaning, statistical analysis, and interactive dashboard creation. The insights derived from this project can guide solar energy investment strategies for sustainable energy solutions.

---

## Objectives  

- Analyze solar radiation and environmental data to uncover trends and insights.  
- Identify key factors influencing solar energy potential.  
- Develop an interactive dashboard to visualize findings and enable decision-making.  

---

## Dataset Description  

The dataset used in this project contains various measurements related to solar radiation and environmental conditions, such as:  

- **GHI (Global Horizontal Irradiance):** Total solar radiation received on a horizontal surface.  
- **DNI (Direct Normal Irradiance):** Solar radiation received perpendicularly from the sun.  
- **DHI (Diffuse Horizontal Irradiance):** Scattered solar radiation received on a horizontal surface.  
- **Temperature and Humidity:** Ambient temperature and relative humidity values.  
- **Wind Conditions:** Wind speed, gusts, and direction.  
- **Cleaning Events:** Indicating whether solar panels or sensors were cleaned.  

For a full description of the data, visit the [Dataset Documentation](https://energydata.info/dataset/?q=Solar+Radiation+Measurement&vocab_regions=AFR).  

---

## Repository Structure  

```plaintext
├── .vscode/
│   └── settings.json             # VSCode settings  
├── .github/
│   └── workflows/
│       └── unittests.yml         # GitHub Actions for testing  
├── data/
│   └── solar_data.csv            # Raw dataset (not included in repo)  
├── notebooks/
│   ├── EDA.ipynb                 # Jupyter Notebook for exploratory data analysis  
├── scripts/
│   ├── data_cleaning.py          # Data cleaning script  
│   ├── visualization.py          # Visualization functions  
├── app/
│   ├── main.py                   # Streamlit dashboard application  
│   ├── utils.py                  # Utility functions for the app  
├── tests/
│   ├── test_cleaning.py          # Unit tests for data cleaning script  
├── README.md                     # Project documentation  
├── requirements.txt              # Python dependencies  
├── .gitignore                    # Files and folders to ignore  
# solar-energy-analysis
Analysis and visualization of solar radiation data to support sustainable energy strategies for MoonLight Energy Solutions.
