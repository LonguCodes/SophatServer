import tokens

def auth(request):
    # TODO : make database lookup to check if user with credentials exist
    # If so send him a token

    return {
        'headers':{
            'RESPONSE':'1'
        },
        'body':{
            'TOKEN': tokens.generate()
        }
    }
    