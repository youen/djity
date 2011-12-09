from djity.utils.websocket import MultiplexServelet, ServeletsManager
from dajaxice.core import DajaxiceRequest
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import get_user

class DummyRequest:
    def __init__(self,environ):
        self.COOKIES = dict(map(lambda x:x.split("="),environ['HTTP_COOKIE'].split('; ')))

class RequestFactory:

    def __init__(self,environ):
        self.environ = environ
        self.smw = SessionMiddleware()
        dr = DummyRequest(self.environ)
        self.smw.process_request(dr)
        self.user = get_user(dr)
        self.session = dr.session

    def request(self,path,POST=None):
        return WebSocketRequest(self.environ, self.session,self.user,path,POST)
        

    def post_request_update(self,request,response):
        self.smw.process_response(request,response)

class WebSocketRequest:

    def __init__(self,environ,session,user,path,POST):
        self.META = environ
        self.session = session
        self.user = user
        self._path = path
        self.POST = POST
        self.method = 'POST'

    def get_full_path(self):
        return self._path


class DajaxMultiplexServelet(MultiplexServelet):
    
    channel_name = "dajax"

    def __init__(self,environ):
        super(DajaxMultiplexServelet,self).__init__(environ)
        self.req_fact = RequestFactory(environ)
        
    def run(self):
        while True:
            message = self.channel.get()
            req = self.req_fact.request('/dajaxice',{'argv':json.dumps(message['params'])})
            resp = DajaxiceRequest(req,message['func']).process()
            self.req_fact.post_request_update(req,resp)
            self.send(resp.content,force_json=False)

ServeletsManager().register(DajaxMultiplexServelet)
