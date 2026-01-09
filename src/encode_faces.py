import face_recognition
import os
import pickle

# Always use absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "..", "data", "known_faces")

encodings = []
names = []

if not os.path.exists(KNOWN_FACES_DIR):
    print("ERROR: Folder not found:", KNOWN_FACES_DIR)
    print("Create folders like data/known_faces/PersonName/image.jpg")
    exit()

for person in os.listdir(KNOWN_FACES_DIR):
    person_path = os.path.join(KNOWN_FACES_DIR, person)

    if not os.path.isdir(person_path):
        continue

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        image = face_recognition.load_image_file(img_path)
        faces = face_recognition.face_encodings(image)

        if faces:
            encodings.append(faces[0])
            names.append(person)
            print("Encoded:", person, img_name)
        else:
            print("No face found in:", img_name)

ENCODINGS_PATH = os.path.join(BASE_DIR, "encodings.pickle")

with open(ENCODINGS_PATH, "wb") as f:
    pickle.dump((encodings, names), f)

print("Encodings saved to:", ENCODINGS_PATH)
print("Total faces encoded:", len(encodings))
