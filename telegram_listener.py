import os
import configparser
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaDocument

from download_message_media import download_message_media
from read_file import read_file
from check_file_downloaded import check_file_downloaded
from append_filename_history import append_filename_history


config = configparser.ConfigParser()
config.read('config.ini')

# Thông tin đăng nhập Telegram của bạn
api_id = config['TELE_API']['APP_ID']
api_hash = config['TELE_API']['HASH_ID']
username = config['TELE_API']['USERNAME']

# Tạo client Telegram
client = TelegramClient(username, api_id, api_hash)

os.makedirs('./storage', exist_ok=True)

@client.on(events.NewMessage)
async def handle_event(event):
    try:
        message = event.message
        print("OK")
        
        # Kiểm tra nếu tin nhắn thuộc về nhóm hoặc kênh và có chứa tài liệu
        if message.is_group or message.is_channel and message.media:
            print(message)
            
            # Kiểm tra nếu có tài liệu trong media
            if isinstance(message.media, MessageMediaDocument):
                # Kiểm tra và lấy tên file
                file_name = None
                for attribute in message.media.document.attributes:
                    if hasattr(attribute, 'file_name'):
                        file_name = attribute.file_name
                        break
                
                if not file_name:
                    file_name = f'document_{message.id}'
                
                history_downloaded = './history_downloaded.txt'
                history_read = './history_read.txt'
                download_dir = './storage'

                if not check_file_downloaded(history_downloaded, file_name):
                    # Tải file về
                    msg_dict = message.to_dict()
                    if hasattr(message.peer_id, 'chat_id'):
                        msg_dict['chat_id'] = message.peer_id.chat_id
                    elif hasattr(message.peer_id, 'channel_id'):
                        msg_dict['channel_id'] = message.peer_id.channel_id

                    file_path = await download_message_media(client, msg_dict, download_dir)
                    
                    if file_path:
                        await read_file(download_dir + file_path)
                        # Đánh dấu đã đọc
                        append_filename_history(history_read, file_name)
                        print(f"Successfully downloaded: {file_path}")
                    else:
                        print("Download failed")
                else:
                    print(f"File {file_name} already downloaded")
                    
    except Exception as e:
        print(f'Error in event handler: {str(e)}')
        import traceback
        print("Full error:", traceback.format_exc()) 


client.start()
client.run_until_disconnected()