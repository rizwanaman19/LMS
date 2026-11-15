import streamlit as st
import pandas as pd

from datetime import date

from data.sample_data import (
    LIBRARIAN_PROFILE,
    INITIAL_BOOKS,
    STUDENTS
)


# -----------------------------------
# INITIALIZE LIBRARY DATA
# -----------------------------------

def initialize_library_data():

    if "library_books" not in st.session_state:
        st.session_state.library_books = [
            book.copy() for book in INITIAL_BOOKS
        ]

    if "library_issues" not in st.session_state:
        st.session_state.library_issues = []

    if "library_returns" not in st.session_state:
        st.session_state.library_returns = []


# -----------------------------------
# ADD AND UPDATE BOOKS
# -----------------------------------

def manage_books():

    st.subheader("Add and Update Books")

    st.write("### Add a New Book")

    with st.form("add_book_form"):

        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Book Title")
            author = st.text_input("Author")

        with col2:
            isbn = st.text_input("ISBN")
            category = st.text_input("Category")

        quantity = st.number_input(
            "Total Quantity",
            min_value=1,
            value=1,
            step=1
        )

        submitted = st.form_submit_button(
            "Add Book",
            use_container_width=True
        )

        if submitted:

            if not all([
                title.strip(),
                author.strip(),
                isbn.strip(),
                category.strip()
            ]):
                st.error("Please complete all book details.")

            elif any(
                book["isbn"].lower() == isbn.strip().lower()
                for book in st.session_state.library_books
            ):
                st.error("A book with this ISBN already exists.")

            else:

                new_book = {
                    "book_id": (
                        f"BK-{len(st.session_state.library_books) + 1:03d}"
                    ),
                    "isbn": isbn.strip(),
                    "title": title.strip(),
                    "author": author.strip(),
                    "category": category.strip(),
                    "quantity": int(quantity),
                    "available": int(quantity)
                }

                st.session_state.library_books.append(new_book)

                st.success("Book added successfully!")

    st.divider()

    st.write("### Update Existing Book")

    books = st.session_state.library_books

    if not books:
        st.info("No books are available.")
        return

    book_options = {
        book["book_id"]: book
        for book in books
    }

    selected_book_id = st.selectbox(
        "Select a Book to Update",
        list(book_options.keys()),
        format_func=lambda book_id: (
            f"{book_options[book_id]['title']} "
            f"({book_id})"
        ),
        key="update_book_selection"
    )

    selected_book = book_options[selected_book_id]

    with st.form("update_book_form"):

        updated_title = st.text_input(
            "Book Title",
            value=selected_book["title"]
        )

        updated_author = st.text_input(
            "Author",
            value=selected_book["author"]
        )

        updated_isbn = st.text_input(
            "ISBN",
            value=selected_book["isbn"]
        )

        updated_category = st.text_input(
            "Category",
            value=selected_book["category"]
        )

        updated_quantity = st.number_input(
            "Total Quantity",
            min_value=1,
            value=int(selected_book["quantity"]),
            step=1
        )

        update_submitted = st.form_submit_button(
            "Update Book Details",
            use_container_width=True
        )

        if update_submitted:

            if not all([
                updated_title.strip(),
                updated_author.strip(),
                updated_isbn.strip(),
                updated_category.strip()
            ]):
                st.error("Please complete all book details.")

            elif any(
                book["isbn"].lower() == updated_isbn.strip().lower()
                and book["book_id"] != selected_book_id
                for book in books
            ):
                st.error("Another book already uses this ISBN.")

            else:

                issued_quantity = (
                    selected_book["quantity"]
                    - selected_book["available"]
                )

                if updated_quantity < issued_quantity:

                    st.error(
                        f"You cannot set the total quantity below "
                        f"{issued_quantity}, because those copies "
                        f"are currently issued."
                    )

                else:

                    selected_book["title"] = updated_title.strip()
                    selected_book["author"] = updated_author.strip()
                    selected_book["isbn"] = updated_isbn.strip()
                    selected_book["category"] = updated_category.strip()

                    selected_book["quantity"] = int(updated_quantity)

                    selected_book["available"] = (
                        int(updated_quantity) - issued_quantity
                    )

                    st.success("Book details updated successfully!")

    st.divider()

    st.write("### Library Book Records")

    books_df = pd.DataFrame(books)

    st.dataframe(
        books_df,
        use_container_width=True,
        hide_index=True
    )


