import os
import pyzipper
import rarfile
import py7zr


async def extract_zip(zip_file_path, extract_file_path, password=None):
    try:
        await os.makedirs(extract_file_path, exist_ok=True)
        with pyzipper.AESZipFile(zip_file_path, "r") as zip_ref:
            if password:
                await zip_ref.extractall(extract_file_path, pwd=password.encode("utf-8"))
            else:
                await zip_ref.extractall(extract_file_path)
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


async def extract_rar(rar_file_path, extract_file_path, password=None):
    try:
        await os.makedirs(extract_file_path, exist_ok=True)
        with rarfile.RarFile(rar_file_path, "r") as rar_ref:
            if password:
                await rar_ref.extractall(extract_file_path, pwd=password)
            else:
                await rar_ref.extractall(extract_file_path)
        print("Extract successful")
    except rarfile.BadRarFile as e:
        print("The RAR file is corrupted.")
    except rarfile.RarWrongPassword:
        print("The password is incorrect.")
    except Exception as e:
        print(f"Error: {str(e)}")


async def extract_7z(sevenz_file_path, extract_file_path, password=None):
    try:
        await os.makedirs(extract_file_path, exist_ok=True)
        with py7zr.SevenZipFile(
            await sevenz_file_path, mode="r", password=password
        ) as archive:
            await archive.extractall(path=extract_file_path)
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


async extract_file(file_path, extract_file_path):
    _, file_extension = os.path.splitext(file_path)
    file_name = os.path.basename(path)
    if (file_extension == '.zip'):
        await extract_zip(file_path, extract_file_path)
    if (file_extension == '.rar'):
        extract_file_path = './storage/'+file_name
        await extract_zip(file_path, extract_file_path)
    if (file_extension == '.7z'):
        extract_file_path = './storage/'+file_name
        await extract_zip(file_path, extract_file_path)

def main():
    zip_file_path = "/mnt/500GB/downloads/data/usa_22.rar"
    extract_file_path = "./"
    extract_rar(zip_file_path, extract_file_path)


if __name__ == "__main__":
    main()
