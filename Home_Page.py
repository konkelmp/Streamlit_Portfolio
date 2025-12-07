import requests
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Fire Systems - NASA FIRMS Data Visualization",
    page_icon="🔥 🌎 🔥",
    layout="centered"
)

st.title(" Welcome to My Streamlit Site")
st.markdown(
    """
    This is a Streamlit Dashboard app for displaying regional wildfire and air quality data
    - Preston Konkel

    Use the left sidebar switch regions and data time ranges.
    """
)

st.caption("Built with Streamlit")

# Cache FIRMS data for 24hrs
# FIRMS data contains last 3 days
@st.cache_data(ttl=86400)
def get_firms_data():            
    firms_url = f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/26af21577de6312527a09da2b7b3a18c/VIIRS_SNPP_NRT/world/3"
    try:
        firms_df = pd.read_csv(firms_url)
        last_refreshed = datetime.datetime.utcnow()
        return firms_df, last_refreshed
    except Exception as e:
        st.error("Failed to fetch FIRMS data.")
        return pd.DataFrame(), datetime.datetime.utcnow()

if "firms_df" not in st.session_state:
    st.session_state.firms_df = get_firms_data()

st.write("Rows loaded:", len(st.session_state.firms_df))
st.write(st.session_state.firms_df.head())

