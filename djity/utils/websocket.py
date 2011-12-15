import sys
import os
import gevent
from gevent import  Greenlet
from gevent.queue import Queue
from geventwebsocket.handler import WebSocketHandler
import random
import json
import logging 

from djity.utils.messaging import ConnectionManager

from dajaxice.core import dajaxice_autodiscover

dajaxice_autodiscover()


try:
        from importlib import import_module
except:
    try:
        from django.utils.importlib import import_module
    except:
        from dajaxice.utils import simple_import_module as import_module

log = logging.getLogger('djity')

def websocket_autodiscover():
    """
    Auto-discover INSTALLED_APPS websocket.py modules and fail silently when
    not present. NOTE: websocket_autodiscover was inspired/copied from
    django.contrib.admin autodiscover
    """
    global LOADING_WEBSOCKET
    if LOADING_WEBSOCKET:
        return
    LOADING_WEBSOCKET = True

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

LOADING_WEBSOCKET = False

class ServeletsManager(object):

    instance = None
    def __new__(theClass):
        if theClass.instance is None:
            theClass.instance = object.__new__(theClass)
            theClass.instance.servelets = []
            theClass.instance.autostart = []

        return theClass.instance

    
    def register(self,serveletClass, autostart=False):
        self.servelets.append(serveletClass)
        if autostart:
            self.autostart.append(serveletClass.channel_name)

    def __iter__(self):
        return self.servelets.__iter__()

    
class Multiplex():

    def __init__(self,environ):
        self.ws = environ['wsgi.websocket']
        self.servelets = dict([(ms_class.channel_name,ms_class(self,environ)) for ms_class in ServeletsManager()])
        print self.servelets
        self.started = dict()


    def start(self):
        log.debug('Starting websocket ...')
        for name in ServeletsManager().autostart:
            s = self.servelets[name]
            s.start()
            self.started[name] = s
        self.receiving()

    def receiving(self):
            while True:
                    message = self.ws.receive()
                    if message == None :
                        break
                    data = json.loads(message)
                    try:
                        self.started[data['type']].channel.put(data['data'])
                    except KeyError:
                        name = data['type']
                        s = self.servelets[name]
                        s.start()
                        self.started[name] = s
                        try:
                            self.started[data['type']].channel.put(data['data'])
                        except KeyError:
                            log.warn('client sent message to an unknown channel %s'%name)

            for s in self.started.values():
                s.shut_down()
            log.debug('Shutdown websocket ...')
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


class WebSocketOverDajax():

    def __init__(self,uuid):
        self.uuid = uuid

    def send(self,message):
        queue_name = str(self.uuid) + 'down'
        with ConnectionManager().get_publisher(queue_name) as pub:
            pub.publish(message)

    def receive(self):
        queue_name = str(self.uuid)+'up'
        log.debug('get message for %s'%queue_name)
        with ConnectionManager().get_consumer(queue_name,block=True,) as queue:
            for m in queue:
                return m

class WebSocketOverDajaxServer(Greenlet):

    def _run(self):
        print "starting Web Coket Over Dajax Server"
        with ConnectionManager().get_consumer('create',block=True) as queue:
            for m in queue:
                log.debug('create server uuid=%s'% m)
                #environ = {'wsgi.websocket':WebSocketOverDajax(m)}
                #Multiplex(environ, None).start()

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

