
from djity.utils.messaging import ConnectionManager 


def create_server(uuid,context):
    queue_name = 'create'
    with ConnectionManager().get_publisher(queue_name) as pub:
        pub.publish(uuid)
                             
def create_server_process():
    with ConnectionManager().get_consumer('create',block=True) as queue:
        for m in queue:
            print m

        
def send_to_servelet(uuid,message):
    queue_name = str(uuid)+'up'
    with ConnectionManager().get_publisher(queue_name) as pub:
        pub.publish(message)
                             
                             
def recv_from_servelet(uuid,wait=False):
    queue_name = str(uuid)+'down'
    with ConnectionManager().get_consumer(queue_name,block_first=True) as queue:
        for m in queue:
            yield m

def send_to_brother(uuid,message):
    queue_name = str(uuid)+'down'
    with ConnectionManager().get_publisher(queue_name) as pub:
        pub.publish(message)

def recv_from_brother(uuid):
    queue_name = str(uuid)+'up'
    with ConnectionManager().get_consumer(queue_name,block=True) as queue:
        for m in queue:
            yield m


