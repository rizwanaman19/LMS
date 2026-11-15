
import streamlit as st

# --------------------------------
# IMPORT LOGIN PAGE
# --------------------------------

from views.login import show_login

# --------------------------------
# IMPORT ROLE DASHBOARDS
# --------------------------------

from views.student import show_dashboard as student_dashboard
from views.teacher import show_dashboard as teacher_dashboard
from views.administrator import show_dashboard as admin_dashboard
from views.examination import show_dashboard as examination_dashboard
from views.accountant import show_dashboard as accountant_dashboard
from views.librarian import show_dashboard as librarian_dashboard
from data.session_data import initialize_session_data

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="GPGC, Nowshera LMS",
    page_icon="🎓",
    layout="wide"
)
# --------------------------------
# SESSION INITIALIZATION
# --------------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "user" not in st.session_state:
    st.session_state["user"] = None

# --------------------------------
# ROLE DASHBOARD ROUTING
# --------------------------------
ROLE_DASHBOARDS = {

    "Student": student_dashboard,

    "Teacher": teacher_dashboard,

    "Administrator": admin_dashboard,

    "Examination Officer": examination_dashboard,

    "Accountant": accountant_dashboard,

    "Librarian": librarian_dashboard
}
# --------------------------------
# MAIN APPLICATION
# --------------------------------

if not st.session_state["logged_in"]:

    show_login()

else:

    user = st.session_state["user"]

    role = user["role"]

    dashboard = ROLE_DASHBOARDS.get(role)

    if dashboard:

        dashboard(user)

    else:

        st.error("Invalid user role.")

        st.session_state["logged_in"] = False
        st.session_state["user"] = None

        st.rerun()
