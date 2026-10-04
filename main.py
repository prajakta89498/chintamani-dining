from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3


# ============================================================
# CHINTAMANI DINING - FASTAPI BACKEND
# ============================================================

app = FastAPI(title="Chintamani Dining API")


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DATABASE
# ============================================================

DATABASE = "chintamani_new.db"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            gender TEXT NOT NULL,
            fee INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()


# ============================================================
# STUDENT DATA MODEL
# ============================================================

class Student(BaseModel):

    name: str
    mobile: str
    gender: str


# ============================================================
# HOME ROUTE
# ============================================================

@app.get("/")
def home():

    return {
        "success": True,
        "message": "Chintamani Dining Backend is Running!"
    }


# ============================================================
# REGISTER STUDENT
# ============================================================

@app.post("/register")
def register_student(student: Student):

    print("Received registration:", student)


    # Convert gender to lowercase
    gender = student.gender.strip().lower()


    # ========================================================
    # MESS FEE
    # ========================================================

    if gender == "girls":

        fee = 2400

    elif gender == "boys":

        fee = 2800

    else:

        return {
            "success": False,
            "message": "Invalid gender selected."
        }


    # ========================================================
    # DATABASE
    # ========================================================

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()


    cursor.execute("""
        INSERT INTO students
        (
            name,
            mobile,
            gender,
            fee
        )
        VALUES (?, ?, ?, ?)
    """, (
        student.name,
        student.mobile,
        student.gender,
        fee
    ))


    connection.commit()

    student_id = cursor.lastrowid

    connection.close()


    print("Registration successful:", student.name)


    # ========================================================
    # RESPONSE
    # ========================================================

    return {

        "success": True,

        "message": "Registration successful!",

        "student_id": student_id,

        "name": student.name,

        "mobile": student.mobile,

        "gender": student.gender,

        "fee": fee
    }


# ============================================================
# GET ALL STUDENTS
# ============================================================

@app.get("/students")
def get_students():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            name,
            mobile,
            gender,
            fee
        FROM students
        ORDER BY id DESC
    """)


    students = cursor.fetchall()

    connection.close()


    return {

        "success": True,

        "count": len(students),

        "students": [
            dict(student)
            for student in students
        ]
    }


# ============================================================
# GET ONE STUDENT
# ============================================================

@app.get("/students/{student_id}")
def get_student(student_id: int):

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()


    cursor.execute("""
        SELECT
            id,
            name,
            mobile,
            gender,
            fee
        FROM students
        WHERE id = ?
    """, (student_id,))


    student = cursor.fetchone()

    connection.close()


    if student is None:

        return {
            "success": False,
            "message": "Student not found."
        }


    return {

        "success": True,

        "student": dict(student)
    }


# ============================================================
# DELETE STUDENT
# ============================================================

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()


    cursor.execute("""
        DELETE FROM students
        WHERE id = ?
    """, (student_id,))


    connection.commit()

    deleted = cursor.rowcount

    connection.close()


    if deleted == 0:

        return {
            "success": False,
            "message": "Student not found."
        }


    return {

        "success": True,

        "message": "Student deleted successfully.",

        "student_id": student_id
    }