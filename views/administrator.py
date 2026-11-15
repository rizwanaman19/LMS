
from utils.helpers import render_role_dashboard


def show_dashboard(user):

    menu_items = [
        "Dashboard",
        "Manage Students",
        "Manage Teachers",
        "Manage Departments",
        "Manage Courses",
        "Assign Teachers",
        "Manage Classrooms",
        "Generate Timetable"
    ]

    render_role_dashboard(
        "Administrator",
        user,
        menu_items
    )
