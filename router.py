
def route(request, path = ''):
    if len(path)>0:
        path = path+'.'
    routes = __import__(path+'routes')
    print(path+'routes')
    for handle in routes.handles:
        if request['headers']['ROUTE'].startswith(handle[0]):
            print('using handle ', handle[0] ,' with path ',path)    
            getattr(__import__(path+'handles',fromlist=[handle[1]]),handle[1])(request)

    for releative_route in routes.routes:
        if request['headers']['ROUTE'].startswith(releative_route[0]):
            print('using route ', releative_route[0] ,' with path ',path)    
            request['headers']['ROUTE'] = request['headers']['ROUTE'][len(releative_route[0]):]
            route(request,path+releative_route[1])