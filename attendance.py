import cv2
import numpy as np
import streamlit as st
from database import get_students, mark_attendance
import os


def prepare_training_data():
    students = get_students()

    faces = []
    labels = []
    label_map = {}

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    label_id = 0

    for name, student_code, department, folder_path in students:

        if not os.path.exists(folder_path):
            continue

        for file in os.listdir(folder_path):
            img_path = os.path.join(folder_path, file)

            img = cv2.imread(img_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            detected_faces = face_detector.detectMultiScale(gray, 1.2, 5)

            for (x, y, w, h) in detected_faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (200, 200))

                faces.append(face)
                labels.append(label_id)

                label_map[label_id] = {
                    "name": name,
                    "student_code": student_code
                }

                label_id += 1

    return faces, np.array(labels), label_map


def start_attendance():
    faces, labels, label_map = prepare_training_data()

    if len(faces) == 0:
        st.error("No registered students found.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, labels)

    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)

    stframe = st.empty()

    while st.session_state.camera_running:
        ret, frame = cap.read()

        if not ret:
            st.error("Camera error.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        detected_faces = face_detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in detected_faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            label, confidence = recognizer.predict(face)

            name = "Unknown"

            if confidence < 80:
                student = label_map[label]
                name = student["name"]
                student_code = student["student_code"]

                mark_attendance(student_code, name)

                color = (0, 255, 0)
                text = f"{name}"
            else:
                color = (0, 0, 255)
                text = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, text, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame, channels="RGB")

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()
    stframe.empty()