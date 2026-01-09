import cv2
import face_recognition
import pickle
import numpy as np
import os
import tkinter as tk
from attendance import mark_attendance

# ---------- Load encodings safely ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENCODINGS_PATH = os.path.join(BASE_DIR, "encodings.pickle")

with open(ENCODINGS_PATH, "rb") as f:
    known_encodings, known_names = pickle.load(f)

# ---------- GUI ----------
root = tk.Tk()
root.title("Face Attendance System")
label = tk.Label(root, text="Looking for face...", font=("Arial", 16))
label.pack()

cap = cv2.VideoCapture(0)
exit_program = False

# ---------- Main loop ----------
def run():
    global exit_program

    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    locations = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, locations)

    for enc, loc in zip(encodings, locations):
        distances = face_recognition.face_distance(known_encodings, enc)
        best_match = np.argmin(distances)

        name = "Unknown"

        if distances[best_match] < 0.55:
            name = known_names[best_match]
            print("Recognized:", name, "Distance:", distances[best_match])

            saved = mark_attendance(name)
            label.config(text=f"{name} Present")

            if saved:
                print("Attendance done. Exiting...")
                exit_program = True

        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
        cv2.putText(frame, name, (left, top-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

    cv2.imshow("Attendance System", frame)

    if exit_program:
        cap.release()
        cv2.destroyAllWindows()
        root.destroy()
        return

    root.after(10, run)

run()
root.mainloop()
