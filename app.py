import streamlit as st
import pandas as pd
from database import create_tables, get_students, get_attendance, delete_student
from attendance import start_attendance
from register_student import save_student_faces
import os
import shutil

create_tables()

st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Smart Attendance System")
st.write("Face Recognition Attendance System")

menu = st.sidebar.selectbox(
    "Choose Page",
    ["Home", "Register Student", "Start Attendance", "Students", "Attendance Report"]
)

if menu == "Home":
    st.header("Project Idea")
    st.write("""
    This system uses the camera to recognize students' faces and automatically mark their attendance.
    """)

elif menu == "Register Student":
    st.header("Register New Student")

    name = st.text_input("Student Name")
    student_code = st.text_input("Student ID")
    department = st.text_input("Department")

    st.write("Capture 3 face images from different angles:")

    image_front = st.camera_input("1) Front face")
    image_left = st.camera_input("2) Slightly turn left")
    image_right = st.camera_input("3) Slightly turn right")

    if st.button("Register Student"):
        if name and student_code and department and image_front and image_left and image_right:
            success, message = save_student_faces(
                name,
                student_code,
                department,
                [image_front, image_left, image_right]
            )

            if success:
                st.success(message)
            else:
                st.error(message)
        else:
            st.warning("Please fill all fields and capture all 3 images.")
elif menu == "Start Attendance":
    st.header("Start Attendance")

    if "camera_running" not in st.session_state:
        st.session_state.camera_running = False

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start Camera"):
            st.session_state.camera_running = True
            start_attendance()

    with col2:
        if st.button("End Camera"):
            st.session_state.camera_running = False
            st.warning("Camera stopped.")
            
elif menu == "Students":
    st.header("Registered Students")

    students = get_students()

    if students:
        df = pd.DataFrame(
            students,
            columns=["Name", "Student Code", "Department", "Image Path"]
        )

        st.dataframe(df)

        st.subheader("Delete Student")

        student_codes = [student[1] for student in students]

        selected_code = st.selectbox(
            "Choose Student ID to delete",
            student_codes
        )

        if st.button("Delete Student"):
            delete_student(selected_code)

            image_folder = f"known_faces/{selected_code}"
            image_file = f"known_faces/{selected_code}.jpg"

            if os.path.exists(image_folder):
                shutil.rmtree(image_folder)

            if os.path.exists(image_file):
                os.remove(image_file)

            st.success(f"Student {selected_code} deleted successfully.")
            st.rerun()

    else:
        st.info("No students registered yet.")
elif menu == "Attendance Report":
    st.header("Attendance Report")

    records = get_attendance()

    if records:
        df = pd.DataFrame(
            records,
            columns=["Student Code", "Name", "Date", "Time", "Status"]
        )

        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download CSV Report",
            data=csv,
            file_name="attendance_report.csv",
            mime="text/csv"
        )
    else:
        st.info("No attendance records yet.")