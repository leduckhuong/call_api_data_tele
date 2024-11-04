import os

extensions = [".txt"]
def check_file(file):
    _, file_extension = os.path.splitext(file)
    return file_extension in extensions