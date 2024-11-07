from telethon.errors import ChannelPrivateError, ChannelInvalidError
from telethon.tl.types import PeerChannel

from check_chat_type import check_chat_type

async def get_channel_entity(client, channel_id):
    
    try:
        if check_chat_type(channel_id):
            # Remove the -100 prefix if present
            if str(channel_id).startswith('-100'):
                channel_id = int(str(channel_id)[4:])
            print(f'Attempting to access channel with ID: {channel_id}')
            
            # Try getting the channel directly
            channel = await client.get_entity(PeerChannel(channel_id))
            
            return channel
        else:
            channel = await client.get_entity(int(channel_id))
            return channel
        
    except ValueError as e:
        print(f'ValueError: {str(e)}')
        raise
    except ChannelPrivateError:
        print('This is a private channel. Please make sure you have joined it.')
        raise
    except ChannelInvalidError:
        print('This channel is invalid or not accessible.')
        raise
    except Exception as e:
        print(f'Error accessing channel: {str(e)}')
        raise