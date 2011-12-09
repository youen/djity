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


from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()


try:
        from importlib import import_module
except:
    try:
        from django.utils.importlib import import_module
    except:
        from dajaxice.utils import simple_import_module as import_module

def websocket_autodiscover():
    """
    Auto-discover INSTALLED_APPS websocket.py modules and fail silently when
    not present. NOTE: websocket_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_DAJAXICE
    if LOADING_DAJAXICE:
        return
    LOADING_DAJAXICE = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:

        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('websocket', app_path)
        except ImportError:
            continue

        import_module("%s.websocket" % app)

LOADING_DAJAXICE = False

class ServeletsManager(object):

    instance = None
    def __new__(theClass):
        if theClass.instance is None:
            theClass.instance = object.__new__(theClass)
            theClass.instance.servelets = []

        return theClass.instance

    
    def register(self,serveletClass):
        self.servelets.append(serveletClass)

    def __iter__(self):
        return self.servelets.__iter__()

    
class Multiplex():

    def __init__(self,environ,start_response):
        self.ws = environ['wsgi.websocket']
        self.servelets = dict([(ms_class.channel_name,ms_class(self,environ)) for ms_class in ServeletsManager()])
        print self.servelets


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
                    try:
                        self.servelets[data['type']].channel.put(data['data'])
                    except KeyError:
                        pass

            for s in self.servelets.values():
                s.shut_down()
    def close(self):
        pass

class MultiplexServelet(Greenlet):
    channel_name = "notify"
    def __init__(self,server,environ):
        Greenlet.__init__(self)
        self.server = server
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

