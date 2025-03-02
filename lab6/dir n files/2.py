import os

path = "/Users/tamilana/Desktop/PP2/pp22/lab6/dir n files"

p = os.listdir(path)
print()

for item in p:
    full_path = os.path.join(path, item)
    print('Exists:', os.access(full_path, os.F_OK))
    print('Readable:', os.access(full_path, os.R_OK))
    print('Writable:', os.access(full_path, os.W_OK))
    print('Executable:', os.access(full_path, os.X_OK))
    print()