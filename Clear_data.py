import os
import shutil

def clean_directory_contents_and_reset_available():
    """
    Cleans all contents (files and subdirectories) inside the dataset and embeddings directories,
    keeping the directories themselves. Then, it rewrites the available.txt file with the value 4.
    """
    # Paths to the directories whose contents need to be cleared
    dataset_dir = "/home/admin/Desktop/Smart Locker/dataset"
    embeddings_dir = "/home/admin/Desktop/Smart Locker/Code/embeddings"
    
    # Path to the available.txt file
    available_file = "/home/admin/Desktop/Smart Locker/available.txt"

    # --- Clear contents of the dataset directory ---
    if os.path.exists(dataset_dir) and os.path.isdir(dataset_dir):
        print(f"Clearing contents of directory: {dataset_dir}")
        for item in os.listdir(dataset_dir):
            item_path = os.path.join(dataset_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Delete file or symlink
                    print(f"  Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Delete subdirectory
                    print(f"  Deleted subdirectory: {item_path}")
            except OSError as e:
                print(f"Error deleting {item_path}: {e}")
    else:
        print(f"Directory does not exist or is not a directory: {dataset_dir}. Will create if necessary.")
        os.makedirs(dataset_dir, exist_ok=True) # Ensure directory exists

    # --- Clear contents of the embeddings directory ---
    if os.path.exists(embeddings_dir) and os.path.isdir(embeddings_dir):
        print(f"Clearing contents of directory: {embeddings_dir}")
        for item in os.listdir(embeddings_dir):
            item_path = os.path.join(embeddings_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Delete file or symlink
                    print(f"  Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Delete subdirectory
                    print(f"  Deleted subdirectory: {item_path}")
            except OSError as e:
                print(f"Error deleting {item_path}: {e}")
    else:
        print(f"Directory does not exist or is not a directory: {embeddings_dir}. Will create if necessary.")
        os.makedirs(embeddings_dir, exist_ok=True) # Ensure directory exists

    # --- Write content to available.txt file ---
    try:
        with open(available_file, "w") as f:
            f.write("4")
        print(f"Wrote '4' to file: {available_file}")
    except IOError as e:
        print(f"Error writing to file {available_file}: {e}")

# Call the function to execute
if __name__ == "__main__":
    clean_directory_contents_and_reset_available()