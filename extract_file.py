import os
import pyzipper
import rarfile
import py7zr


def extract_zip(zip_file_path, extract_file_path, password=None):
    try:
        os.makedirs(extract_file_path, exist_ok=True)
        with pyzipper.AESZipFile(zip_file_path, "r") as zip_ref:
            if password:
                zip_ref.extractall(extract_file_path, pwd=password.encode("utf-8"))
            else:
                zip_ref.extractall(extract_file_path)
        print("Extract successful")
    except RuntimeError as e:
        if "password required" in str(e).lower():
            print("This zip file requires a password.")
        elif "bad password" in str(e).lower():
            print("The password is incorrect.")
        else:
            print(f"RuntimeError: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


def extract_rar(rar_file_path, extract_file_path, password=None):
    try:
        os.makedirs(extract_file_path, exist_ok=True)
        with rarfile.RarFile(rar_file_path, "r") as rar_ref:
            if password:
                rar_ref.extractall(extract_file_path, pwd=password)
            else:
                rar_ref.extractall(extract_file_path)
        print("Extract successful")
    except rarfile.BadRarFile as e:
        print("The RAR file is corrupted.")
    except rarfile.RarWrongPassword:
        print("The password is incorrect.")
    except Exception as e:
        print(f"Error: {str(e)}")


def extract_7z(sevenz_file_path, extract_file_path, password=None):
    try:
        os.makedirs(extract_file_path, exist_ok=True)
        with py7zr.SevenZipFile(
            sevenz_file_path, mode="r", password=password
        ) as archive:
            archive.extractall(path=extract_file_path)
        print("Extract successful")
    except py7zr.Bad7zFile:
        print("The 7z file is corrupted.")
    except RuntimeError as e:
        if "incorrect password" in str(e).lower():
            print("The password is incorrect.")
        else:
            print(f"RuntimeError: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    zip_file_path = "/mnt/500GB/downloads/data/usa_22.rar"
    extract_file_path = "./"
    extract_rar(zip_file_path, extract_file_path)


if __name__ == "__main__":
    main()
