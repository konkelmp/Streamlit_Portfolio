import streamlit as st

st.set_page_config(page_title="Professional Bio", page_icon="👤", layout="centered")

st.title("👤 Professional Bio")

# --- Short Professional Summary ---
st.subheader("Summary")
st.write(
  """
  I am a part‑time software support specialist and student with hands‑on experience in scripting, troubleshooting, and data visualization. 
  My background includes Computer Science schooling and three years in IT support, where I honed skills in automation systems and workflow optimization. 
  I specialize in building and supporting interactive dashboards and exploratory data analysis tools using Python libraries, Streamlit, and Tableau. 
  My interests span systems‑level programming, cryptographic solutions, geographic systems, and space and science exploration.
  """
)

# --- Profile Image (Optional) ---
st.subheader("Profile")
st.image("assests/hubble-captures-vivid-auroras-in-jupiters-atmosphere_28000029525_o~small.jpg", caption="Exploring clarity in code, data, and design.", width=200)
st.write("Alt-text: Photo of Jupiter")

# --- Highlights ---
st.subheader("Highlights")
st.markdown(
  """
  - 📊 Skilled in Python libraries: **Pandas, Seaborn, Matplotlib, Plotly, Streamlit**
  - ⚙️ User focused with making information easy to understand
  - 🔐 Experience with **cryptographic solutions**
  - 📈 Data storytelling with **Tableau**
  """
)

# --- Visualization Philosophy ---
st.subheader("Visualization Philosophy")
st.write(
  """
  I believe effective visualization should prioritize **clarity, accessibility, and ethical responsibility**:
  """
)
