import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from datetime import datetime, timedelta, date
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="DASHBOARD",
    page_icon="🔥 🌎 🔥",
    layout="wide"
)

firms_df = st.session_state.get("firms_df")

if firms_df is None or firms_df.empty:
    st.warning("No FIRMS data available. Please refresh from Home Page.")
    st.stop()
    
###########################################

# Sidebar
st.sidebar.title("Dashboard Filters")
region_select = st.sidebar.selectbox("Select Region", ["North America", "South America", "Europe", "Asia", "Africa", "Oceania"])
time_range_select = st.sidebar.selectbox("Select Time Range", ["Past Day", "Past 2 Days", "Past 3 Days"])
confidence_select = st.sidebar.selectbox("Select Confidence Level", ["All", "Low", "Nominal", "High"])

# Day Mapping
days = {"Past Day": 1,
        "Past 2 Days": 2,
        "Past 3 Days": 3}
days_back = days[time_range_select]
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
lon_min, lat_min, lon_max, lat_max = region_bounds[region_select]

# Confidence level mapping
confidences = {"All": "", "Low": "l", "Nominal": "n", "High": "h"}
confidence = confidences[confidence_select]

###########################################

firms_df['acq_date'] = pd.to_datetime(firms_df['acq_date']).dt.date
filtered_df = firms_df[firms_df['acq_date'] >= cutoff_date]

# Confidence filter
if confidence != "":
    filtered_df = filtered_df[filtered_df['confidence'] == confidence]

# Assign region based on lat/lon
def get_region(lat, lon):
    for region, (lon_min, lat_min, lon_max, lat_max) in region_bounds.items():
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return region
    return "Other"

filtered_df['region'] = filtered_df.apply(lambda row: get_region(row['latitude'], row['longitude']), axis=1)

# Group by region
region_counts = filtered_df['region'].value_counts().reset_index()
region_counts.columns = ['Region', 'Fire Count']

col1, col2 = st.columns([3, 2])

with col2:
    st.subheader("🔥 Fires by Region")
    st.bar_chart(region_counts.set_index('Region'))

# Filter by selected region for the map
region_df = filtered_df[filtered_df['region'] == region_select]

with col1:
    st.subheader(f"🔥 Fires in {region_select}")
    fire_map = folium.Map(location=[(lat_min + lat_max)/2, (lon_min + lon_max)/2], zoom_start=3)
    marker_cluster = MarkerCluster().add_to(fire_map)

    for _, row in region_df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            color='red',
            fill=True,
            fill_opacity=0.7,
            popup=f"Date: {row['acq_date']} | Confidence: {row['confidence']}"
        ).add_to(marker_cluster)

    st_folium(fire_map, width=500, height=350)

###########################################

#  KPI Metrics
st.subheader("📊 Key Metrics")

st.metric("Total Fires", len(filtered_df))
avg_frp = round(filtered_df['frp'].mean(), 2)
st.metric("Average Fire Radiative Power (FRP) in MegaWatts", avg_frp)

day_count = (filtered_df['daynight'] == "D").sum()
night_count = (filtered_df['daynight'] == "N").sum()
st.metric("Detection Day or Night", f"Day: {day_count} \n Night: {night_count}")

st.metric("Top Reporting Satellite", filtered_df['satellite'].mode()[0])
