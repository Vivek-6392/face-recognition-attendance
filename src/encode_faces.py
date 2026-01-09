import face_recognition
import os
import pickle

KNOWN_FACES_DIR = "../data/known_faces"
encodings = []
names = []

for person in os.listdir(KNOWN_FACES_DIR):
    person_path = os.path.join(KNOWN_FACES_DIR, person)
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        image = face_recognition.load_image_file(img_path)
        face_enc = face_recognition.face_encodings(image)

        if face_enc:
            encodings.append(face_enc[0])
            names.append(person)

with open("encodings.pickle", "wb") as f:
    pickle.dump((encodings, names), f)

print("Encodings saved successfully")
