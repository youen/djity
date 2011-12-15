import logging

from django.core.management.base import BaseCommand
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from djity.utils.websocket import Multiplex,  DajaxMultiplexServelet, ChatMultiplexServelet

from tweet import TweetMultiplexServelet
multiplex_servelets = [TweetMultiplexServelet,ChatMultiplexServelet]
#multiplex_servelets = [DajaxMultiplexServelet]



def dispatch(environ, start_response):

    """Resolves the websocket depending on the path."""

    if environ['PATH_INFO'] == '/ws':
        
        return Multiplex(environ, start_response, multiplex_servelets).start()

class Command(BaseCommand):
    help = """Start a greenlet server for websocket."""

    def handle(slef,*args,**options):

        server = pywsgi.WSGIServer(('0.0.0.0', 8181), dispatch,
            handler_class=WebSocketHandler)
        server.serve_forever()

