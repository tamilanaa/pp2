import os

def list_directories_files(path):
    path = os.path.abspath(path)  # Преобразуем путь в абсолютный
    entries = os.listdir(path)  # Получаем список файлов и папок в директории

    directories = [entry for entry in entries if os.path.isdir(os.path.join(path, entry))]
    files = [entry for entry in entries if os.path.isfile(os.path.join(path, entry))]

    print("Directories:")
    for directory in directories:
        print("   ", directory)

    print("\n Files:")
    for file in files:
        print("   ", file)

    print("\n All directories and files:")
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            print(os.path.join(root, dir))
        for file in files:
            print(os.path.join(root, file))


path = "/Users/tamilana/Desktop/PP2/pp22/lab6/dir n files"

list_directories_files(path)
