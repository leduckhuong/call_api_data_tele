import os
from append_filename_history import append_filename_history
from progress_callback import progress_callback

async def download_message_media(client, message, download_dir='./storage'):
    try:
        # Create storage directory
        os.makedirs(download_dir, exist_ok=True)
        
        # Get the original message object from Telethon, not the dict version
        # original_message = await client.get_messages(message['channel_id'], ids=message['id'])
        # original_message = await client.get_messages(message.chat_id, ids=message.id)
        print(message)
        original_message = None
        if 'channel_id' in message:  # Nếu có key 'channel_id'
            print('Message has channel id')
            original_message = await client.get_messages(message['channel_id'], ids=message['id'])
        elif 'chat_id' in message:  # Nếu có key 'chat_id'
            print('Message has chat id')
            original_message = await client.get_messages(message['chat_id'], ids=message['id'])
        else:
            print("Message does not contain channel_id or chat_id.")
            
        if not original_message or not original_message.media:
            print("No media found in original message")
            return None
        
        # Get file name
        file_name = None
        if hasattr(original_message.media, 'document') and original_message.media.document:
            for attribute in original_message.media.document.attributes:
                if hasattr(attribute, 'file_name'):
                    file_name = attribute.file_name
                    break
        
        if not file_name:
            file_name = f"document_{message['id']}"
            
        download_path = os.path.join(download_dir, file_name)
        print(f"Attempting to download: {file_name}")
        
        
        # Download using original message object
        file_path = await client.download_media(
            original_message.media,
            file=download_path,
            progress_callback=progress_callback
        )
        
        if file_path:
            print(f'Successfully downloaded to: {file_path}')
            append_filename_history('./history_downloaded.txt', file_name)
            return file_path
        else:
            print(f'Download failed for: {file_name}')
            return None
            
    except Exception as e:
        print(f'Error during download: {str(e)}')
        import traceback
        print("Full error:", traceback.format_exc())
        return None