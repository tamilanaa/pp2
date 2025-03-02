def copy(source_file, destination_file):
    with open(source_file, 'r') as source, open(destination_file, 'w') as destination:
        destination.writelines(source)

    print("File copied successfully.")

copy('A.txt', 'B.txt')
