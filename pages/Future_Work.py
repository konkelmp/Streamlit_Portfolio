import streamlit as st

st.set_page_config(page_title="Future Work", page_icon="🔮", layout="centered")

st.title("🔮 Future Work")

# --- Next Steps ---
st.subheader("Next Steps")
st.write("Here are the directions I plan to take this project:")

st.markdown("""
- ⛅ Add Air Quality data and make relations to fires and air quality.
- 📈 Add forecasting models to predict fire activity trends.
- ⚙️ Optimize performance for faster map rendering and smoother interactivity.
""")

# --- Reflection ---
st.subheader("Reflection")
st.write("Key changes and improvements made since the initial paper prototype:")

st.markdown("""
- Delved deeper into the fire information
- Refined layout for clarity and user experience compared to the original prototype.
""")
