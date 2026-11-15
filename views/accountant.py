import streamlit as st
import pandas as pd

from datetime import date

from data.sample_data import (
    ACCOUNTANT_PROFILE,
    FEE_STRUCTURE,
    INITIAL_FEE_ACCOUNTS
)


# -----------------------------------
# INITIALIZE ACCOUNTANT DATA
# -----------------------------------

def initialize_accountant_data():

    if "fee_structure" not in st.session_state:
        st.session_state.fee_structure = [
            item.copy() for item in FEE_STRUCTURE
        ]

    if "fee_accounts" not in st.session_state:
        st.session_state.fee_accounts = [
            item.copy() for item in INITIAL_FEE_ACCOUNTS
        ]

    if "fee_payments" not in st.session_state:
        st.session_state.fee_payments = []


# -----------------------------------
# HELPER: GET FEE BALANCE
# -----------------------------------

def get_fee_balance(account):

    return account["total_fee"] - account["paid_amount"]


# -----------------------------------
# MANAGE FEE STRUCTURE
# -----------------------------------

def manage_fee_structure():

    st.subheader("Manage Fee Structure")

    st.write("View existing fee components or add a new component.")

    with st.form("add_fee_component_form"):

        col1, col2 = st.columns(2)

        with col1:
            semester = st.selectbox(
                "Semester",
                [
                    "1st Semester",
                    "2nd Semester",
                    "3rd Semester",
                    "4th Semester",
                    "5th Semester",
                    "6th Semester",
                    "7th Semester",
                    "8th Semester"
                ]
            )

        with col2:
            fee_type = st.text_input(
                "Fee Component",
                placeholder="e.g. Transport Fee"
            )

        amount = st.number_input(
            "Fee Amount (PKR)",
            min_value=1,
            value=1000,
            step=500
        )

        submitted = st.form_submit_button(
            "Add Fee Component",
            use_container_width=True
        )

        if submitted:

            if not fee_type.strip():

                st.error("Please enter a fee component name.")

            else:

                new_component = {
                    "semester": semester,
                    "fee_type": fee_type.strip(),
                    "amount": amount
                }

                st.session_state.fee_structure.append(
                    new_component
                )

                st.success("Fee component added successfully!")

    st.divider()

    st.write("### Current Fee Structure")

    fee_df = pd.DataFrame(
        st.session_state.fee_structure
    )

    st.dataframe(
        fee_df,
        use_container_width=True,
        hide_index=True
    )

    total_structure_fee = sum(
        item["amount"]
        for item in st.session_state.fee_structure
        if item["semester"] == "6th Semester"
    )

    st.metric(
        "6th Semester Fee Structure Total",
        f"PKR {total_structure_fee:,.0f}"
    )

    st.caption(
        "Adding a fee component updates the fee structure list. "
        "Existing student invoices are not automatically changed."
    )


# -----------------------------------
# RECORD FEE PAYMENT
# -----------------------------------

def record_fee_payment():

    st.subheader("Record Student Fee Payment")

    accounts = st.session_state.fee_accounts

    unpaid_accounts = [
        account
        for account in accounts
        if get_fee_balance(account) > 0
    ]

    if not unpaid_accounts:

        st.success("All student fees have been paid.")
        return

    student_options = {
        account["student_id"]: account
        for account in unpaid_accounts
    }

    with st.form("record_payment_form"):

        selected_student_id = st.selectbox(
            "Select Student",
            list(student_options.keys()),
            format_func=lambda student_id: (
                f"{student_options[student_id]['student_name']} "
                f"({student_id})"
            )
        )

        account = student_options[selected_student_id]

        outstanding = get_fee_balance(account)

        st.info(
            f"Outstanding Balance: PKR {outstanding:,.0f}"
        )

        payment_amount = st.number_input(
            "Payment Amount (PKR)",
            min_value=1.0,
            max_value=float(outstanding),
            value=1.0,
            step=500.0
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Cash",
                "Bank Transfer",
                "Online Banking",
                "Other"
            ]
        )

        payment_date = st.date_input(
            "Payment Date",
            value=date.today()
        )

        submitted = st.form_submit_button(
            "Save Payment",
            use_container_width=True
        )

        if submitted:

            if payment_amount > outstanding:

                st.error(
                    "Payment cannot exceed the outstanding balance."
                )

            else:

                account["paid_amount"] += payment_amount

                payment_record = {
                    "payment_id": (
                        f"PAY-{len(st.session_state.fee_payments) + 1:03d}"
                    ),
                    "student_id": account["student_id"],
                    "student_name": account["student_name"],
                    "amount": payment_amount,
                    "payment_method": payment_method,
                    "payment_date": str(payment_date)
                }

                st.session_state.fee_payments.append(
                    payment_record
                )

                st.success("Fee payment recorded successfully!")

                st.write(
                    f"Remaining Balance: "
                    f"PKR {get_fee_balance(account):,.0f}"
                )

    st.divider()

    st.write("### Recent Payments")

    if st.session_state.fee_payments:

        payments_df = pd.DataFrame(
            st.session_state.fee_payments
        )

        st.dataframe(
            payments_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No payment records available yet.")


# -----------------------------------
# GENERATE FEE REPORT
# -----------------------------------

def generate_fee_report():

    st.subheader("Fee Collection Report")

    accounts = st.session_state.fee_accounts

    total_fee = sum(
        account["total_fee"]
        for account in accounts
    )

    total_paid = sum(
        account["paid_amount"]
        for account in accounts
    )

    total_pending = total_fee - total_paid

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Fee",
            f"PKR {total_fee:,.0f}"
        )

    with col2:
        st.metric(
            "Collected Amount",
            f"PKR {total_paid:,.0f}"
        )

    with col3:
        st.metric(
            "Pending Amount",
            f"PKR {total_pending:,.0f}"
        )

    st.divider()

    st.write("### Student Fee Report")

    report_records = []

    for account in accounts:

        pending = get_fee_balance(account)

        if account["paid_amount"] == 0:
            status = "Unpaid"

        elif pending == 0:
            status = "Paid"

        else:
            status = "Partially Paid"

        report_records.append({
            "Student ID": account["student_id"],
            "Student Name": account["student_name"],
            "Total Fee": account["total_fee"],
            "Paid Amount": account["paid_amount"],
            "Pending Amount": pending,
            "Status": status
        })

    report_df = pd.DataFrame(report_records)

    st.dataframe(
        report_df,
        use_container_width=True,
        hide_index=True
    )

    st.write("### Payment Transaction History")

    if st.session_state.fee_payments:

        payments_df = pd.DataFrame(
            st.session_state.fee_payments
        )

        st.dataframe(
            payments_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No payment transactions have been recorded.")

    csv_data = report_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Fee Report (CSV)",
        data=csv_data,
        file_name="student_fee_report.csv",
        mime="text/csv",
        use_container_width=True
    )


