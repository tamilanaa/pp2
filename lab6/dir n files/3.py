import os

def analyze_path(given_path):
    if os.path.exists(given_path):
        print("The path exists.")
        filename = os.path.basename(given_path)
        directory = os.path.dirname(given_path)
        print("Filename:", filename)
        print("Directory:", directory)
    else:
        print("The path does not exist.")

given_path = "/Users/tamilana/Desktop/PP2/pp22/lab6/dir n files"

analyze_path(given_path)