
# --------------------------------
# DEMO USER ACCOUNTS
# --------------------------------

USERS = {
    "aman": {
        "password": "aman123",
        "name": "Aman Siddiqui",
        "role": "Student"
    },

    "teacher": {
        "password": "teacher123",
        "name": "Ahmed Khan",
        "role": "Teacher"
    },

    "admin": {
        "password": "admin123",
        "name": "System Administrator",
        "role": "Administrator"
    },

    "exam": {
        "password": "exam123",
        "name": "Examination Officer",
        "role": "Examination Officer"
    },

    "accountant": {
        "password": "acc123",
        "name": "Finance Officer",
        "role": "Accountant"
    },

    "librarian": {
        "password": "lib123",
        "name": "Library Officer",
        "role": "Librarian"
    }
}


# --------------------------------
# LOGIN VALIDATION
# --------------------------------

def authenticate_user(username, password):

    user = USERS.get(username)

    if user and user["password"] == password:
        return {
            "username": username,
            "name": user["name"],
            "role": user["role"]
        }

    return None
