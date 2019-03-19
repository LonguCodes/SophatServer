
def route(request, path = ''):
    routes = __import__(path+'.routes')
    for handle in routes.handles:
        if(request['headers']['ROUTE'].startswith(handle[0])):
            getattr(__import__(path+'.handles'),handle[1])(request)
    
    for route in routes.routes:
        if(request['headers']['ROUTE'].startwith(route[0])):
            request['headers']['ROUTE'][len(route[0]):]
            route(request,path+'.'+route[1])