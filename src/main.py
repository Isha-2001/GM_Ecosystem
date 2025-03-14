import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static

# Constants
DATA_FILE = "data/companies_ai_cybersecurity_raw.csv"

# Function to geocode addresses
def geocode(address):
    try:
        geolocator = Nominatim(user_agent="company_locator")
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    except:
        return None

# Streamlit app
st.title("Company Locator Dashboard")

# Load existing data
if st.button("Load Companies Data"):
    df = pd.read_csv(DATA_FILE)
    st.success(f"Loaded {len(df)} companies.")
else:
    df = pd.DataFrame()  # Start with an empty DataFrame

# Display DataFrame if loaded
if not df.empty:
    st.subheader("Company Data")
    st.dataframe(df)

    # Geocode addresses
    df['Coordinates'] = df['Registered Office Address'] + ', ' + df['Locality'] + ', ' + df['Postal Code']
    df['Location'] = df['Coordinates'].apply(geocode)
    df[['Latitude', 'Longitude']] = df['Location'].apply(pd.Series)

    # Create a base map
    m = folium.Map(location=[54.0, -5.0], zoom_start=6)

    # Add markers for each company
    for index, row in df.iterrows():
        if row['Location'] is not None:
            folium.Marker(
                location=row['Location'],
                popup=row['Company Name'],
                icon=folium.Icon(color='blue')
            ).add_to(m)

    # Display map in Streamlit
    folium_static(m)

    # Add filters for company data
    company_types = df['Company Type'].unique()
    selected_type = st.selectbox("Select Company Type", ["All"] + list(company_types))

    if selected_type != "All":
        df = df[df['Company Type'] == selected_type]
        st.subheader(f"Filtered Data: {selected_type}")
        st.dataframe(df)
else:
    st.warning("No company data available.")

