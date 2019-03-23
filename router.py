from importlib import import_module

def route_request(request, path = ''):
    if len(path)>0:
        path = path+'.'
    routes = import_module(f'{path}routes')
    for handle in routes.handles:
        if request['headers']['ROUTE'].startswith(handle[0]):
            return getattr(import_module(path+'handles'),handle[1])(request)

    for releative_route in routes.routes:
        if request['headers']['ROUTE'].startswith(releative_route[0]):
            request['headers']['ROUTE'] = request['headers']['ROUTE'][len(releative_route[0]):]
            return route_request(request,path+releative_route[1])