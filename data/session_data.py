
import streamlit as st
from copy import deepcopy

from data.sample_data import (
    INITIAL_ENROLLED_COURSES,
    FEE_STRUCTURE,
    INITIAL_FEE_ACCOUNTS,
    INITIAL_BOOKS
)


def initialize_session_data():
    """
    Initialize shared application data.

    Existing session data is preserved.
    New data is created only when a key does not exist.
    """

    # -----------------------------------
    # STUDENT DATA
    # -----------------------------------

    if "enrolled_courses" not in st.session_state:
        st.session_state.enrolled_courses = deepcopy(
            INITIAL_ENROLLED_COURSES
        )

    # -----------------------------------
    # TEACHER DATA
    # -----------------------------------

    if "teacher_attendance" not in st.session_state:
        st.session_state.teacher_attendance = []

    if "teacher_marks" not in st.session_state:
        st.session_state.teacher_marks = []

    # -----------------------------------
    # EXAMINATION DATA
    # -----------------------------------

    if "examinations" not in st.session_state:
        st.session_state.examinations = []

    if "exam_schedules" not in st.session_state:
        st.session_state.exam_schedules = []

    if "exam_marks" not in st.session_state:
        st.session_state.exam_marks = []

    if "published_results" not in st.session_state:
        st.session_state.published_results = []

    # -----------------------------------
    # ACCOUNTANT DATA
    # -----------------------------------

    if "fee_structure" not in st.session_state:
        st.session_state.fee_structure = deepcopy(
            FEE_STRUCTURE
        )

    if "fee_accounts" not in st.session_state:
        st.session_state.fee_accounts = deepcopy(
            INITIAL_FEE_ACCOUNTS
        )

    if "fee_payments" not in st.session_state:
        st.session_state.fee_payments = []

    # -----------------------------------
    # LIBRARY DATA
    # -----------------------------------

    if "library_books" not in st.session_state:
        st.session_state.library_books = deepcopy(
            INITIAL_BOOKS
        )

    if "library_issues" not in st.session_state:
        st.session_state.library_issues = []

    if "library_returns" not in st.session_state:
        st.session_state.library_returns = []
