import streamlit as st

st.set_page_config(
    page_title="Aviation Management Dashboard",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ Aviation Management & Airport Operations Dashboard")

st.subheader("Welcome to the Dashboard")

st.write(
    "This project analyzes aviation operations data to understand "
    "flight activity, delays, airport performance, routes, and "
    "operational efficiency."
)

st.info("🚧 Dashboard under development")

st.divider()

st.write("### Project Goals")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Flight Operations", "Coming Soon")

with col2:
    st.metric("Delay Analysis", "Coming Soon")

with col3:
    st.metric("Airport Performance", "Coming Soon")
