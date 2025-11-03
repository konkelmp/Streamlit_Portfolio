import os
import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime, timedelta

DATA_PATH = "data/firms_last10days.csv"

def get_firms_data():
    today = date.today()
    # Check if file already exists and is recent (within 1 day)
    if os.path.exists(DATA_PATH):
        file_time = datetime.fromtimestamp(os.path.getmtime(DATA_PATH))
        if datetime.utcnow() - file_time < timedelta(hours=24):
            return pd.read_csv(DATA_PATH)
            
    FIRMS_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/26af21577de6312527a09da2b7b3a18c/VIIRS_SNPP_NRT/world/10/{today}"
    try:
        fire_df = pd.read_csv(FIRMS_url)
        os.makedirs("data", exist_ok=True)
        fire_df.to_csv(DATA_PATH, index=False)
        return fire_df
    except Exception as e:
        st.error("Failed to fetch FIRMS data.")
        return pd.DataFrame()

# Sidebar
st.sidebar.title("Dashboard Filters")
region = st.sidebar.selectbox("Select Region", ["North America", "South America", "Europe", "Asia", "Africa", "Pacifica"])
date = st.sidebar.selectbox("Select Date", ["Past Day", "Past 3 Days", "Past 10 Days"])

#  Region Mapping 
region_bounds = {
    "North America": [-170, 15, -50, 75],
    "South America": [-90, -60, -30, 15],
    "Europe": [-25, 35, 45, 70],
    "Asia": [60, 5, 150, 60],
    "Africa": [-20, -35, 55, 35],
    "Pacifica": [120, -50, -120, 50]
}

bbox = region_bounds[region]

fire_df = pd.read_csv("data/firms_data.csv")

#  Wildfire Choropleth Map
st.subheader("🔥 Wildfire Activity Map")
fire_map = folium.Map(location=[(bbox[1]+bbox[3])/2, (bbox[0]+bbox[2])/2], zoom_start=4)
for _, row in fire_df.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color='red',
        fill=True,
        fill_opacity=0.7
    ).add_to(fire_map)
st_folium(fire_map, width=700)


#  KPI Metrics
st.subheader("📊 Key Metrics")
st.metric("Total Fires", len(fire_df))

# ---------------- Line Chart ----------------
#if not aq_df.empty:
    #aq_chart_df = aq_df.groupby('parameter')['value'].mean().reset_index()
    #fig = px.bar(aq_chart_df, x='parameter', y='value', title="Average Pollutant Levels")
    #st.plotly_chart(fig, use_container_width=True)
