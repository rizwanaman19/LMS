import streamlit as st
import pandas as pd

from datetime import date, time

from data.sample_data import (
    EXAM_COURSES,
    EXAM_OFFICER_PROFILE,
    STUDENTS
)


# -----------------------------------
# INITIALIZE EXAMINATION DATA
# -----------------------------------

def initialize_exam_data():

    if "examinations" not in st.session_state:
        st.session_state.examinations = []

    if "exam_schedules" not in st.session_state:
        st.session_state.exam_schedules = []

    if "exam_marks" not in st.session_state:
        st.session_state.exam_marks = []

    if "published_results" not in st.session_state:
        st.session_state.published_results = []


# -----------------------------------
# CREATE EXAMINATION
# -----------------------------------

def create_examination():

    st.subheader("Create New Examination")

    course_options = {
        course["course_id"]: course["course_name"]
        for course in EXAM_COURSES
    }

    with st.form("create_exam_form"):

        exam_name = st.text_input(
            "Examination Name",
            placeholder="e.g. Fall 2026 Midterm"
        )

        exam_type = st.selectbox(
            "Examination Type",
            [
                "Midterm Exam",
                "Final Exam",
                "Quiz",
                "Practical Exam"
            ]
        )

        course_id = st.selectbox(
            "Select Course",
            list(course_options.keys()),
            format_func=lambda x: f"{x} - {course_options[x]}"
        )

        total_marks = st.number_input(
            "Total Marks",
            min_value=1,
            max_value=500,
            value=100
        )

        exam_date = st.date_input(
            "Examination Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Create Examination",
            use_container_width=True
        )

        if submitted:

            if not exam_name.strip():

                st.error("Please enter an examination name.")

            else:

                new_exam = {
                    "exam_id": f"EXM-{len(st.session_state.examinations) + 1:03d}",
                    "exam_name": exam_name.strip(),
                    "exam_type": exam_type,
                    "course_id": course_id,
                    "course_name": course_options[course_id],
                    "total_marks": total_marks,
                    "exam_date": str(exam_date)
                }

                st.session_state.examinations.append(new_exam)

                st.success("Examination created successfully!")


    st.divider()

    st.write("### Created Examinations")

    if st.session_state.examinations:

        exams_df = pd.DataFrame(
            st.session_state.examinations
        )

        st.dataframe(
            exams_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No examinations created yet.")


# -----------------------------------
# PREPARE EXAMINATION SCHEDULE
# -----------------------------------

def prepare_exam_schedule():

    st.subheader("Prepare Examination Schedule")

    if not st.session_state.examinations:

        st.warning(
            "Please create an examination before preparing its schedule."
        )
        return

    exam_options = {
        exam["exam_id"]: exam["exam_name"]
        for exam in st.session_state.examinations
    }

    with st.form("exam_schedule_form"):

        selected_exam = st.selectbox(
            "Select Examination",
            list(exam_options.keys()),
            format_func=lambda x: exam_options[x]
        )

        schedule_date = st.date_input(
            "Exam Date",
            value=date.today(),
            key="schedule_date"
        )

        exam_time = st.time_input(
            "Exam Time",
            value=time(9, 0)
        )

        room = st.text_input(
            "Examination Room",
            placeholder="e.g. Hall A"
        )

        submitted = st.form_submit_button(
            "Save Exam Schedule",
            use_container_width=True
        )

        if submitted:

            if not room.strip():

                st.error("Please enter an examination room.")

            else:

                new_schedule = {
                    "exam_id": selected_exam,
                    "exam_name": exam_options[selected_exam],
                    "date": str(schedule_date),
                    "time": str(exam_time),
                    "room": room.strip()
                }

                # Update an existing schedule for this exam
                existing_schedules = [
                    item
                    for item in st.session_state.exam_schedules
                    if item["exam_id"] != selected_exam
                ]

                existing_schedules.append(new_schedule)

                st.session_state.exam_schedules = existing_schedules

                st.success("Examination schedule saved successfully!")


    st.divider()

    st.write("### Examination Schedule")

    if st.session_state.exam_schedules:

        schedule_df = pd.DataFrame(
            st.session_state.exam_schedules
        )

        st.dataframe(
            schedule_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No examination schedules available.")


# -----------------------------------
# ENTER EXAMINATION MARKS
# -----------------------------------

def enter_exam_marks():

    st.subheader("Enter Examination Marks")

    if not st.session_state.examinations:

        st.warning("Create an examination first.")
        return

    exam_options = {
        exam["exam_id"]: exam
        for exam in st.session_state.examinations
    }

    with st.form("exam_marks_form"):

        selected_exam_id = st.selectbox(
            "Select Examination",
            list(exam_options.keys()),
            format_func=lambda x: exam_options[x]["exam_name"]
        )

        selected_student = st.selectbox(
            "Select Student",
            STUDENTS,
            format_func=lambda x: f"{x['student_id']} - {x['name']}"
        )

        exam = exam_options[selected_exam_id]

        obtained_marks = st.number_input(
            "Obtained Marks",
            min_value=0.0,
            max_value=float(exam["total_marks"]),
            value=0.0,
            step=1.0
        )

        submitted = st.form_submit_button(
            "Save Examination Marks",
            use_container_width=True
        )

        if submitted:

            new_record = {
                "exam_id": selected_exam_id,
                "exam_name": exam["exam_name"],
                "student_id": selected_student["student_id"],
                "student_name": selected_student["name"],
                "course_name": exam["course_name"],
                "obtained_marks": obtained_marks,
                "total_marks": exam["total_marks"]
            }

            # Update marks if the same student and exam
            # already have a record.
            existing_records = [
                record
                for record in st.session_state.exam_marks
                if not (
                    record["exam_id"] == selected_exam_id
                    and record["student_id"] == selected_student["student_id"]
                )
            ]

            existing_records.append(new_record)

            st.session_state.exam_marks = existing_records

            st.success("Examination marks saved successfully!")


    st.divider()

    st.write("### Examination Marks Records")

    if st.session_state.exam_marks:

        marks_df = pd.DataFrame(
            st.session_state.exam_marks
        )

        st.dataframe(
            marks_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No examination marks entered yet.")


# -----------------------------------
# PUBLISH RESULTS
# -----------------------------------

def publish_results():

    st.subheader("Publish Examination Results")

    if not st.session_state.exam_marks:

        st.warning(
            "No examination marks available. Enter marks before publishing results."
        )
        return

    marks_df = pd.DataFrame(
        st.session_state.exam_marks
    )

    marks_df["percentage"] = (
        marks_df["obtained_marks"]
        / marks_df["total_marks"]
        * 100
    ).round(2)

    marks_df["status"] = "Pass"

    marks_df.loc[
        marks_df["percentage"] < 40,
        "status"
    ] = "Fail"

    st.write("### Preview Results")

    st.dataframe(
        marks_df,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Passing percentage in this demo is 40%. "
        "This is a sample rule and can be changed."
    )

    if st.button(
        "Publish All Results",
        use_container_width=True
    ):

        st.session_state.published_results = marks_df.to_dict(
            orient="records"
        )

        st.success("Results published successfully!")


    st.divider()

    st.write("### Published Results")

    if st.session_state.published_results:

        published_df = pd.DataFrame(
            st.session_state.published_results
        )

        st.dataframe(
            published_df,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Published Result Records",
            len(published_df)
        )

    else:

        st.info("No results have been published yet.")


# -----------------------------------
# EXAMINATION OFFICER DASHBOARD
# -----------------------------------

def show_dashboard(user):

    initialize_exam_data()

    st.sidebar.title("Examination Panel")

    st.sidebar.write(
        f"Welcome, {user['name']}"
    )

    menu_items = [
        "Dashboard",
        "Create Examination",
        "Exam Schedule",
        "Enter Examination Marks",
        "Publish Results"
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


    st.title("Examination Officer Dashboard")

    st.write(
        f"Welcome back, {user['name']}!"
    )


    # Dashboard overview

    if selected_page == "Dashboard":

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Examinations",
                len(st.session_state.examinations)
            )

        with col2:

            st.metric(
                "Scheduled Exams",
                len(st.session_state.exam_schedules)
            )

        with col3:

            st.metric(
                "Published Results",
                len(st.session_state.published_results)
            )

        st.divider()

        st.subheader("Officer Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Officer ID:**",
                EXAM_OFFICER_PROFILE["officer_id"]
            )

            st.write(
                "**Name:**",
                EXAM_OFFICER_PROFILE["name"]
            )

        with col2:

            st.write(
                "**Email:**",
                EXAM_OFFICER_PROFILE["email"]
            )

            st.write(
                "**Department:**",
                EXAM_OFFICER_PROFILE["department"]
            )

        st.divider()

        st.subheader("Quick Overview")

        st.write(
            "Use the sidebar to create examinations, "
            "prepare schedules, enter student marks, "
            "and publish results."
        )


    elif selected_page == "Create Examination":

        create_examination()


    elif selected_page == "Exam Schedule":

        prepare_exam_schedule()


    elif selected_page == "Enter Examination Marks":

        enter_exam_marks()


    elif selected_page == "Publish Results":

        publish_results()