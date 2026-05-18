import streamlit as st

from database.db import (
    authenticate_user,
    create_table,
    seed_users
)

# -----------------------------------
# Initial Setup
# -----------------------------------

create_table()
seed_users()

st.set_page_config(
    page_title="Login",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 Login")

# -----------------------------------
# Session Defaults
# -----------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

if "username" not in st.session_state:

    st.session_state.username = None

if "role" not in st.session_state:

    st.session_state.role = None

# -----------------------------------
# Login Form
# -----------------------------------

username = st.text_input("Username")

password = st.text_input(
    "Password",
    type="password"
)

if st.button("Login"):

    user = authenticate_user(
        username,
        password
    )

    if user:

        st.session_state.logged_in = True
        st.session_state.username = user[0]
        st.session_state.role = user[1]

        st.success("Login successful.")

        st.rerun()

    else:

        st.error("Invalid credentials.")

# -----------------------------------
# Logged In Message
# -----------------------------------

if st.session_state.logged_in:

    st.success(
        f"Logged in as "
        f"{st.session_state.username}"
    )

    if st.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.role = None

        st.rerun()