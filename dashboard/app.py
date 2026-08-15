    
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Aviation Management Dashboard",
    page_icon="✈️",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("T_ONTIME_MARKETING.csv")

# Convert numeric columns
numeric_columns = [
    "DEP_DELAY",
    "CANCELLED",
    "DIVERTED",
    "CARRIER_DELAY",
    "NAS_DELAY",
    "SECURITY_DELAY",
    "LATE_AIRCRAFT_DELAY"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce").fillna(0)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("✈️ Dashboard Controls")

airlines = ["All Airlines"] + sorted(
    df["MKT_UNIQUE_CARRIER"].dropna().unique().tolist()
)

selected_airline = st.sidebar.selectbox(
    "Select Airline",
    airlines
)

if selected_airline != "All Airlines":
    filtered_df = df[
        df["MKT_UNIQUE_CARRIER"] == selected_airline
    ]
else:
    filtered_df = df.copy()

# -----------------------------
# TITLE
# -----------------------------

st.title("✈️ Aviation Management & Airport Operations")

st.markdown(
    """
    **Operational Performance Dashboard**

    This dashboard analyzes flight operations, delays,
    cancellations, airline performance and airport activity
    to support data-driven aviation management decisions.
    """
)

st.divider()

# -----------------------------
# KPIs
# -----------------------------

total_flights = len(filtered_df)

operated = filtered_df[filtered_df["CANCELLED"] == 0]

delayed = operated[operated["DEP_DELAY"] >= 15]

delay_rate = (
    len(delayed) / len(operated) * 100
    if len(operated) > 0 else 0
)

average_delay = (
    operated["DEP_DELAY"].mean()
    if len(operated) > 0 else 0
)

cancelled = int(filtered_df["CANCELLED"].sum())

diverted = int(filtered_df["DIVERTED"].sum())

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("✈️ Flights", f"{total_flights:,}")
col2.metric("⏱️ Delay Rate", f"{delay_rate:.1f}%")
col3.metric("Average Delay", f"{average_delay:.1f} min")
col4.metric("🚫 Cancellations", f"{cancelled:,}")
col5.metric("↪️ Diversions", f"{diverted:,}")

st.divider()

# -----------------------------
# AIRLINE PERFORMANCE
# -----------------------------

st.subheader("📊 Airline Performance")

airline_summary = (
    filtered_df
    .groupby("MKT_UNIQUE_CARRIER")
    .agg(
        Flights=("MKT_CARRIER_FL_NUM", "count"),
        Average_Delay=("DEP_DELAY", "mean")
    )
    .reset_index()
)

fig_airline = px.bar(
    airline_summary,
    x="MKT_UNIQUE_CARRIER",
    y="Average_Delay",
    title="Average Departure Delay by Airline",
    labels={
        "MKT_UNIQUE_CARRIER": "Airline",
        "Average_Delay": "Average Delay (minutes)"
    }
)

st.plotly_chart(fig_airline, use_container_width=True)

# -----------------------------
# AIRPORT ACTIVITY
# -----------------------------

st.subheader("🛫 Airport Activity")

airport_summary = (
    filtered_df["ORIGIN_AIRPORT_ID"]
    .value_counts()
    .head(10)
    .reset_index()
)

airport_summary.columns = ["Airport", "Flights"]

fig_airport = px.bar(
    airport_summary,
    x="Airport",
    y="Flights",
    title="Top 10 Departure Airports"
)

st.plotly_chart(fig_airport, use_container_width=True)

# -----------------------------
# DELAY CAUSES
# -----------------------------

st.subheader("⏱️ Delay Cause Analysis")

delay_causes = {
    "Carrier": filtered_df["CARRIER_DELAY"].sum(),
    "Air Traffic / NAS": filtered_df["NAS_DELAY"].sum(),
    "Security": filtered_df["SECURITY_DELAY"].sum(),
    "Late Aircraft": filtered_df["LATE_AIRCRAFT_DELAY"].sum()
}

delay_df = pd.DataFrame(
    list(delay_causes.items()),
    columns=["Cause", "Minutes"]
)

fig_delay = px.pie(
    delay_df,
    names="Cause",
    values="Minutes",
    title="Distribution of Delay Causes"
)

st.plotly_chart(fig_delay, use_container_width=True)

# -----------------------------
# MANAGEMENT INSIGHTS
# -----------------------------

st.subheader("🎯 Management Insights")

if delay_rate >= 30:
    st.warning(
        f"⚠️ The current delay rate is {delay_rate:.1f}%. "
        "Operational teams should investigate the main sources "
        "of delay and prioritize corrective action."
    )
else:
    st.success(
        f"✅ The current delay rate is {delay_rate:.1f}%, "
        "indicating relatively strong departure performance."
    )

st.info(
    "Management recommendation: monitor recurring delay causes, "
    "identify high-performing and underperforming airlines, and "
    "prioritize airports or routes showing persistent operational disruption."
)

st.caption(
    "Data source: U.S. Bureau of Transportation Statistics (BTS) "
    "On-Time Performance data."
)
