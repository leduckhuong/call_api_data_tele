import os

def check_file_exist(history_file, file_name):
    try:
        # Kiểm tra file có tồn tại không
        if not os.path.exists(history_file):
            return False

        # Mở và đọc file
        with open(history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Kiểm tra file_name có trong nội dung file không
            if file_name in content.splitlines():
                print(f"File {file_name} is already in history.")
                return True
    except Exception as e:
        print(f"Error checking file existence: {str(e)}")
    return False