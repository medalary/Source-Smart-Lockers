import pickle
import os
import numpy as np # Import numpy for array comparison

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adjust this path if your face_cosine_data.pkl is in a different location
# This path assumes 'check_train.py' is at the same level as 'train.py'
# and 'face_cosine_data.pkl' is inside 'Code/embeddings' relative to BASE_DIR
embeddings_file_path = os.path.join(BASE_DIR, "Code", "embeddings", "face_cosine_data.pkl")

try:
    with open(embeddings_file_path, "rb") as f:
        face_data_loaded = pickle.load(f)
    print("Successfully loaded face_cosine_data.pkl")
    print("Content of face_data_loaded:")
    
    if not face_data_loaded:
        print("The loaded face_data is empty!")
    else:
        for person_id, embeddings_list in face_data_loaded.items():
            print(f"  Locker ID: {person_id}, Number of embeddings: {len(embeddings_list)}")
            
            # Optional: Print the first few elements of the first embedding for inspection
            if embeddings_list:
                # print(f"    First embedding (first 5 elements): {embeddings_list[0][:5]}")
                pass # Comment out the above line if you don't want to print embedding values

            # Check if all embeddings are identical for a given person_id
            if len(embeddings_list) > 1:
                first_emb = embeddings_list[0]
                all_identical = True
                for i in range(1, len(embeddings_list)):
                    if not np.allclose(first_emb, embeddings_list[i], atol=1e-8): # Use atol for float precision
                        all_identical = False
                        break
                if all_identical:
                    print(f"    Warning: All embeddings for Locker ID {person_id} appear to be identical!")
                else:
                    print(f"    Embeddings for Locker ID {person_id} are diverse (not all identical).")

except FileNotFoundError:
    print(f"Error: The file '{embeddings_file_path}' was not found.")
except Exception as e:
    print(f"An unexpected error occurred while loading or inspecting the pickle file: {e}")