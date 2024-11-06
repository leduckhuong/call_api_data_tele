import configparser
import json
import asyncio
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, ChannelPrivateError, ChannelInvalidError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel, InputPeerChannel, Channel, PeerUser, PeerChat

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, bytes):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def check_chat_type(chat_id):
    """
    Helper function to determine the chat type from the chat ID.
    Returns True if the chat is a channel, False otherwise.
    """
    if str(chat_id).startswith('-100'):
        return True
    return False

async def get_channel_entity(client, channel_id):
    """Helper function to get channel entity with proper error handling"""
    try:
        if check_chat_type(channel_id):
            # Remove the -100 prefix if present
            if str(channel_id).startswith('-100'):
                channel_id = int(str(channel_id)[4:])
            print(f"Attempting to access channel with ID: {channel_id}")
            
            # Try getting the channel directly
            channel = await client.get_entity(PeerChannel(channel_id))
            
            return channel
        else:
            channel = await client.get_entity(int(channel_id))
            return channel
        
    except ValueError as e:
        print(f"ValueError: {str(e)}")
        raise
    except ChannelPrivateError:
        print("This is a private channel. Please make sure you have joined it.")
        raise
    except ChannelInvalidError:
        print("This channel is invalid or not accessible.")
        raise
    except Exception as e:
        print(f"Error accessing channel: {str(e)}")
        raise

async def main(phone):
    try:
        await client.start()
        print("Client Created")
        
        # Ensure authorization
        if not await client.is_user_authorized():
            await client.send_code_request(phone)
            try:
                await client.sign_in(phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await client.sign_in(password=input('Password: '))

        me = await client.get_me()
        print(f"Logged in as: {me.username if me.username else me.first_name}")
        
        user_input_channel = input('enter entity(telegram URL or entity id):')
        
        # Get the channel entity
        my_channel = await get_channel_entity(client, user_input_channel)
        print(f"Successfully connected to channel: {getattr(my_channel, 'title', 'Unknown')}")
        
        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
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
                msg_dict['channel_id'] = my_channel.id
                msg_dict['channel_title'] = getattr(my_channel, 'title', 'Unknown')
                all_messages.append(msg_dict)
            
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        print(f"Total messages retrieved: {total_messages}")
        
        if all_messages:
            output_file = f'channel_messages_{my_channel.id}.json'
            with open(output_file, 'w', encoding='utf-8') as outfile:
                json.dump(all_messages, outfile, cls=DateTimeEncoder, ensure_ascii=False, indent=2)
            
            print(f"Messages saved to {output_file}")
        else:
            print("No messages were retrieved")

    except ChannelPrivateError:
        print("ERROR: This is a private channel. Please:")
        print("1. Join the channel first")
        print("2. Make sure you're using the correct channel ID")
        print("3. Check if you've been banned or removed from the channel")
    except ChannelInvalidError:
        print("ERROR: Invalid channel. Please:")
        print("1. Verify the channel ID is correct")
        print("2. Make sure the channel still exists")
        print("3. Try getting the channel ID from the channel's URL")
    except ValueError as e:
        print(f"ERROR: Invalid channel ID format: {str(e)}")
        print("Tips:")
        print("1. Try using the channel username if it's public")
        print("2. Make sure you're copying the full channel ID")
        print("3. If using a channel URL, make sure to use only the numeric ID part")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        await client.disconnect()

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

api_id = int(config['TELE_API']['APP_ID'])
api_hash = str(config['TELE_API']['HASH_ID'])
phone = config['TELE_API']['PHONE']
username = config['TELE_API']['USERNAME']

client = TelegramClient(username, api_id, api_hash)

with client:
    client.loop.run_until_complete(main(phone))