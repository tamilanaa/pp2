import os

def list_directories_files(path):
    print("Directories:")
    
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path): 
            print("   ", entry)  

    print("\nFiles:")
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            print("   ", entry)

    print("\nAll directories and files:")
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print("   ",os.path.join(root, dir))
        for file in files:
            print("   ",os.path.join(root, file))

path = "/Users/tamilana/Desktop/PP2/pp22/lab6"

list_directories_files(path)
