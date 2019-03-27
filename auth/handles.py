from auth import tokens
from protocol import response

def login(request):
    if 'LOGIN' not in request['body'] or 'PASSWORD' not in request['body']:
        return response.unknown_request()

    login  = request['body']['LOGIN']
    password = request['body']['PASSWORD']

    # TODO : make database lookup to check if user with credentials exist
    # If so send him a token

    # Dummy check as a sql lookup
    if False:
        return response.wrong_authentication()

    id = 0

    return response.login(id, tokens.generate(id))
    
@tokens.require_token
def renew_token(request):    
    return response.token(tokens.generate(id))


    