# -----------------------------------
# CHECK PENDING FEES
# -----------------------------------

def check_pending_fees():

    st.subheader("Pending Student Fees")

    pending_accounts = [
        account
        for account in st.session_state.fee_accounts
        if get_fee_balance(account) > 0
    ]

    if pending_accounts:

        pending_records = []

        for account in pending_accounts:

            pending_records.append({
                "Student ID": account["student_id"],
                "Student Name": account["student_name"],
                "Total Fee": account["total_fee"],
                "Paid Amount": account["paid_amount"],
                "Pending Amount": get_fee_balance(account),
                "Due Date": account["due_date"]
            })

        pending_df = pd.DataFrame(pending_records)

        st.metric(
            "Students with Pending Fees",
            len(pending_accounts)
        )

        st.metric(
            "Total Outstanding Fees",
            f"PKR {sum(get_fee_balance(a) for a in pending_accounts):,.0f}"
        )

        st.dataframe(
            pending_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.success("There are no pending student fees.")


# -----------------------------------
# ACCOUNTANT DASHBOARD
# -----------------------------------

def show_dashboard(user):

    initialize_accountant_data()

    st.sidebar.title("Accountant Panel")

    st.sidebar.write(
        f"Welcome, {user['name']}"
    )

    menu_items = [
        "Dashboard",
        "Manage Fee Structure",
        "Record Fee Payment",
        "Generate Fee Report",
        "Check Pending Fees"
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

    st.title("Accountant Dashboard")

    st.write(
        f"Welcome back, {user['name']}!"
    )

    # Dashboard overview

    if selected_page == "Dashboard":

        accounts = st.session_state.fee_accounts

        total_fee = sum(
            account["total_fee"]
            for account in accounts
        )

        total_paid = sum(
            account["paid_amount"]
            for account in accounts
        )

        total_pending = total_fee - total_paid

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Students",
                len(accounts)
            )

        with col2:

            st.metric(
                "Total Collected",
                f"PKR {total_paid:,.0f}"
            )

        with col3:

            st.metric(
                "Pending Fees",
                f"PKR {total_pending:,.0f}"
            )

        st.divider()

        st.subheader("Accountant Information")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Officer ID:**",
                ACCOUNTANT_PROFILE["officer_id"]
            )

            st.write(
                "**Name:**",
                ACCOUNTANT_PROFILE["name"]
            )

        with col2:

            st.write(
                "**Email:**",
                ACCOUNTANT_PROFILE["email"]
            )

            st.write(
                "**Department:**",
                ACCOUNTANT_PROFILE["department"]
            )

        st.divider()

        st.subheader("Fee Collection Overview")

        if total_fee > 0:

            collection_percentage = (
                total_paid / total_fee
            ) * 100

            st.progress(
                int(collection_percentage)
            )

            st.write(
                f"Fee Collection: {collection_percentage:.1f}%"
            )

        st.info(
            "Use the sidebar to manage fee structures, "
            "record payments, generate reports, "
            "and check pending fees."
        )

    elif selected_page == "Manage Fee Structure":

        manage_fee_structure()

    elif selected_page == "Record Fee Payment":

        record_fee_payment()

    elif selected_page == "Generate Fee Report":

        generate_fee_report()

    elif selected_page == "Check Pending Fees":

        check_pending_fees()