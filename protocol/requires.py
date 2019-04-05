from protocol import response

def require_body(data_name):
    def require_wrapper(function):
        def wrapper(request, *args, **kwargs):
            if data_name not in request['body']:
                return response.unknown_request()
            return function(request, *args, **kwargs)
        return wrapper
    return require_wrapper