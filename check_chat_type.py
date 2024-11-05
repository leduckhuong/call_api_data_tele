def check_chat_type(chat_id):
    if str(channel_id).startswith('-100'):
        return True
    elif str(channel_id).startswith('-'):
        return True
    return False