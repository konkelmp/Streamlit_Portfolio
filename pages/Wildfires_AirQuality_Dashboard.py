import os
import streamlit as st
import pandas as pd
import requests
import folium
import plotly.express as px
from streamlit_folium import st_folium
from datetime import datetime, timedelta, date
from folium.plugins import MarkerCluster

DATA_PATH = "data/firms_data.csv"

# Cache FIRMS data for 24hrs
# FIRMS data contains last 3 days
@st.cache_data(ttl=86400)
def get_firms_data():            
    firms_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/26af21577de6312527a09da2b7b3a18c/VIIRS_SNPP_NRT/world/3"
    try:
        firms_df = pd.read_csv(firms_url)
        os.makedirs("data", exist_ok=True)
        firms_df.to_csv(DATA_PATH, index=False)
        return firms_df
    except Exception as e:
        st.error("Failed to fetch FIRMS data.")
        return pd.DataFrame()

if "firms_df" not in st.session_state:
    st.session_state.firms_df = get_firms_data()
firms_df = st.session_state.firms_df

# Sidebar
st.sidebar.title("Dashboard Filters")
region = st.sidebar.selectbox("Select Region", ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"])
time_range = st.sidebar.selectbox("Select Time Range", ["Past Day", "Past 2 Days", "Past 3 Days"])

days = {"Past Day": 1,
        "Past 2 Days": 2,
        "Past 3 Days": 3}
        
days_back = days[time_range]
cutoff_date = datetime.utcnow().date() - timedelta(days=days_back)

#  Region Mapping 
region_bounds = {
    "North America": [-170, 15, -50, 75],
    "South America": [-90, -60, -30, 15],
    "Europe": [-25, 35, 45, 70],
    "Asia": [60, 5, 150, 60],
    "Africa": [-20, -35, 55, 35],
    "Oceania": [110, -50, 180, 10]
}
lon_min, lat_min, lon_max, lat_max = region_bounds[region]

# Filter by region
filtered_df = firms_df[
    (firms_df['latitude'] >= lat_min) & (firms_df['latitude'] <= lat_max) &
    (firms_df['longitude'] >= lon_min) & (firms_df['longitude'] <= lon_max)
]

# Filter by date
filtered_df['acq_date'] = pd.to_datetime(filtered_df['acq_date']).dt.date
filtered_df = filtered_df[filtered_df['acq_date'] >= cutoff_date]

#  Wildfire Choropleth Map
st.subheader(f"🔥 Wildfires in {region}")
fire_map = folium.Map(location=[(lat_min + lat_max)/2, (lon_min + lon_max)/2], zoom_start=3)
marker_cluster = MarkerCluster().add_to(fire_map)

for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.7,
        popup=f"Date: {row['acq_date']}"
    ).add_to(marker_cluster)

st_folium(fire_map, width=700)


#  KPI Metrics
st.subheader("📊 Key Metrics")
st.metric("Total Fires", len(filtered_df))
