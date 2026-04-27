import cv2
from face_detection import detect_faces

def open_camera_with_face_box():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera could not be opened.")
        return

    print("Camera started.")
    print("Press Q to stop.")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Could not read frame.")
            break

        faces, gray = detect_faces(frame)

        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Face Detected",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        cv2.imshow("Camera - Face Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    open_camera_with_face_box()
    