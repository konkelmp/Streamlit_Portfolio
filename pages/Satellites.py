def satellite_page(df):
    st.title("Satellite Reporting Frequency")

    st.write("This visualization shows which satellites reported the most fire detections.")

    satellite_counts = df['satellite'].value_counts().reset_index()
    satellite_counts.columns = ['Satellite', 'Detections']

    fig = px.bar(satellite_counts, x="Satellite", y="Detections",
                 title="Detections by Satellite",
                 labels={"Detections":"Number of Detections"},
                 color="Detections")

    st.plotly_chart(fig, use_container_width=True)
