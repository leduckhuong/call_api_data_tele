import os
import configparser
from telethon import TelegramClient, events


config = configparser.ConfigParser()
config.read('config.ini')

# Thông tin đăng nhập Telegram của bạn
api_id = config['TELE_API']['APP_ID']
api_hash = config['TELE_API']['HASH_ID']

# Tạo client Telegram
client = TelegramClient('session_name', api_id, api_hash)

os.makedirs('./storage', exist_ok=True)

@client.on(events.NewMessage)
async def handle_event(event):
    message = event.message
    print("OK")
    # Kiểm tra nếu tin nhắn thuộc về nhóm hoặc kênh và có chứa tài liệu
    if message.is_group or message.is_channel:
        if message.media and hasattr(message.media, 'document'):
            for attribute in message.media.document.attributes:
                if hasattr(attribute, 'file_name'):
                    file_name = attribute.file_name
                    print("Filename:", file_name)

                    try:
                        # Tải file về thư mục ./storage
                        download_path = f'./storage/{file_name}'
                        await client.download_media(message, file=download_path)
                        
                        print(f"File '{file_name}' downloaded to {download_path}")

                        

                    except Exception as error:
                        print("Error while downloading:", error)
                    break  # Thoát sau khi tải xong file đầu tiên

client.start()
client.run_until_disconnected()