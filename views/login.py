
import streamlit as st

from utils.authentication import authenticate_user


def show_login():

    st.title("GPGC Nowshera LMS")

    st.subheader("Login to your account")

    st.write(
        "Welcome! Please enter your credentials "
        "to access the Learning Management System."
    )

    st.divider()

    # Login form
    with st.form("login_form"):

        username = st.text_input(
            "Username",
            placeholder="Enter your username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        login_button = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login_button:

        user = authenticate_user(username, password)

        if user:

            st.session_state["logged_in"] = True

            st.session_state["user"] = user

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("Invalid username or password.")

    st.divider()

    st.caption("GPGC Nowshera Learning Management System")
