
import streamlit as st


def render_role_dashboard(role, user, menu_items):

    # Sidebar header
    st.sidebar.title("🎓 University LMS")

    st.sidebar.write(f"Welcome, {user['name']}")

    st.sidebar.caption(f"Role: {role}")

    st.sidebar.divider()

    # Role-based navigation
    selected_page = st.sidebar.selectbox(
        "Navigation",
        menu_items
    )

    st.sidebar.divider()

    # Logout
    if st.sidebar.button("Logout", use_container_width=True):

        st.session_state["logged_in"] = False
        st.session_state["user"] = None

        st.rerun()

    # Main dashboard
    st.title(f"{role} Dashboard")

    st.write(f"Welcome, {user['name']}!")

    st.divider()

    st.subheader(selected_page)

    if selected_page == "Dashboard":

        st.success(f"You are logged in as {role}.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Academic Year", "2026-27")

        with col2:
            st.metric("Semester", "Fall")

        with col3:
            st.metric("System Status", "Active")

    else:

        st.info(
            f"{selected_page} module will be implemented "
            "in the upcoming development phase."
        )
