import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Salah Tracker",
    page_icon="🕌",
    layout="centered"
)

st.title("🕌 Daily Salah Tracker")

today = date.today()

st.subheader(f"Date: {today}")

fajr = st.checkbox("Fajr")
zuhr = st.checkbox("Zuhr")
asr = st.checkbox("Asr")
maghrib = st.checkbox("Maghrib")
isha = st.checkbox("Isha")

completed = sum([
    fajr,
    zuhr,
    asr,
    maghrib,
    isha
])

st.metric("Today's Completion", f"{completed}/5")

if st.button("Save Salah"):

    data = {
        "Date": [today],
        "Fajr": [fajr],
        "Zuhr": [zuhr],
        "Asr": [asr],
        "Maghrib": [maghrib],
        "Isha": [isha]
    }

    df = pd.DataFrame(data)

    try:
        old_df = pd.read_csv("prayers.csv")
        df = pd.concat([old_df, df], ignore_index=True)
    except:
        pass

    df.to_csv("prayers.csv", index=False)

    st.success("Salah saved successfully!")

st.divider()

st.subheader("Prayer History")

try:
    history = pd.read_csv("prayers.csv")
    st.dataframe(history, use_container_width=True)
except:
    st.info("No prayer history available.")