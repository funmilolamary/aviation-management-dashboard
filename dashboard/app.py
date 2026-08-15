    
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
# ROUTE ANALYSIS
# -----------------------------

st.subheader("🗺️ Busiest Flight Routes")

route_summary = (
    filtered_df
    .groupby(["ORIGIN_AIRPORT_ID", "DEST"])
    .size()
    .reset_index(name="Flights")
    .sort_values("Flights", ascending=False)
    .head(10)
)

route_summary["Route"] = (
    route_summary["ORIGIN_AIRPORT_ID"].astype(str)
    + " → "
    + route_summary["DEST"]
)

fig_routes = px.bar(
    route_summary,
    x="Flights",
    y="Route",
    orientation="h",
    title="Top 10 Flight Routes by Number of Operations",
    labels={"Flights": "Number of Flights"}
)

st.plotly_chart(fig_routes, use_container_width=True)
# -----------------------------
# OPERATIONAL RISK
# -----------------------------

st.subheader("🚨 Operational Risk Indicators")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    st.metric(
        "Flights Delayed 15+ Minutes",
        f"{len(delayed):,}"
    )

with risk_col2:
    st.metric(
        "Operational Disruptions",
        f"{cancelled + diverted:,}"
    )

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
# -----------------------------
# AVIATION MANAGER'S DECISION CENTER
# -----------------------------

st.subheader("🎯 Aviation Manager's Decision Center")

st.markdown(
    "Automated operational assessment based on the selected flight data."
)

# Overall operational status
if delay_rate >= 30:
    status = "🔴 HIGH OPERATIONAL RISK"
    message = (
        f"The delay rate is {delay_rate:.1f}%, indicating that "
        "departure performance requires management attention."
    )
elif delay_rate >= 15:
    status = "🟡 MODERATE OPERATIONAL RISK"
    message = (
        f"The delay rate is {delay_rate:.1f}%. "
        "Operations should be monitored for recurring disruption."
    )
else:
    status = "🟢 LOW OPERATIONAL RISK"
    message = (
        f"The delay rate is {delay_rate:.1f}%, "
        "indicating relatively strong departure performance."
    )

st.markdown(f"### {status}")
st.write(message)

# Identify the main delay cause
delay_causes = {
    "Carrier": filtered_df["CARRIER_DELAY"].sum(),
    "Air Traffic / NAS": filtered_df["NAS_DELAY"].sum(),
    "Security": filtered_df["SECURITY_DELAY"].sum(),
    "Late Aircraft": filtered_df["LATE_AIRCRAFT_DELAY"].sum(),
}

main_cause = max(delay_causes, key=delay_causes.get)

st.warning(
    f"⚠️ **Primary delay contributor:** {main_cause}. "
    "Management should investigate recurring patterns in this category."
)

# Management recommendations
st.markdown("### 💡 Recommended Management Actions")

recommendations = [
    "Monitor airlines and airports with consistently high delay rates.",
    "Investigate the primary source of operational delays.",
    "Review recurring high-volume routes for disruption patterns.",
    "Track cancellations and diversions as indicators of operational instability.",
]

for recommendation in recommendations:
    st.write(f"• {recommendation}")
