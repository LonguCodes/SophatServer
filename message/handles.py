from auth.tokens import require_token
from protocol import response
from protocol.requires import require_body
from . import data 

@require_token
@require_body('CHAT_ID')
@require_body('LAST_UPDATE')
def update_chat(request):
    chat_id = request['body']['CHAT_ID']
    last_update = request['body']['LAST_UPDATE']

    if chat_id not in data.loaded_chats:
        data.load_chat(chat_id)
    chat = data.loaded_chats[chat_id]['messages']
    if len(chat) == 0 or chat[0]['timestamp'] > last_update:
        chat_data = data.load_messages(chat_id)    
        for message in chat_data:
            if last_update >= message['timestamp']:
                break
    chat = data.loaded_chats[chat_id]['messages']
    return response.update_chat(chat)


@require_token
@require_body('CONTENT')
@require_body('CHAT_ID')
@require_body('SENDER')
def message(request):
    chat_id = request['body']['CHAT_ID']
    sender = request['body']['SENDER']
    content = request['body']['CONTENT']

    message = data.add_new_message(chat_id,sender,content)

    return 
    