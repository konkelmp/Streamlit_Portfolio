import streamlit as st

st.set_page_config(
    page_title="My Streamlit Site",
    page_icon="📊",
    layout="wide"
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
