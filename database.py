import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        student_code TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        image_path TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_code TEXT NOT NULL,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def add_student(name, student_code, department, image_path):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students (name, student_code, department, image_path)
    VALUES (?, ?, ?, ?)
    """, (name, student_code, department, image_path))

    conn.commit()
    conn.close()

def get_students():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT name, student_code, department, image_path FROM students")
    students = cursor.fetchall()

    conn.close()
    return students

def mark_attendance(student_code, name):
    conn = connect_db()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    cursor.execute("""
    SELECT * FROM attendance
    WHERE student_code = ? AND date = ?
    """, (student_code, today))

    already_exists = cursor.fetchone()

    if already_exists:
        conn.close()
        return False

    cursor.execute("""
    INSERT INTO attendance (student_code, name, date, time, status)
    VALUES (?, ?, ?, ?, ?)
    """, (student_code, name, today, current_time, "Present"))

    conn.commit()
    conn.close()
    return True

def get_attendance():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT student_code, name, date, time, status FROM attendance")
    records = cursor.fetchall()

    conn.close()
    return records

def delete_student(student_code):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE student_code = ?", (student_code,))
    cursor.execute("DELETE FROM attendance WHERE student_code = ?", (student_code,))

    conn.commit()
    conn.close()