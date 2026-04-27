import os
import cv2
import numpy as np
from database import add_student
from face_detection import detect_faces, crop_face


def streamlit_image_to_cv2(uploaded_image):
    file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
    frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    return frame


def save_student_faces(name, student_code, department, uploaded_images):
    folder = f"known_faces/{student_code}"
    os.makedirs(folder, exist_ok=True)

    angle_names = ["front", "left", "right"]

    saved_count = 0

    for i, uploaded_image in enumerate(uploaded_images):
        frame = streamlit_image_to_cv2(uploaded_image)

        faces, gray = detect_faces(frame)

        if len(faces) == 0:
            return False, f"No face detected in image {i+1}. Please retake it."

        face = faces[0]
        cropped_face = crop_face(gray, face)

        image_path = f"{folder}/{student_code}_{angle_names[i]}.jpg"
        cv2.imwrite(image_path, cropped_face)

        saved_count += 1

    try:
        add_student(name, student_code, department, folder)
        return True, f"Student registered successfully with {saved_count} face images."
    except:
        return False, "Student ID already exists."