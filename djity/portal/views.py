import urllib

from django.http import  HttpResponseRedirect


def redirect_root(request,path,*args,**kwargs):
    """
    Redirect the root project the root path with get parameters
    """
    if request.method == 'GET':
        params = urllib.urlencode(request.GET)
        return HttpResponseRedirect('../../' + path +"?%s"%params)
    return HttpResponseRedirect('../../' + path)


        

