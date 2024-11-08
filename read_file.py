import os
import json
import asyncio

from check_file_format import check_file_format
from check_line_format import check_line_format
from check_file_valid import check_file_valid
from check_compress_file import check_compress_file
from save_data import save_data, client
from check_custom_mail import check_custom_mail
from extract_file import extract_file
from append_filename_history import append_filename_history

async def read_file(path):
    print(path)
    try:
        if os.path.isfile(path):
            if not check_compress_file(path):
                if check_file_valid(path):
                    _, file_extension = os.path.splitext(path)
                    file_name = os.path.basename(path)
                    if file_extension == ".txt":
                        file_format = check_file_format(path)
                        if file_format == 1:
                            with open(path, "r") as file_txt:
                                for line in file_txt:
                                    line = line.strip()
                                    format_type = check_line_format(line)
                                    if format_type == 1:
                                        pos1 = line.rfind(":")  
                                        pos2 = line.rfind(":", 0, pos1)  

                                        # Cắt chuỗi
                                        base_url = line[:pos2]
                                        mail = line[pos2 + 1: pos1]
                                        password = line[pos1 + 1:]
                                        await save_data("", file_name, base_url, mail, password, "", "")
                                        print("URL:", base_url)
                                        print("mail:", mail)
                                        print("Password:", password)
                                    elif format_type == 2:
                                        pos1 = line.rfind(":")  
                                        pos2 = line.rfind(" ", 0, pos1) 

                                        # Cắt chuỗi
                                        base_url = line[:pos2]
                                        mail = line[pos2 + 1: pos1]
                                        password = line[pos1 + 1:]
                                        await save_data("", file_name, base_url, mail, password, "", "")
                                        print("URL:", base_url)
                                        print("Mail:", mail)
                                        print("Password:", password)
                                    elif format_type == 3:
                                        pos1 = line.find(":")  
                                        pos2 = line.find("\t")  
                                        mail = line[:pos1]
                                        password = line[pos1+1:pos2]
                                        base_url = line[pos2:].strip()

                                        await save_data("", file_name, base_url, mail, password, "", "")
                                        print("URL:", base_url)
                                        print("Mail:", mail)
                                        print("Password:", password)

                                    elif format_type == 4:
                                        pos1 = line.rfind(" ")  
                                        pos2 = line.rfind(":", 0, pos1)  

                                        mail = line[:pos2]
                                        if check_custom_mail(mail):
                                            password = line[pos2 + 1: pos1]
                                            await save_data("", file_name, "", mail, password, "", "")
                                            print("Mail:", mail)
                                            print("Password:", password)
                                    elif format_type == 5:
                                        mail, password = line.split(":")
                                        if check_custom_mail(mail):
                                            await save_data("", file_name, "", mail, password, "", "")
                                            print("Mail:", mail)
                                            print("Password:", password)
                            append_filename_history('./history_read.txt', file_name)
                        elif file_format == 2:
                            with open(path) as file:
                                content = file.read()  
                                block = content.split("\n\n")  
                                for item in block:
                                    url, mail, password = "","",""
                                    lines_item = item.split("\n")
                                    for line_item in lines_item:
                                        pos1 = line_item.find(":")
                                        if "url" in line_item:
                                            url = line_item[pos1+1:]
                                        if "login" in line_item:
                                            mail = line_item[pos1+1:]
                                        if "password" in line_item:
                                            password = line_item[pos1+1:]
                                    print("Url: ", url)
                                    print("Mail: ", mail)
                                    print("Password: ", password)
                            append_filename_history('./history_read.txt', file_name)
                        elif file_format == 3:
                            with open(path) as file:
                                content = file.read()  
                                block = content.split("\n===============")
                                for item in block:
                                    url, mail, password = "", "", ""
                                    lines_item = item.split("\n")
                                    for line_item in lines_item:
                                        pos1 = line_item.find(":")
                                        if "URL" in line_item:
                                            url = line_item[pos1 + 1:].strip()
                                        if "Mail" in line_item:
                                            mail = line_item[pos1 + 1:].strip()
                                        if "Password" in line_item:
                                            password = line_item[pos1 + 1:].strip()
                                    print("Url: ", url)
                                    print("Mail: ", mail)
                                    print("Password: ", password)
                            append_filename_history('./history_read.txt', file_name)
            else:
                extract_file_path = './storage/'+file_name
                await extract_file(path, extract_file_path)
            # Xóa file sau khi đã đọc và xử lý
            # os.remove(path)
            # print(f"File {path} has been processed and deleted.")

        elif os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                await read_file(item_path)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    path = "./storage/test2.txt"
    await read_file(path)

if __name__ == "__main__":
    try:
        asyncio.run(main())  
    finally:
        client.close() 