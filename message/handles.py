from auth.tokens import require_token
from protocol import response

@require_token
def update_client(request):
    if 'CHAT_ID' not in request['body'] or 'LAST_UPDATE' not in request['body']:
        return response.unknown_request()
    
    chat_id = request['body']['CHAT_ID']
    last_update = request['body']['LAST_UPDATE']

    