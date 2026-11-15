# --------------------------------
# STUDENT INFORMATION
# --------------------------------
STUDENT_PROFILE = {
    "student_id": "STU-2026-001",
    "name": "Aman Siddiqui",
    "email": "ali@example.com",
    "department": "Computer Science",
    "semester": "5th Semester",
    "program": "BS Computer Science",
    "session": "2023-2027",
    "cgpa": 3.45
}
# --------------------------------
# AVAILABLE COURSES
# --------------------------------
COURSES = [
    {
        "course_id": "CS301",
        "course_name": "Artificial Intelligence",
        "credit_hours": 3,
        "teacher": "Mr. Ahmed"
    },
    {
        "course_id": "CS302",
        "course_name": "Machine Learning",
        "credit_hours": 3,
        "teacher": "Mr. Bilal"
    },
    {
        "course_id": "CS303",
        "course_name": "Database Systems",
        "credit_hours": 3,
        "teacher": "Ms. Sara"
    },
    {
        "course_id": "CS304",
        "course_name": "Software Engineering",
        "credit_hours": 3,
        "teacher": "Mr. Usman"
    },
    {
        "course_id": "CS305",
        "course_name": "Computer Networks",
        "credit_hours": 3,
        "teacher": "Ms. Ayesha"
    },
    {
        "course_id": "CS306",
        "course_name": "Web Development",
        "credit_hours": 3,
        "teacher": "Mr. Hamza"
    }
]
# --------------------------------
# INITIAL ENROLLED COURSES
# --------------------------------
INITIAL_ENROLLED_COURSES = [
    "CS301",
    "CS303",
    "CS304"
]
# --------------------------------
# ATTENDANCE RECORDS
# --------------------------------

ATTENDANCE = [
    {
        "course": "Artificial Intelligence",
        "total_classes": 20,
        "present": 18,
        "absent": 2
    },
    {
        "course": "Database Systems",
        "total_classes": 18,
        "present": 16,
        "absent": 2
    },
    {
        "course": "Software Engineering",
        "total_classes": 22,
        "present": 20,
        "absent": 2
    }
]


# --------------------------------
# CLASS TIMETABLE
# --------------------------------

TIMETABLE = [
    {
        "day": "Monday",
        "time": "09:00 - 10:30",
        "course": "Artificial Intelligence",
        "room": "Lab 01"
    },
    {
        "day": "Tuesday",
        "time": "10:30 - 12:00",
        "course": "Database Systems",
        "room": "Room 202"
    },
    {
        "day": "Wednesday",
        "time": "09:00 - 10:30",
        "course": "Software Engineering",
        "room": "Room 105"
    },
    {
        "day": "Thursday",
        "time": "11:00 - 12:30",
        "course": "Artificial Intelligence",
        "room": "Lab 01"
    },
    {
        "day": "Friday",
        "time": "10:30 - 12:00",
        "course": "Database Systems",
        "room": "Room 202"
    }
]

# -----------------------------------
# TEACHER SAMPLE DATA
# -----------------------------------

TEACHER_PROFILE = {
    "teacher_id": "TCH-2026-001",
    "name": "Ahmed Khan",
    "email": "ahmed@example.com",
    "department": "Computer Science",
    "designation": "Lecturer"
}

TEACHER_COURSES = [
    {
        "course_id": "CS301",
        "course_name": "Artificial Intelligence",
        "credit_hours": 3,
        "semester": "6th Semester"
    },
    {
        "course_id": "CS302",
        "course_name": "Machine Learning",
        "credit_hours": 3,
        "semester": "6th Semester"
    },
    {
        "course_id": "CS305",
        "course_name": "Computer Networks",
        "credit_hours": 3,
        "semester": "6th Semester"
    }
]

TEACHER_TIMETABLE = [
    {
        "day": "Monday",
        "time": "09:00 - 10:30",
        "course": "Artificial Intelligence",
        "room": "Lab 01"
    },
    {
        "day": "Tuesday",
        "time": "11:00 - 12:30",
        "course": "Machine Learning",
        "room": "Room 203"
    },
    {
        "day": "Wednesday",
        "time": "09:00 - 10:30",
        "course": "Computer Networks",
        "room": "Room 105"
    },
    {
        "day": "Thursday",
        "time": "09:00 - 10:30",
        "course": "Artificial Intelligence",
        "room": "Lab 01"
    },
    {
        "day": "Friday",
        "time": "11:00 - 12:30",
        "course": "Machine Learning",
        "room": "Room 203"
    }
]

