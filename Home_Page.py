import requests
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(
    page_title="Fire Systems - NASA FIRMS Data Visualization",
    page_icon="🔥 🌎 🔥",
    layout="centered"
)

st.title(" Welcome to Fire Systems - Streamlit App")
st.markdown(
    """
    This is a Streamlit Portofolio app for displaying regional fire data from NASA FIRMS API

    Use the sidebar navigation to start exploring.

    FIRMS API is called once a day and caches the last 3 days of data
    See data preview below

    Created by Preston Konkel
    """
)

# Cache FIRMS data for 24hrs
# FIRMS data contains last 3 days
@st.cache_data(ttl=86400)
def get_firms_data():            
    firms_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/26af21577de6312527a09da2b7b3a18c/VIIRS_SNPP_NRT/world/3"
    try:
        firms_df = pd.read_csv(firms_url)
        st.caption(f"🔄 Data last refreshed : {datetime.datetime.utcnow() - datetime.timedelta(hours=7)} MST")
        return firms_df
    except Exception as e:
        st.error("Failed to fetch FIRMS data.")
        return pd.DataFrame()

if "firms_df" not in st.session_state:
    st.session_state.firms_df = get_firms_data()

st.write("Rows loaded:", len(st.session_state.firms_df))
st.write(st.session_state.firms_df.head())

