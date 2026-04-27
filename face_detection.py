import cv2

def detect_faces(frame):
    face_detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5
    )

    return faces, gray


def crop_face(gray_image, face):
    x, y, w, h = face
    cropped_face = gray_image[y:y+h, x:x+w]
    cropped_face = cv2.resize(cropped_face, (200, 200))
    return cropped_face