# -----------------------------------
# SEARCH BOOKS
# -----------------------------------

def search_books():

    st.subheader("Search Library Books")

    books = st.session_state.library_books

    search_text = st.text_input(
        "Search by title, author, ISBN, or category",
        placeholder="Enter a book title or keyword..."
    )

    categories = sorted(
        set(book["category"] for book in books)
    )

    selected_category = st.selectbox(
        "Filter by Category",
        ["All Categories"] + categories
    )

    availability_filter = st.selectbox(
        "Availability",
        [
            "All Books",
            "Available Books",
            "Currently Unavailable"
        ]
    )

    filtered_books = []

    for book in books:

        searchable_text = (
            book["title"] + " "
            + book["author"] + " "
            + book["isbn"] + " "
            + book["category"]
        ).lower()

        matches_search = (
            search_text.strip().lower() in searchable_text
        )

        matches_category = (
            selected_category == "All Categories"
            or book["category"] == selected_category
        )

        if availability_filter == "Available Books":
            matches_availability = book["available"] > 0

        elif availability_filter == "Currently Unavailable":
            matches_availability = book["available"] == 0

        else:
            matches_availability = True

        if (
            matches_search
            and matches_category
            and matches_availability
        ):
            filtered_books.append(book)

    st.divider()

    st.write(f"### Search Results ({len(filtered_books)})")

    if filtered_books:

        results_df = pd.DataFrame(filtered_books)

        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning("No matching books found.")


# -----------------------------------
# ISSUE BOOKS
# -----------------------------------

