import os

def delete_file(path):
    if os.path.exists(path) and os.access(path, os.W_OK):
        os.remove(path)
        print(f"Deleted file: {path}")
    else:
        print("the File doesn't exist or access is denied")


delete_file("nadodel.txt")
