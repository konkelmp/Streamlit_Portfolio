import streamlit as st
import pandas as pd
import folium
import plotly.express as px
from streamlit_folium import st_folium
from datetime import datetime, timedelta, date
from folium.plugins import MarkerCluster

firms_df = st.session_state.get("firms_df")

if firms_df is None or firms_df.empty:
    st.warning("No FIRMS data available. Please refresh or check the API.")
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

# Filter by region
filtered_df = firms_df[
    (firms_df['latitude'] >= lat_min) & (firms_df['latitude'] <= lat_max) &
    (firms_df['longitude'] >= lon_min) & (firms_df['longitude'] <= lon_max)
]

# Filter by date
filtered_df['acq_date'] = pd.to_datetime(filtered_df['acq_date']).dt.date
filtered_df = filtered_df[filtered_df['acq_date'] >= cutoff_date]

# Filter by confidence
if (confidence != ""):
    filtered_df = filtered_df[filtered_df['confidence'] == confidence]


###########################################

#  Wildfire Choropleth Map
st.subheader(f"🔥 Fires in {region_select}")
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

###########################################

#  KPI Metrics
st.subheader("📊 Key Metrics")

st.metric("Total Fires", len(filtered_df))
avg_frp = round(filtered_df['frp'].mean(), 2)
st.metric("Average Fire Radiative Power (FRP) in MegaWatts", avg_frp)

day_count = (filtered_df['daynight'] == "D").sum()
night_count = (filtered_df['daynight'] == "N").sum()
st.metric("Detection Day or Night", f"{day_count} / {night_count}")

st.metric("Top Reporting Satellite", filtered_df['satellite'].mode()[0])