def issue_books():

    st.subheader("Issue Books to Students")

    available_books = [
        book
        for book in st.session_state.library_books
        if book["available"] > 0
    ]

    if not available_books:

        st.warning("No books are currently available for issuing.")
        return

    book_options = {
        book["book_id"]: book
        for book in available_books
    }

    student_options = {
        student["student_id"]: student
        for student in STUDENTS
    }

    with st.form("issue_book_form"):

        selected_student_id = st.selectbox(
            "Select Student",
            list(student_options.keys()),
            format_func=lambda student_id: (
                f"{student_options[student_id]['name']} "
                f"({student_id})"
            )
        )

        selected_book_id = st.selectbox(
            "Select Book",
            list(book_options.keys()),
            format_func=lambda book_id: (
                f"{book_options[book_id]['title']} "
                f"(Available: {book_options[book_id]['available']})"
            )
        )

        issue_date = st.date_input(
            "Issue Date",
            value=date.today()
        )

        due_date = st.date_input(
            "Return Due Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Issue Book",
            use_container_width=True
        )

        if submitted:

            if due_date < issue_date:

                st.error(
                    "The return due date cannot be earlier than the issue date."
                )

            else:

                selected_book = book_options[selected_book_id]
                selected_student = student_options[selected_student_id]

                issue_record = {
                    "issue_id": (
                        f"ISS-{len(st.session_state.library_issues) + 1:03d}"
                    ),
                    "student_id": selected_student["student_id"],
                    "student_name": selected_student["name"],
                    "book_id": selected_book["book_id"],
                    "book_title": selected_book["title"],
                    "issue_date": str(issue_date),
                    "due_date": str(due_date),
                    "status": "Issued"
                }

                selected_book["available"] -= 1

                st.session_state.library_issues.append(
                    issue_record
                )

                st.success(
                    f"'{selected_book['title']}' issued to "
                    f"{selected_student['name']} successfully!"
                )

    st.divider()

    st.write("### Issued Books")

    if st.session_state.library_issues:

        issues_df = pd.DataFrame(
            st.session_state.library_issues
        )

        st.dataframe(
            issues_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No books have been issued yet.")


# -----------------------------------
# RECEIVE RETURNED BOOKS
# -----------------------------------

def return_books():

    st.subheader("Receive Returned Books")

    active_issues = [
        issue
        for issue in st.session_state.library_issues
        if issue["status"] == "Issued"
    ]

    if not active_issues:

        st.info("There are no books awaiting return.")
        return

    issue_options = {
        issue["issue_id"]: issue
        for issue in active_issues
    }

    with st.form("return_book_form"):

        selected_issue_id = st.selectbox(
            "Select Issued Book",
            list(issue_options.keys()),
            format_func=lambda issue_id: (
                f"{issue_options[issue_id]['book_title']} - "
                f"{issue_options[issue_id]['student_name']} "
                f"({issue_id})"
            )
        )

        return_date = st.date_input(
            "Return Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Confirm Book Return",
            use_container_width=True
        )

        if submitted:

            selected_issue = issue_options[selected_issue_id]

            selected_book = next(
                (
                    book
                    for book in st.session_state.library_books
                    if book["book_id"] == selected_issue["book_id"]
                ),
                None
            )

            if selected_book is None:

                st.error("The associated book record could not be found.")

            elif return_date < date.fromisoformat(
                selected_issue["issue_date"]
            ):

                st.error(
                    "Return date cannot be earlier than the issue date."
                )

            else:

                selected_issue["status"] = "Returned"
                selected_issue["return_date"] = str(return_date)

                selected_book["available"] += 1

                return_record = {
                    "issue_id": selected_issue["issue_id"],
                    "student_id": selected_issue["student_id"],
                    "student_name": selected_issue["student_name"],
                    "book_id": selected_book["book_id"],
                    "book_title": selected_book["title"],
                    "return_date": str(return_date)
                }

                st.session_state.library_returns.append(
                    return_record
                )

                st.success("Book returned successfully!")

    st.divider()

    st.write("### Returned Book History")

    if st.session_state.library_returns:

        returns_df = pd.DataFrame(
            st.session_state.library_returns
        )

        st.dataframe(
            returns_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No books have been returned yet.")


# -----------------------------------
# LIBRARIAN DASHBOARD
# -----------------------------------

def show_dashboard(user):

    initialize_library_data()

    st.sidebar.title("Librarian Panel")

    st.sidebar.write(
        f"Welcome, {user['name']}"
    )

    menu_items = [
        "Dashboard",
        "Add and Update Books",
        "Search Books",
        "Issue Books",
        "Receive Returned Books"
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

    st.title("Librarian Dashboard")

    st.write(
        f"Welcome back, {user['name']}!"
    )

    # Dashboard overview

    if selected_page == "Dashboard":

        books = st.session_state.library_books
        issues = st.session_state.library_issues

        total_books = sum(
            book["quantity"] for book in books
        )

        available_books = sum(
            book["available"] for book in books
        )

        currently_issued = sum(
            1 for issue in issues
            if issue["status"] == "Issued"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Book Copies",
                total_books
            )

        with col2:

            st.metric(
                "Available Copies",
                available_books
            )

        with col3:

            st.metric(
                "Currently Issued",
                currently_issued
            )

        st.divider()

        st.subheader("Librarian Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Officer ID:**",
                LIBRARIAN_PROFILE["officer_id"]
            )

            st.write(
                "**Name:**",
                LIBRARIAN_PROFILE["name"]
            )

        with col2:

            st.write(
                "**Email:**",
                LIBRARIAN_PROFILE["email"]
            )

            st.write(
                "**Department:**",
                LIBRARIAN_PROFILE["department"]
            )

        st.divider()

        st.subheader("Recent Library Activity")

        if issues:

            issues_df = pd.DataFrame(issues)

            st.dataframe(
                issues_df.tail(5),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info("No library activity recorded yet.")

    elif selected_page == "Add and Update Books":

        manage_books()

    elif selected_page == "Search Books":

        search_books()

    elif selected_page == "Issue Books":

        issue_books()

    elif selected_page == "Receive Returned Books":

        return_books()