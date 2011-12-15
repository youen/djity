import logging

from django.core.management.base import BaseCommand
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

from djity.utils.websocket import websocket_autodiscover, Multiplex, WebSocketOverDajax
from djity.utils.messaging import ConnectionManager

log = logging.getLogger('djity')

websocket_autodiscover()


class Command(BaseCommand):
    help = """Start a greenlet server for websocket."""

    def handle(slef,*args,**options):
        with ConnectionManager().get_consumer('create',block=True) as queue:
            for m in queue:
                log.debug('create server uuid=%s'% m)
                environ = {'wsgi.websocket':WebSocketOverDajax(m)}
                Multiplex(environ).start()



