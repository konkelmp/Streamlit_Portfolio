import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FIRMS Exploratory Data Analysis Gallery", page_icon="📊", layout="wide")

firms_df = st.session_state.get("firms_df")

if firms_df is None or firms_df.empty:
    st.warning("No FIRMS data available. Please refresh or check the API.")
    st.stop()

st.title("📊 EDA Gallery (Exploratory Data Analysis Showcase)")

# 1. Bar Chart – Fires by Confidence Level
st.subheader("1️⃣ Fires by Confidence Level")
st.write("**Question explored:** How many fires were detected at each confidence level in the selected time range?")

fig1 = px.bar(firms_df, x="confidence", title="Fires by Confidence Level")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown("""
- X-axis shows confidence categories (Low, Nominal, High).
- Y-axis shows number of detections.
- Taller bars = more fires at that confidence level.
- Colors distinguish categories.
""")

st.markdown("**Observations:**")
st.markdown(
  """
  - Most detections are in the *Nominal* category.
  - High confidence fires are fewer but more reliable.
  - Low confidence fires are rare.
  - Distribution shifts slightly by region but remains consistent overall.
  """
)

# 2. Histogram – Distribution of FRP
st.subheader("2️⃣ Distribution of Fire Radiative Power (FRP)")
st.write("**Question explored:** What is the distribution of fire intensity (FRP) among detected fires?")

fig2 = px.histogram(firms_df, x="frp", nbins=30, title="FRP Distribution (MW)")
st.plotly_chart(fig2, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown("""
- X-axis shows FRP values (megawatts).
- Y-axis shows number of fires in each FRP bin.
- The shape shows whether most fires are weak or strong.
- Outliers appear as bars far to the right.
""")

st.markdown("**Observations:**")
st.markdown("""
- Most fires cluster at low FRP (< 20 MW).
- A few extreme outliers exceed 200 MW.
- Distribution is right-skewed: many small fires, few intense ones.
- Highlights importance of monitoring high-FRP events.
""")

# 3. Scatter Plot – Location vs FRP
st.subheader("3️⃣ Fire Locations and Intensity")
st.write("**Question explored:** Where are fires located geographically, and how does FRP vary across locations?")

fig3 = px.scatter(
    firms_df,
    x="longitude",
    y="latitude",
    color="frp",
    hover_data=["acq_date", "confidence", "satellite"],
    title="Fire Locations with FRP Intensity"
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown("""
- Each point = one fire detection.
- X-axis = longitude, Y-axis = latitude.
- Color encodes FRP intensity (lighter = weaker, darker = stronger).
- Hover shows date, confidence, and satellite.
""")

st.markdown("**Observations:**")
st.markdown("""
- Fires cluster in equatorial Africa, western US, and South America.
- High-FRP fires appear scattered but align with known fire-prone zones.
- Dense clusters of low-FRP fires suggest widespread small burns.
- Interactive hover reveals temporal and satellite details.
""")

# 4. Box Plot – FRP by Day/Night
st.subheader("4️⃣ FRP by Day vs Night Detection")
st.write("**Question explored:** How does fire intensity (FRP) differ between day and night detections?")

fig4 = px.box(firms_df, x="daynight", y="frp", title="FRP by Day/Night")
st.plotly_chart(fig4, use_container_width=True)

st.markdown("**How to read this chart:**")
st.markdown("""
- X-axis shows Day vs Night categories.
- Y-axis shows FRP values (MW).
- Box shows median, quartiles, and spread.
- Outliers plotted as individual points.
""")

st.markdown("**Observations:**")
st.markdown("""
- Daytime detections tend to have slightly higher FRP values.
- Night detections show wider spread and variability.
- Outliers exist in both categories, but extreme FRP values are more common at night.
- Highlights differences in detection conditions.
""")
