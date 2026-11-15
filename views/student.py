
import streamlit as st

from data.sample_data import (
    STUDENT_PROFILE,
    COURSES,
    INITIAL_ENROLLED_COURSES,
    ATTENDANCE,
    TIMETABLE
)
# ========================================
# STUDENT SESSION DATA
# ========================================

def initialize_student_data():

    if "enrolled_courses" not in st.session_state:

        st.session_state.enrolled_courses = (
            INITIAL_ENROLLED_COURSES.copy()
        )


# ========================================
# STUDENT PROFILE
# ========================================

def show_profile():

    st.subheader("👤 Student Profile")

    profile = STUDENT_PROFILE

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Student ID",
            value=profile["student_id"],
            disabled=True
        )

        st.text_input(
            "Full Name",
            value=profile["name"],
            disabled=True
        )

        st.text_input(
            "Email",
            value=profile["email"],
            disabled=True
        )

        st.text_input(
            "Program",
            value=profile["program"],
            disabled=True
        )

    with col2:

        st.text_input(
            "Department",
            value=profile["department"],
            disabled=True
        )

        st.text_input(
            "Semester",
            value=profile["semester"],
            disabled=True
        )

        st.text_input(
            "Academic Session",
            value=profile["session"],
            disabled=True
        )

        st.text_input(
            "CGPA",
            value=str(profile["cgpa"]),
            disabled=True
        )


# ========================================
# REGISTER COURSE
# ========================================

def register_course():

    st.subheader("📚 Course Registration")

    enrolled = st.session_state.enrolled_courses

    available_courses = [
        course for course in COURSES
        if course["course_id"] not in enrolled
    ]

    if not available_courses:

        st.info("No additional courses available.")

        return

    st.write("Select a course to register.")

    with st.form("register_course_form"):

        selected_course = st.selectbox(
            "Available Courses",
            available_courses,
            format_func=lambda course: (
                f"{course['course_id']} - "
                f"{course['course_name']} "
                f"({course['credit_hours']} CH)"
            )
        )

        submit = st.form_submit_button(
            "Register Course",
            use_container_width=True
        )

    if submit:

        course_id = selected_course["course_id"]

        if course_id not in st.session_state.enrolled_courses:

            st.session_state.enrolled_courses.append(course_id)

            st.success(
                f"Successfully registered "
                f"for {selected_course['course_name']}!"
            )

            st.rerun()


# ========================================
# DROP COURSE
# ========================================

def drop_course():

    st.subheader("❌ Drop Course")

    enrolled = st.session_state.enrolled_courses

    enrolled_details = [
        course for course in COURSES
        if course["course_id"] in enrolled
    ]

    if not enrolled_details:

        st.info("You have no registered courses.")

        return

    with st.form("drop_course_form"):

        selected_course = st.selectbox(
            "Select Course to Drop",
            enrolled_details,
            format_func=lambda course: (
                f"{course['course_id']} - "
                f"{course['course_name']}"
            )
        )

        submit = st.form_submit_button(
            "Drop Course",
            use_container_width=True
        )

    if submit:

        course_id = selected_course["course_id"]

        st.session_state.enrolled_courses.remove(course_id)

        st.success(
            f"{selected_course['course_name']} "
            "has been dropped successfully."
        )

        st.rerun()


# ========================================
# VIEW TIMETABLE
# ========================================

def show_timetable():

    st.subheader("📅 Class Timetable")

    timetable = [
        item for item in TIMETABLE
        if any(
            course["course_name"] == item["course"]
            and course["course_id"] in st.session_state.enrolled_courses
            for course in COURSES
        )
    ]

    if timetable:

        st.dataframe(
            timetable,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No timetable available for your courses.")


# ========================================
# VIEW ATTENDANCE
# ========================================

def show_attendance():

    st.subheader("📊 Attendance Records")

    enrolled_names = [
        course["course_name"]
        for course in COURSES
        if course["course_id"] in st.session_state.enrolled_courses
    ]

    records = [
        record for record in ATTENDANCE
        if record["course"] in enrolled_names
    ]

    if not records:

        st.info("No attendance records available.")

        return

    total_classes = sum(
        record["total_classes"] for record in records
    )

    total_present = sum(
        record["present"] for record in records
    )

    total_absent = sum(
        record["absent"] for record in records
    )

    percentage = (
        total_present / total_classes * 100
        if total_classes else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Classes", total_classes)

    col2.metric("Present", total_present)

    col3.metric("Absent", total_absent)

    st.metric("Overall Attendance", f"{percentage:.2f}%")

    st.progress(int(percentage))

    attendance_table = []

    for record in records:

        attendance_percentage = (
            record["present"] /
            record["total_classes"] * 100
            if record["total_classes"] else 0
        )

        attendance_table.append({
            "Course": record["course"],
            "Total Classes": record["total_classes"],
            "Present": record["present"],
            "Absent": record["absent"],
            "Attendance": f"{attendance_percentage:.2f}%"
        })

    st.dataframe(
        attendance_table,
        use_container_width=True,
        hide_index=True
    )


# ========================================
# STUDENT DASHBOARD
# ========================================

def show_dashboard(user):

    initialize_student_data()

    st.sidebar.title("🎓 University LMS")

    st.sidebar.write(f"Welcome, {user['name']}")

    st.sidebar.caption("Student Panel")

    st.sidebar.divider()

    menu_items = [
        "Dashboard",
        "View Profile",
        "Register Course",
        "Drop Course",
        "View Timetable",
        "View Attendance"
    ]

    selected_page = st.sidebar.selectbox(
        "Navigation",
        menu_items
    )

    st.sidebar.divider()

    if st.sidebar.button("Logout", use_container_width=True):

        st.session_state["logged_in"] = False

        st.session_state["user"] = None

        st.rerun()

    # Main page routing

    if selected_page == "Dashboard":

        st.title("🎓 Student Dashboard")

        st.write(f"Welcome back, {user['name']}!")

        st.divider()

        enrolled_count = len(
            st.session_state.enrolled_courses
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Enrolled Courses", enrolled_count)

        col2.metric("Current CGPA", STUDENT_PROFILE["cgpa"])

        col3.metric("Semester", "6th")

        st.divider()

        st.subheader("Academic Information")

        st.write(f"**Student ID:** {STUDENT_PROFILE['student_id']}")

        st.write(f"**Department:** {STUDENT_PROFILE['department']}")

        st.write(f"**Program:** {STUDENT_PROFILE['program']}")

        st.info("Select a module from the sidebar to continue.")

    elif selected_page == "View Profile":

        show_profile()

    elif selected_page == "Register Course":

        register_course()

    elif selected_page == "Drop Course":

        drop_course()

    elif selected_page == "View Timetable":

        show_timetable()

    elif selected_page == "View Attendance":

        show_attendance()
