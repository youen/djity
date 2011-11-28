import sys
import os
import gevent

from gevent import monkey
monkey.patch_all(thread=False)

from gevent import pywsgi , fork, sleep, Greenlet
from gevent.queue import Queue
from geventwebsocket.handler import WebSocketHandler
import random
import json




from tweepy.streaming import StreamListener, Stream
from tweepy.auth import BasicAuthHandler

from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()

from dajaxice.core import DajaxiceRequest
from django.test.client import Client
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

class Multiplex():

    def __init__(self,environ,start_response,servelets):
        self.ws = environ['wsgi.websocket']
        self.servelets = dict([(ms_class.channel_name,ms_class(environ)) for ms_class in servelets])

    def start(self):
        for s in self.servelets.values():
            s.start()
        self.receiving()

    def receiving(self):
            while True:
                    message = self.ws.receive()
                    if message == None :
                        break
                    data = json.loads(message)
                    self.servelets[data['type']].channel.put(data['data'])
            
            for s in self.servelets.values():
                s.shut_down()
    def close(self):
        pass

class MultiplexServelet(Greenlet):
    channel_name = "notify"
    def __init__(self,environ):
        Greenlet.__init__(self)
        self.channel = Queue() 
        self.environ = environ
        self.ws = environ['wsgi.websocket']

    def _run(self):
        pass
    

    def send(self,message,channel=None,force_json=True):
        if not channel:
            channel = self.channel_name
        if  force_json:
            message = json.dumps(message)
        self.ws.send('{"type":"%s","data": %s}'%(channel,message))

    def shut_down(self):
        self.kill()
 
class ChatMultiplexServelet(MultiplexServelet):
    channel_name = "chat"
    participants = set()
    
    def run(self):
        self.__class__.participants.add(self)
        try:
            for message in self.channel :
                for client in self.__class__.participants:
                    try:
                        client.send(message,channel='notify')
                    except :
                        print "can't send %s"%message
                        print "remove %s"%client
                        self.__class__.participants.remove(client)
                        
        except:
            print "error in chatmultiplex"
        finally:
            print "remove %s"%self
            self.__class__.participants.discard(self)

    def shut_down(self):
        self.__class__.participants.discard(self)
        self.kill()

class TicMultiplexServelet(MultiplexServelet):
    
    def run(self):
        while True :
            print "tac" 
            sleep(2)
            self.send("tic")

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


def multiplex(environ, start_response):
    """
    A multiplex websocket
    """

    req_fact = RequestFactory(environ)

    ws = environ['wsgi.websocket']
    pid = fork()
    try:
        while True:

            if pid == 0 :
                print "tac" 
                sleep(2)
                ws.send('{"type":"notify", "data" : "tic"}')
                continue
       
            m = ws.receive()
            message = json.loads(m)
            META = {'REMOTE_ADDR':'127.0.0.1'}
            req = req_fact.request('/dajaxice',{'argv':json.dumps(message['data']['params'])})
            resp = DajaxiceRequest(req,message['data']['func']).process()
            req_fact.post_request_update(req,resp)
            ws.send('{"type":"dajax", "data" : %s}'%resp.content)
    finally:
        pass



