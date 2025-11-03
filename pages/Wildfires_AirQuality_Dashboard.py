import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
import plotly.express as px
from datetime import datetime, timedelta

# Sidebar
st.sidebar.title("Dashboard Filters")
region = st.sidebar.selectbox("Select Region", ["North America", "South America", "Europe", "Asia", "Africa", "Pacifica"])
selected_date = st.sidebar.date_input(
    "Select Start Date",
    value=datetime.utcnow().date() - timedelta(days=1),
    min_value=datetime.utcnow().date() - timedelta(days=30),
    max_value=datetime.utcnow().date()
)
start_str = selected_date.strftime("%Y-%m-%d")

# ---------------- Region Mapping ----------------
region_bounds = {
    "North America": [-170, 15, -50, 75],
    "South America": [-90, -60, -30, 15],
    "Europe": [-25, 35, 45, 70],
    "Asia": [60, 5, 150, 60],
    "Africa": [-20, -35, 55, 35],
    "Pacifica": [120, -50, -120, 50]
}

bbox = region_bounds[region]

# ---------------- Wildfire Data (NASA FIRMS) ----------------
fire_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/26af21577de6312527a09da2b7b3a18c/VIIRS_SNPP_NRT/world/10"
fire_df = pd.read_csv(fire_url)


#aq_url = f"https://api.openaq.org/v2/measurements?date_from={start_str}&limit=10000&coordinates={bbox[1]},{bbox[0]}"
#aq_response = requests.get(aq_url).json()
#aq_df = pd.DataFrame(aq_response['results'])
##

# ---------------- Wildfire Map ----------------
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

# ---------------- Air Quality Map ----------------
#st.subheader("🌫️ Air Quality Map")
#aq_map = folium.Map(location=[(bbox[1]+bbox[3])/2, (bbox[0]+bbox[2])/2], zoom_start=4)
#for _, row in aq_df.iterrows():
#    folium.CircleMarker(
#        location=[row['coordinates']['latitude'], row['coordinates']['longitude']],
#        radius=3,
#        color='blue',
#        fill=True,
#        fill_opacity=0.6,
#        popup=f"{row['parameter']}: {row['value']} {row['unit']}"
#    ).add_to(aq_map)
#st_folium(aq_map, width=700)

# ---------------- KPI Metrics ----------------
st.subheader("📊 Key Metrics")
st.metric("Total Fires", len(fire_df))
#st.metric("Air Quality Samples", len(aq_df))

# ---------------- Line Chart ----------------
#if not aq_df.empty:
    #aq_chart_df = aq_df.groupby('parameter')['value'].mean().reset_index()
    #fig = px.bar(aq_chart_df, x='parameter', y='value', title="Average Pollutant Levels")
    #st.plotly_chart(fig, use_container_width=True)
