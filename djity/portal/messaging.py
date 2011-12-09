from kombu import BrokerConnection, Exchange , Queue
from kombu.common import maybe_declare
from kombu.pools import producers, connections
from kombu.compat import Consumer
from kombu.simple import Empty

ws_exchange_up = Exchange("websocketOverDajaxUp",type='direct') # brother to servelets
ws_exchange_down = Exchange("websocketOverDajaxDown", type='direct') # servelets to brother

create_queue = Queue("create", exchange=ws_exchange_up, key="create")

from kombu.mixins import ConsumerMixin



class Worker(ConsumerMixin):
    
    def __init__(self, connection):
        self.connection = connection
        
    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[create_queue],
                         callbacks=[self.process_server])]
        
    def process_server(self, body, message):
        print body,message
        message.ack()

def create_server(uuid,context):
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with producers[connection].acquire(block=True) as producer:
            maybe_declare(ws_exchange_up, producer.channel)
            producer.publish((uuid,context),
                             serializer="pickle",
                             routing_key='create')
                             
def create_server_process():
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with connections[connection].acquire(block=True) as conn:
            Worker(conn).run()
        
def send_to_servelet(uuid,channel,message):
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with producers[connection].acquire(block=True) as producer:
            maybe_declare(ws_exchange_up, producer.channel)
            producer.publish((channel,message),
                             serializer="pickle",
                             routing_key=uuid + 'up')
                             
def recv_from_servelet(uuid,wait=False):
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with connections[connection].acquire(block=True) as conn:
        q = conn.SimpleQueue(uuid + 'down')
        if wait:
            m = q.get()
            yield m.payload
            m.ack()

        try:
            while True:
                m = q.get_nowait()
                yield m.payload
                m.ack()
        except Empty:
            pass


def send_to_brother(uuid,channel,message):
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with producers[connection].acquire(block=True) as producer:
            maybe_declare(ws_exchange_down, producer.channel)
            producer.publish({'type':channel,'data':message},
                             serializer="pickle",
                             routing_key=uuid + 'down')

def recv_from_brother(uuid):
    connection = BrokerConnection("amqp://guest:guest@djity:5672//") 
    with connections[connection].acquire(block=True) as conn:
        q = conn.SimpleQueue(uuid + 'up')
        while True:
            m = q.get()
            yield m.payload
            m.ack()

