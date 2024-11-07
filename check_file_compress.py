import os

extensions = ['.zip', '.rar', '.7z']


def check_compress_file(file):
    _, file_extension = os.path.splitext(file)
    return file_extension in extensions
