def unknown_request():
    return {
        'headers': {
            'TYPE': 1
        },
        'body':{

        }
    }

def token(token):
    return {
        'headers':{
            'TYPE': 0
        },
        'body':{
            'TOKEN':token
        }
    }

def login(id,token):
    return {
        'headers':{
            'TYPE': 0
        },
        'body':{
            'TOKEN':token,
            'ID':id
        }
    }

def wrong_authentication():
    return {
        'headers':{
            'TYPE' : 2
        },
        'body':{

        }
    }