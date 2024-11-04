import os
import json
import asyncio
from check_file_format import check_file_format
from check_line_format import check_line_format
from check_extension import check_extension
from save_data import save_data
from check_custom_mail import check_custom_mail

async def read_file(path):
    try:
        if os.path.isfile(path):
            if check_file(path):
                _, file_extension = os.path.splitext(path)
                if file_extension == ".txt":
                    file_format = check_file_format(path)
                    if file_format == 1:
                        with open(path, "r") as file_txt:
                            for line in file_txt:
                                line = line.strip()
                                format_type = check_line_format(line)
                                if format_type == 1:
                                    pos1 = line.rfind(":")  # tìm dấu : cuối cùng
                                    pos2 = line.rfind(":", 0, pos1)  # tìm dấu : thứ 2 từ cuối

                                    # Cắt chuỗi
                                    base_url = line[:pos2]
                                    username = line[pos2 + 1: pos1]
                                    password = line[pos1 + 1:]
                                    await save_data("", "", base_url, username, password, "", "")
                                    print("URL:", base_url)
                                    print("Username:", username)
                                    print("Password:", password)
                                elif format_type == 2:
                                    pos1 = line.rfind(":")  # tìm dấu : cuối cùng
                                    pos2 = line.rfind(" ", 0, pos1)  # tìm khoảng trắng

                                    # Cắt chuỗi
                                    base_url = line[:pos2]
                                    username = line[pos2 + 1: pos1]
                                    password = line[pos1 + 1:]
                                    await save_data("", "", base_url, username, password, "", "")
                                    print("URL:", base_url)
                                    print("Username:", username)
                                    print("Password:", password)
                                elif format_type == 3:
                                    pos1 = line.find(":")  # tìm dấu : 
                                    pos2 = line.find("\t")  # tìm tab
                                    username = line[:pos1]
                                    password = line[pos1+1:pos2]
                                    base_url = line[pos2:].strip()

                                    await save_data("", "", base_url, username, password, "", "")
                                    print("URL:", base_url)
                                    print("Username:", username)
                                    print("Password:", password)

                                elif format_type == 4:
                                    pos1 = line.rfind(" ")  # tìm khoảng trắng  cuối cùng
                                    pos2 = line.rfind(":", 0, pos1)  # tìm dấu ":"

                                    username = line[:pos2]
                                    if check_custom_mail(username):
                                        password = line[pos2 + 1: pos1]
                                        await save_data("", "", "", username, password, "", "")
                                        print("Username:", username)
                                        print("Password:", password)
                                elif format_type == 5:
                                    # Chuyển chuỗi JSON thành dictionary
                                    parsed_data = json.loads(line)

                                    # Lấy giá trị của các khóa "name", "phone", "email"
                                    email = parsed_data.get("email")
                                    if check_custom_mail(username):
                                        name = parsed_data.get("name")
                                        phone = parsed_data.get("phone")
                                        await save_data("", "", "", username, password, name, phone)
                                        print("Name:", name)
                                        print("Phone:", phone)
                                        print("Email:", email)
                                elif format_type == 6:
                                    username, password = line.split(":")
                                    if check_custom_mail(mail):
                                        await save_data("", "", "", username, password, "", "")
                                        print("Username:", username)
                                        print("Password:", password)
                    elif file_format == 2:
                        with open(path) as file:
                            content = file.read()  
                            block = content.split("\n\n")  
                            for item in block:
                                url, user, password = "","",""
                                lines_item = item.split("\n")
                                for line_item in lines_item:
                                    pos1 = line_item.find(":")
                                    if "url" in line_item:
                                        url = line_item[pos1+1:]
                                    if "login" in line_item:
                                        user = line_item[pos1+1:]
                                    if "password" in line_item:
                                        password = line_item[pos1+1:]
                                print("Url: ", url)
                                print("User: ", user)
                                print("Password: ", password)
                    elif file_format == 3:
                        with open(path) as file:
                            content = file.read()  
                            block = content.split("\n===============")
                            for item in block:
                                url, user, password = "", "", ""
                                lines_item = item.split("\n")
                                for line_item in lines_item:
                                    pos1 = line_item.find(":")
                                    if "URL" in line_item:
                                        url = line_item[pos1 + 1:].strip()
                                    if "Username" in line_item:
                                        user = line_item[pos1 + 1:].strip()
                                    if "Password" in line_item:
                                        password = line_item[pos1 + 1:].strip()
                                print("Url: ", url)
                                print("User: ", user)
                                print("Password: ", password)
            # Xóa file sau khi đã đọc và xử lý
            os.remove(path)
            print(f"File {path} has been processed and deleted.")

        elif os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                await read_file(item_path)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    path = "./storage/test4.txt"
    await read_file(path)

if __name__ == "__main__":
    try:
        asyncio.run(main())  
    finally:
        client.close() 