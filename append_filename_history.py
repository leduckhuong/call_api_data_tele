import os

def append_filename_history(history_file, file_name):
    try:
        # Kiểm tra nếu file chưa tồn tại, tạo file rỗng
        if not os.path.exists(history_file):
            with open(history_file, 'w', encoding='utf-8') as f:
                pass  # Tạo file rỗng nếu chưa tồn tại

        # Nếu file_name chưa có, ghi thêm vào cuối file
        with open(history_file, 'a', encoding='utf-8') as f:
            f.write(f"{file_name}\n")
            print(f"Marked {file_name} as downloaded.")

    except Exception as e:
        print(f"Error marking file download: {str(e)}")