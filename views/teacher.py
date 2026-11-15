import streamlit as st
import pandas as pd

from datetime import date

from data.sample_data import (
    TEACHER_PROFILE,
    TEACHER_COURSES,
    TEACHER_TIMETABLE,
    STUDENTS
)


# -----------------------------------
# INITIALIZE TEACHER DATA
# -----------------------------------

def initialize_teacher_data():

    if "teacher_attendance" not in st.session_state:
        st.session_state.teacher_attendance = []

    if "teacher_marks" not in st.session_state:
        st.session_state.teacher_marks = []


# -----------------------------------
# VIEW ASSIGNED COURSES
# -----------------------------------

def show_assigned_courses():

    st.subheader("My Assigned Courses")

    courses_df = pd.DataFrame(TEACHER_COURSES)

    st.dataframe(
        courses_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# VIEW TIMETABLE
# -----------------------------------

def show_timetable():

    st.subheader("My Teaching Timetable")

    timetable_df = pd.DataFrame(TEACHER_TIMETABLE)

    st.dataframe(
        timetable_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# VIEW STUDENT LIST
# -----------------------------------

def show_student_list():

    st.subheader("Student List")

    st.write("Students enrolled in your assigned courses.")

    students_df = pd.DataFrame(STUDENTS)

    st.dataframe(
        students_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(f"Total Students: {len(STUDENTS)}")


# -----------------------------------
# MARK ATTENDANCE
# -----------------------------------

def mark_attendance():

    st.subheader("Mark Student Attendance")

    course_names = [
        course["course_name"]
        for course in TEACHER_COURSES
    ]

    with st.form("attendance_form"):

        selected_course = st.selectbox(
            "Select Course",
            course_names
        )

        attendance_date = st.date_input(
            "Attendance Date",
            value=date.today()
        )

        st.write("### Select Student Attendance")

        attendance_records = []

        for student in STUDENTS:

            status = st.selectbox(
                student["name"],
                ["Present", "Absent"],
                key=f"attendance_{student['student_id']}"
            )

            attendance_records.append({
                "student_id": student["student_id"],
                "student_name": student["name"],
                "course": selected_course,
                "date": str(attendance_date),
                "status": status
            })

        submitted = st.form_submit_button(
            "Save Attendance",
            use_container_width=True
        )

        if submitted:

            # Remove previously saved records for this
            # course, date, and student combination.
            existing_records = [
                record
                for record in st.session_state.teacher_attendance
                if not (
                    record["course"] == selected_course
                    and record["date"] == str(attendance_date)
                )
            ]

            existing_records.extend(attendance_records)

            st.session_state.teacher_attendance = existing_records

            st.success("Attendance saved successfully!")


    # Display saved attendance

    st.divider()
    st.write("### Saved Attendance")

    if st.session_state.teacher_attendance:

        attendance_df = pd.DataFrame(
            st.session_state.teacher_attendance
        )

        st.dataframe(
            attendance_df,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No attendance records have been saved yet.")


# -----------------------------------
# SUBMIT MARKS
# -----------------------------------

def submit_marks():

    st.subheader("Submit Student Marks")

    course_names = [
        course["course_name"]
        for course in TEACHER_COURSES
    ]

    student_names = [
        student["name"]
        for student in STUDENTS
    ]

    with st.form("marks_form"):

        selected_course = st.selectbox(
            "Select Course",
            course_names
        )

        selected_student = st.selectbox(
            "Select Student",
            student_names
        )

        assessment = st.selectbox(
            "Assessment Type",
            [
                "Quiz",
                "Assignment",
                "Midterm Exam",
                "Final Exam"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:
            obtained_marks = st.number_input(
                "Obtained Marks",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        with col2:
            total_marks = st.number_input(
                "Total Marks",
                min_value=1.0,
                value=100.0,
                step=1.0
            )

        submitted = st.form_submit_button(
            "Submit Marks",
            use_container_width=True
        )

        if submitted:

            if obtained_marks > total_marks:

                st.error(
                    "Obtained marks cannot exceed total marks."
                )

            else:

                student = next(
                    student
                    for student in STUDENTS
                    if student["name"] == selected_student
                )

                new_record = {
                    "student_id": student["student_id"],
                    "student_name": selected_student,
                    "course": selected_course,
                    "assessment": assessment,
                    "obtained_marks": obtained_marks,
                    "total_marks": total_marks
                }

                st.session_state.teacher_marks.append(
                    new_record
                )

                st.success("Marks submitted successfully!")


# -----------------------------------
# VIEW MARKS
# -----------------------------------

def view_marks():

    st.subheader("Student Marks")

    if st.session_state.teacher_marks:

        marks_df = pd.DataFrame(
            st.session_state.teacher_marks
        )

        marks_df["percentage"] = (
            marks_df["obtained_marks"]
            / marks_df["total_marks"]
            * 100
        ).round(2)

        st.dataframe(
            marks_df,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Total Mark Records",
            len(marks_df)
        )

    else:

        st.info(
            "No marks have been submitted yet. "
            "Use the Submit Marks section to add records."
        )


# -----------------------------------
# TEACHER DASHBOARD
# -----------------------------------

def show_dashboard(user):

    initialize_teacher_data()

    # Sidebar navigation

    st.sidebar.title("Teacher Panel")

    st.sidebar.write(
        f"Welcome, {user['name']}"
    )

    menu_items = [
        "Dashboard",
        "Assigned Courses",
        "My Timetable",
        "Student List",
        "Mark Attendance",
        "Submit Marks",
        "View Marks"
    ]

    selected_page = st.sidebar.radio(
        "Navigation",
        menu_items
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None

        st.rerun()


    # Main content

    st.title("Teacher Dashboard")

    st.write(
        f"Welcome back, {user['name']}!"
    )

    if selected_page == "Dashboard":

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Assigned Courses",
                len(TEACHER_COURSES)
            )

        with col2:
            st.metric(
                "Total Students",
                len(STUDENTS)
            )

        with col3:
            st.metric(
                "Attendance Records",
                len(st.session_state.teacher_attendance)
            )

        st.divider()

        st.subheader("Teacher Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Teacher ID:**", TEACHER_PROFILE["teacher_id"])
            st.write("**Name:**", TEACHER_PROFILE["name"])
            st.write("**Email:**", TEACHER_PROFILE["email"])

        with col2:
            st.write("**Department:**", TEACHER_PROFILE["department"])
            st.write("**Designation:**", TEACHER_PROFILE["designation"])

        st.divider()

        st.subheader("Assigned Courses")

        for course in TEACHER_COURSES:

            st.write(
                f"**{course['course_id']}** - "
                f"{course['course_name']} "
                f"({course['credit_hours']} Credit Hours)"
            )

    elif selected_page == "Assigned Courses":

        show_assigned_courses()

    elif selected_page == "My Timetable":

        show_timetable()

    elif selected_page == "Student List":

        show_student_list()

    elif selected_page == "Mark Attendance":

        mark_attendance()

    elif selected_page == "Submit Marks":

        submit_marks()

    elif selected_page == "View Marks":

        view_marks()