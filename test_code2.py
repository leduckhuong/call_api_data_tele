import configparser
from telethon import TelegramClient
from telethon.tl.types import PeerChannel

config = configparser.ConfigParser()
config.read('config.ini')

api_id = config['TELE_API']['APP_ID']
api_hash = config['TELE_API']['HASH_ID']

client = TelegramClient('session_name', api_id, api_hash)

id_messages = [4520503739]  

async def fetch_previous_messages(channel_id):
    count = 0
    try:
        print(type(channel_id))
        # Lấy entity của channel
        entity = await client.get_entity(channel_id)
        
        # Lấy tin nhắn từ entity đã xác định
        async for message in client.iter_messages(entity):
            if message.text:  # Chỉ lấy tin nhắn văn bản
                print(f"Message {count + 1}: {message.text}")
                print(f"Date: {message.date}\n")
            count += 1
        print(f"Total messages in channel ID {channel_id}: {count}")
    except Exception as e:
        print(f"Error fetching messages from {channel_id}: {e}")
    return count

async def main():
    await client.start()

    # Duyệt qua từng chat ID trong danh sách và lấy số lượng tin nhắn
    for chat_id in id_messages:
        await fetch_previous_messages(chat_id)

    # Ngắt kết nối sau khi hoàn thành
    await client.disconnect()

client.loop.run_until_complete(main())