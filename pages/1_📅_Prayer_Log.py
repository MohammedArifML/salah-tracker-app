import streamlit as st
from datetime import date

from database.db import (
    create_table,
    insert_prayer,
    update_prayer,
    get_prayer_record,
    get_user_history,
    add_user,
    get_users,
    seed_users
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

if st.session_state.role == "admin":

    st.warning(
        "Admins cannot log prayers."
    )

    st.stop()

# -----------------------------------
# Page Setup
# -----------------------------------

st.set_page_config(
    page_title="Salah Tracker",
    page_icon="🕌",
    layout="centered"
)

create_table()
seed_users()

# -----------------------------------
# Title
# -----------------------------------

st.title("🕌 Daily Salah Tracker")


# -----------------------------------
# Date Input
# -----------------------------------

selected_date = st.date_input(
    "Select Date",
    value=date.today(),
    max_value=date.today()
)

selected_date_str = str(selected_date)

# -----------------------------------
# Existing Record Check
# -----------------------------------

existing_record = None

if user_name.strip():

    existing_record = get_prayer_record(
        user_name=user_name,
        prayer_date=selected_date_str
    )

# -----------------------------------
# Existing Record Message
# -----------------------------------

if existing_record:

    st.info(
        "You already logged salah for this date. "
        "You may edit and update it."
    )

# -----------------------------------
# Default Checkbox Values
# -----------------------------------

default_fajr = False
default_zuhr = False
default_asr = False
default_maghrib = False
default_isha = False

# -----------------------------------
# Load Existing Values
# -----------------------------------

if existing_record:

    default_fajr = bool(existing_record[3])
    default_zuhr = bool(existing_record[4])
    default_asr = bool(existing_record[5])
    default_maghrib = bool(existing_record[6])
    default_isha = bool(existing_record[7])

# -----------------------------------
# Salah Checkboxes
# -----------------------------------

# -----------------------------------
# Default Values
# -----------------------------------

default_fajr = False
default_zuhr = False
default_asr = False
default_maghrib = False
default_isha = False

if existing_record:

    default_fajr = bool(existing_record[3])
    default_zuhr = bool(existing_record[4])
    default_asr = bool(existing_record[5])
    default_maghrib = bool(existing_record[6])
    default_isha = bool(existing_record[7])

# -----------------------------------
# Dynamic Widget Key
# -----------------------------------

widget_suffix = f"{user_name}_{selected_date_str}"

# -----------------------------------
# Salah Checkboxes
# -----------------------------------

st.subheader("Salah Tracking")

fajr = st.checkbox(
    "Fajr",
    value=default_fajr,
    key=f"fajr_{widget_suffix}"
)

zuhr = st.checkbox(
    "Zuhr",
    value=default_zuhr,
    key=f"zuhr_{widget_suffix}"
)

asr = st.checkbox(
    "Asr",
    value=default_asr,
    key=f"asr_{widget_suffix}"
)

maghrib = st.checkbox(
    "Maghrib",
    value=default_maghrib,
    key=f"maghrib_{widget_suffix}"
)

isha = st.checkbox(
    "Isha",
    value=default_isha,
    key=f"isha_{widget_suffix}"
)

# -----------------------------------
# Completion Metric
# -----------------------------------

completed = sum([
    fajr,
    zuhr,
    asr,
    maghrib,
    isha
])

st.metric(
    "Today's Completion",
    f"{completed}/5"
)

# -----------------------------------
# Save / Update
# -----------------------------------

button_text = (
    "Update Salah"
    if existing_record
    else "Save Salah"
)

if st.button(button_text):

    if not user_name.strip():

        st.error("Name is required.")

    else:

        if existing_record:

            update_prayer(
                user_name=user_name,
                prayer_date=selected_date_str,
                fajr=int(fajr),
                zuhr=int(zuhr),
                asr=int(asr),
                maghrib=int(maghrib),
                isha=int(isha)
            )

            st.success(
                "Salah updated successfully."
            )

        else:

            insert_prayer(
                user_name=user_name,
                prayer_date=selected_date_str,
                fajr=int(fajr),
                zuhr=int(zuhr),
                asr=int(asr),
                maghrib=int(maghrib),
                isha=int(isha)
            )

            st.success(
                "Salah saved successfully."
            )

# -----------------------------------
# User History Dashboard
# -----------------------------------

if user_name.strip():

    st.divider()

    st.subheader("📅 Last 7 Days History")

    history = get_user_history(user_name)

    if history:

        # Header Row
        header_cols = st.columns(
            [1.2, 1.5, 1, 1, 1, 1, 1, 1]
        )

        headers = [
            "Day",
            "Date",
            "Fajr",
            "Zuhr",
            "Asr",
            "Maghrib",
            "Isha",
            "Total"
        ]

        for col, header in zip(header_cols, headers):
            col.markdown(f"**{header}**")

        st.markdown("---")

        # Data Rows
        for row in history:

            prayer_date = row[0]

            fajr_val = row[1]
            zuhr_val = row[2]
            asr_val = row[3]
            maghrib_val = row[4]
            isha_val = row[5]

            completed = sum([
                fajr_val,
                zuhr_val,
                asr_val,
                maghrib_val,
                isha_val
            ])

            from datetime import datetime

            day_name = datetime.strptime(
                prayer_date,
                "%Y-%m-%d"
            ).strftime("%a")

            cols = st.columns(
                [1.2, 1.5, 1, 1, 1, 1, 1, 1]
            )

            cols[0].write(day_name)
            cols[1].write(prayer_date)

            cols[2].write("✅" if fajr_val else "❌")
            cols[3].write("✅" if zuhr_val else "❌")
            cols[4].write("✅" if asr_val else "❌")
            cols[5].write("✅" if maghrib_val else "❌")
            cols[6].write("✅" if isha_val else "❌")

            cols[7].write(f"{completed}/5")

    else:

        st.info("No history available yet.")            