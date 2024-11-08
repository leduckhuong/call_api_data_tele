import os
import configparser
import json
import asyncio
from datetime import datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ChannelPrivateError, ChannelInvalidError
from telethon.tl.functions.messages import GetHistoryRequest

from get_channel_entity import get_channel_entity
from check_file_downloaded import check_file_downloaded
from download_message_media import download_message_media

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

async def main(phone):
    try:
        await client.start()
        print('Client Created')
        
        # Ensure authorization
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()
        print(f'Logged in as: {me.username if me.username else me.first_name}')
        
        user_input_channel = input('enter entity(telegram URL or entity id):')
        
        # Get the channel entity
        my_channel = await get_channel_entity(client, user_input_channel)
        print(f'Successfully connected to channel: {getattr(my_channel, 'title', 'Unknown')}')
        
        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            history = await client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            
            if not history.messages:
                break
            
            messages = history.messages
            for message in messages:
                # Convert message to dict and add additional metadata
                msg_dict = message.to_dict()
                if hasattr(message.peer_id, 'chat_id'):
                    msg_dict['chat_id'] = message.peer_id.chat_id
                elif hasattr(message.peer_id, 'channel_id'):
                    msg_dict['channel_id'] = message.peer_id.channel_id
                msg_dict['channel_title'] = getattr(my_channel, 'title', 'Unknown')
                all_messages.append(msg_dict)
            
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        print(f'Total messages retrieved: {total_messages}')
        
        if all_messages:
            
            for index, message in enumerate(all_messages):
                if message.get('media') and message['media'].get('document') is not None:
                    # Kiểm tra và lấy tên file
                    try:
                        attributes = message['media']['document'].get('attributes', [])
                        if attributes:
                            file_name = attributes[0].get('file_name', f'document_{index}')
                        else:
                            file_name = f'document_{index}'  # Đặt tên mặc định nếu không có `file_name`
                        
                        history_file = './history_downloaded.txt'
                        download_dir = './storage'
                        
                        if not check_file_downloaded(history_file, file_name):

                            file_path = await download_message_media(client, message, download_dir)
            
                            if file_path:
                                print(f'Successfully downloaded file: {file_path}')
                            else:
                                print(f'Failed to download file from message {index}')

                    except Exception as e:
                        print(f'Error downloading {e}')
        else:
            print('No messages were retrieved')

    except ChannelPrivateError:
        print('ERROR: This is a private channel. Please:')
        print('1. Join the channel first')
        print('2. Make sure you are using the correct channel ID')
        print('3. Check if you have been banned or removed from the channel')
    except ChannelInvalidError:
        print('ERROR: Invalid channel. Please:')
        print('1. Verify the channel ID is correct')
        print('2. Make sure the channel still exists')
        print('3. Try getting the channel ID from the channels"s URL')
    except ValueError as e:
        print(f'ERROR: Invalid channel ID format: {str(e)}')
        print('Tips:')
        print('1. Try using the channel username if it is public')
        print('2. Make sure you are copying the full channel ID')
        print('3. If using a channel URL, make sure to use only the numeric ID part')
    except Exception as e:
        print(f'Unexpected error: {str(e)}')
    finally:
        await client.disconnect() 

# Reading Configs
config = configparser.ConfigParser()
config.read('config.ini')

api_id = int(config['TELE_API']['APP_ID'])
api_hash = str(config['TELE_API']['HASH_ID'])
phone = config['TELE_API']['PHONE']
username = config['TELE_API']['USERNAME']

client = TelegramClient(username, api_id, api_hash)

with client:
    client.loop.run_until_complete(main(phone))