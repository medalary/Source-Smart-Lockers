import os
import cv2
import numpy as np
import pickle
from mtcnn import MTCNN
from keras_facenet import FaceNet

embedder = FaceNet()
detector = MTCNN()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "dataset")

def extract_face(img_path, required_size=(160, 160)):
    img = cv2.imread(img_path)
    if img is None:
        return None
    results = detector.detect_faces(img)
    if len(results) == 0:
        return None
    x, y, w, h = results[0]['box']
    x, y = max(x, 0), max(y, 0)
    face = img[y:y + h, x:x + w]
    face = cv2.resize(face, required_size)
    return face

face_data = {} 

for person_name in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person_name)
    if not os.path.isdir(person_path):
        continue
    face_data[person_name] = []
    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)
        face = extract_face(img_path)
        if face is not None:
            # Note: The original code used embedder.embeddings([face])[0]
            # If face_pixels normalization is intended (as discussed previously), it should be applied here.
            # Example for pixel normalization:
            # face_pixels = face.astype('float32')
            # mean, std = face_pixels.mean(), face_pixels.std()
            # face_pixels = (face_pixels - mean) / std
            # emb = embedder.embeddings(np.expand_dims(face_pixels, axis=0))[0]
            
            emb = embedder.embeddings([face])[0] # Original line from your provided snippet
            face_data[person_name].append(emb)
            print(f"Extracted embedding: {person_name} / {img_name}") 

embedding_dir = os.path.join(BASE_DIR, "Code", "embeddings")
os.makedirs(embedding_dir, exist_ok=True)
with open(os.path.join(embedding_dir, "face_cosine_data.pkl"), "wb") as f:
    pickle.dump(face_data, f)

print("Training successful! Embeddings saved to face_cosine_data.pkl") 