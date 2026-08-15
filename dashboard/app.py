import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Aviation Management Dashboard",
    page_icon="✈️",
    layout="wide"
)

# Load aviation data
df = pd.read_csv("T_ONTIME_MARKETING.csv")

st.title("✈️ Aviation Management & Airport Operations Dashboard")

st.markdown(
    "### Flight Operations Performance — January 2026"
)

# Clean data
df["DEP_DELAY"] = pd.to_numeric(df["DEP_DELAY"], errors="coerce")
df["CANCELLED"] = pd.to_numeric(df["CANCELLED"], errors="coerce")
df["DIVERTED"] = pd.to_numeric(df["DIVERTED"], errors="coerce")

# Key performance indicators
total_flights = len(df)
cancelled = int(df["CANCELLED"].sum())
diverted = int(df["DIVERTED"].sum())

operated_flights = df[df["CANCELLED"] == 0]
delayed_flights = operated_flights[operated_flights["DEP_DELAY"] >= 15]

delay_rate = (
    len(delayed_flights) / len(operated_flights) * 100
    if len(operated_flights) > 0 else 0
)

avg_delay = operated_flights["DEP_DELAY"].mean()

# Dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Flights", f"{total_flights:,}")

with col2:
    st.metric("Delay Rate", f"{delay_rate:.1f}%")

with col3:
    st.metric("Average Departure Delay", f"{avg_delay:.1f} min")

with col4:
    st.metric("Cancelled Flights", f"{cancelled:,}")

st.divider()

st.subheader("📊 Flight Operations Overview")

col1, col2 = st.columns(2)

with col1:
    airline_counts = df["MKT_UNIQUE_CARRIER"].value_counts()
    st.bar_chart(airline_counts)

with col2:
    delay_by_airline = (
        operated_flights
        .groupby("MKT_UNIQUE_CARRIER")["DEP_DELAY"]
        .mean()
        .sort_values(ascending=False)
    )

    st.bar_chart(delay_by_airline)

st.subheader("🛫 Top Departure Airports")

airport_counts = df["ORIGIN_AIRPORT_ID"].value_counts().head(10)
st.bar_chart(airport_counts)

st.subheader("📈 Management Summary")

st.write(
    f"""
    The dataset contains **{total_flights:,} flights**.
    Of the operated flights, **{delay_rate:.1f}%** experienced
    a departure delay of 15 minutes or more.

    The average departure delay was **{avg_delay:.1f} minutes**.
    There were **{cancelled:,} cancellations** and
    **{diverted:,} diversions**.
    """
)
