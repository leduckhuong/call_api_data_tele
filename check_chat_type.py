def check_chat_type(chat_id):
    if str(chat_id).startswith('-100'):
        return True
    return False