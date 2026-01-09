import cv2
import face_recognition
import pickle
from attendance import mark_attendance

with open("encodings.pickle", "rb") as f:
    known_encodings, known_names = pickle.load(f)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for enc, loc in zip(encodings, locations):
        matches = face_recognition.compare_faces(known_encodings, enc)
        name = "Unknown"

        if True in matches:
            idx = matches.index(True)
            name = known_names[idx]
            mark_attendance(name)

        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.imshow("Attendance System", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
