# University Learning Management System (LMS)

A demo University Learning Management System built with **Python** and **Streamlit**. It provides role-based dashboards for students, teachers, administrators, examination officers, accountants, and librarians.

> **Project status:** Educational/demo project. It uses sample data and Streamlit session state. It is not a production-ready university system.

## Features

The application includes six role-based dashboards:

| Role | Current features |
|---|---|
| Student | View profile, register/drop courses, view timetable, view attendance |
| Teacher | View assigned courses, timetable and student list; mark attendance; submit and view marks |
| Administrator | Dashboard and navigation placeholders for administrative operations |
| Examination Officer | Create examinations, prepare schedules, enter marks, publish results |
| Accountant | Manage fee structure, record demo payments, generate fee reports, check pending fees |
| Librarian | Add/update/search books, issue books and record returns |

Some planned student features and teacher features may not yet be implemented. Check the relevant dashboard before presenting them as completed.

## Technology

- Python
- Streamlit
- Pandas
- Python session state for temporary, shared application data

No database is currently used.

## Project structure

```text
University_LMS/
│
├── app.py
├── requirements.txt
│
├── data/
│   ├── sample_data.py
│   └── session_data.py
│
├── utils/
│   ├── authentication.py
│   └── helpers.py
│
├── views/
│   ├── login.py
│   ├── student.py
│   ├── teacher.py
│   ├── administrator.py
│   ├── examination.py
│   ├── accountant.py
│   └── librarian.py
│
└── assets/
```

## Requirements

- Python 3.10 or newer recommended
- pip
- Visual Studio Code or another Python editor

## Installation on Windows

Open PowerShell in the project folder.

### 1. Create a virtual environment

```powershell
python -m venv venv
```

### 2. Activate it

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If the requirements file has not yet been populated, install the packages used by the project:

```powershell
pip install streamlit pandas
```

### 4. Run the application

```powershell
streamlit run app.py
```

Streamlit will show a local URL in the terminal, usually:

```text
http://localhost:8501
```

Open that address in your browser.

## Demo login credentials

Use these sample accounts to explore each dashboard:

| Role | Username | Password |
|---|---|---|
| Student | `student` | `student123` |
| Teacher | `teacher` | `teacher123` |
| Administrator | `admin` | `admin123` |
| Examination Officer | `exam` | `exam123` |
| Accountant | `accountant` | `acc123` |
| Librarian | `librarian` | `lib123` |

These credentials are for local demonstration only. Do not use this authentication approach for a real deployment.

## Data and limitations

- Sample records are defined in `data/sample_data.py`.
- Shared collections are initialized in `data/session_data.py`.
- Changes are held in Streamlit session state and are not stored in a permanent database.
- Data may be lost when the browser session ends or the application restarts.
- Fee payments are recorded as demonstrations only. No real payment gateway is connected.
- Online classes, if represented in future versions, will require a real conferencing integration.
- Authentication uses demonstration credentials and is not suitable for production.
- The application should be tested with all six demo roles before a presentation.

## Development notes

When adding a feature that needs to be shared between roles, use a common `st.session_state` key rather than creating separate, disconnected copies of the same records. Initialize shared collections in `data/session_data.py`.

## Future improvements

- Complete the remaining administrator operations.
- Connect student views to teacher attendance and published examination results.
- Show student fee balances and library borrowing records in the Student dashboard.
- Complete additional student and teacher learning features.
- Add persistent storage and secure authentication if the project moves beyond a classroom demo.

## License

This project is intended for educational and demonstration purposes. Add a license file if you decide to distribute it publicly.