STUDENTS = [
    {
        "student_id": "STU-001",
        "name": "Ali Khan",
        "department": "Computer Science",
        "semester": "6th Semester"
    },
    {
        "student_id": "STU-002",
        "name": "Usman Ali",
        "department": "Computer Science",
        "semester": "6th Semester"
    },
    {
        "student_id": "STU-003",
        "name": "Sara Ahmed",
        "department": "Computer Science",
        "semester": "6th Semester"
    },
    {
        "student_id": "STU-004",
        "name": "Hassan Khan",
        "department": "Computer Science",
        "semester": "6th Semester"
    },
    {
        "student_id": "STU-005",
        "name": "Ayesha Noor",
        "department": "Computer Science",
        "semester": "6th Semester"
    }
]

# -----------------------------------
# EXAMINATION OFFICER SAMPLE DATA
# -----------------------------------

EXAM_COURSES = [
    {
        "course_id": "CS301",
        "course_name": "Artificial Intelligence"
    },
    {
        "course_id": "CS302",
        "course_name": "Machine Learning"
    },
    {
        "course_id": "CS303",
        "course_name": "Database Systems"
    },
    {
        "course_id": "CS304",
        "course_name": "Software Engineering"
    },
    {
        "course_id": "CS305",
        "course_name": "Computer Networks"
    }
]

EXAM_OFFICER_PROFILE = {
    "officer_id": "EXM-2026-001",
    "name": "Examination Officer",
    "email": "exam@example.com",
    "department": "Examination Department"
}

# -----------------------------------
# ACCOUNTANT SAMPLE DATA
# -----------------------------------

ACCOUNTANT_PROFILE = {
    "officer_id": "ACC-2026-001",
    "name": "Finance Officer",
    "email": "accountant@example.com",
    "department": "Finance Department"
}

FEE_STRUCTURE = [
    {
        "semester": "6th Semester",
        "fee_type": "Tuition Fee",
        "amount": 45000
    },
    {
        "semester": "6th Semester",
        "fee_type": "Laboratory Fee",
        "amount": 5000
    },
    {
        "semester": "6th Semester",
        "fee_type": "Library Fee",
        "amount": 2000
    },
    {
        "semester": "6th Semester",
        "fee_type": "Examination Fee",
        "amount": 3000
    }
]

INITIAL_FEE_ACCOUNTS = [
    {
        "student_id": "STU-001",
        "student_name": "Ali Khan",
        "semester": "6th Semester",
        "total_fee": 55000,
        "paid_amount": 30000,
        "due_date": "2026-12-15"
    },
    {
        "student_id": "STU-002",
        "student_name": "Usman Ali",
        "semester": "6th Semester",
        "total_fee": 55000,
        "paid_amount": 55000,
        "due_date": "2026-12-15"
    },
    {
        "student_id": "STU-003",
        "student_name": "Sara Ahmed",
        "semester": "6th Semester",
        "total_fee": 55000,
        "paid_amount": 20000,
        "due_date": "2026-12-15"
    },
    {
        "student_id": "STU-004",
        "student_name": "Hassan Khan",
        "semester": "6th Semester",
        "total_fee": 55000,
        "paid_amount": 0,
        "due_date": "2026-12-15"
    },
    {
        "student_id": "STU-005",
        "student_name": "Ayesha Noor",
        "semester": "6th Semester",
        "total_fee": 55000,
        "paid_amount": 40000,
        "due_date": "2026-12-15"
    }
]

# -----------------------------------
# LIBRARIAN SAMPLE DATA
# -----------------------------------

LIBRARIAN_PROFILE = {
    "officer_id": "LIB-2026-001",
    "name": "Library Officer",
    "email": "librarian@example.com",
    "department": "Central Library"
}

INITIAL_BOOKS = [
    {
        "book_id": "BK-001",
        "isbn": "9780131103627",
        "title": "The C Programming Language",
        "author": "Brian W. Kernighan",
        "category": "Programming",
        "quantity": 5,
        "available": 5
    },
    {
        "book_id": "BK-002",
        "isbn": "9780132350884",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "category": "Software Engineering",
        "quantity": 4,
        "available": 4
    },
    {
        "book_id": "BK-003",
        "isbn": "9780262033848",
        "title": "Introduction to Algorithms",
        "author": "Thomas H. Cormen",
        "category": "Algorithms",
        "quantity": 3,
        "available": 3
    },
    {
        "book_id": "BK-004",
        "isbn": "9781491950296",
        "title": "Fundamentals of Data Engineering",
        "author": "Joe Reis",
        "category": "Data Engineering",
        "quantity": 2,
        "available": 2
    },
    {
        "book_id": "BK-005",
        "isbn": "9780134685991",
        "title": "Effective Java",
        "author": "Joshua Bloch",
        "category": "Programming",
        "quantity": 3,
        "available": 3
    }
]