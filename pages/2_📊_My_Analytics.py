import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import (
    get_users,
    get_all_user_records,
    get_daily_completion_data
)

# -----------------------------------
# Login Protection
# -----------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.warning("Please login first.")
    st.stop()

# -----------------------------------
# Current Logged-in User
# -----------------------------------

user_name = st.session_state.username

# -----------------------------------
# Admin Restriction
# -----------------------------------

if st.session_state.role == "admin":

    st.warning(
        "Admins cannot log prayers."
    )

    st.stop()

# -----------------------------------
# Page Setup
# -----------------------------------

st.set_page_config(
    page_title="My Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 My Salah Analytics")



# -----------------------------------
# Load Records
# -----------------------------------

records = get_all_user_records(user_name)

# -----------------------------------
# Total Prayers
# -----------------------------------

total_possible = len(records) * 5

total_completed = 0

for row in records:

    total_completed += sum([
        row[1],
        row[2],
        row[3],
        row[4],
        row[5]
    ])

# -----------------------------------
# Completion Percentage
# -----------------------------------

completion_percentage = 0

if total_possible > 0:

    completion_percentage = round(
        (total_completed / total_possible) * 100,
        2
    )

# -----------------------------------
# Metrics Row
# -----------------------------------

col1, col2 = st.columns(2)

col1.metric(
    "Total Salah Completed",
    total_completed
)

col2.metric(
    "Completion Percentage",
    f"{completion_percentage}%"
)

st.divider()

# -----------------------------------
# Daily Completion Chart
# -----------------------------------

st.subheader("📈 Daily Completion Trend")

daily_data = get_daily_completion_data(user_name)

if daily_data:

    df = pd.DataFrame(
        daily_data,
        columns=[
            "Date",
            "Completed"
        ]
    )

    df["Date"] = pd.to_datetime(
        df["Date"]
    ).dt.strftime("%d-%b")

    fig = px.line(
        df,
        x="Date",
        y="Completed",
        markers=True
    )

    fig.update_layout(
        yaxis=dict(range=[0, 5])
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No analytics data available.")