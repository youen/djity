import cPickle
import gevent.monkey

gevent.monkey.patch_all(time=False)

import redis


class ConnectionManager(object):

    instance = None
    def __new__(theClass):
        if theClass.instance is None:
            theClass.instance = object.__new__(theClass)
            theClass.instance._init()

        return theClass.instance

    def _init(self):
        self.client = redis.Redis()

    def get_consumer(self,queue_name,block=False,block_first=False):

        queue_name = str(queue_name)
        if block_first:
            return FirstBlockedQueue(redis.Redis(),queue_name)
        elif block:
            return BlockedQueue(redis.Redis(),queue_name)
        else:
            return Queue(redis.Redis(),queue_name)


    def get_publisher(self,queue_name):
        queue_name = str(queue_name)
        return Publisher(self.client,queue_name)

class Queue():

    def __init__(self,client,name):
        self.client = client
        self.name = name
    
    def __enter__(self):
        return self

    def __iter__(self):
        while True:
            m = self.client.rpop(self.name)
            if m is None:
                break
            yield cPickle.loads(m)

    def __exit__(self,error,val,tb):
        if error:
            raise

class Publisher(Queue):

    def __iter__(self):
        pass

    def publish(self,message):
        self.client.rpush(self.name,cPickle.dumps(message,-1))



class FirstBlockedQueue(Queue):

    def __iter__(self):
        q,m = self.client.blpop(self.name)
        yield cPickle.loads(m)
        while True:
            m = self.client.rpop(self.name)
            if m is None:
                break
            yield cPickle.loads(m)



class BlockedQueue(Queue):

    def __iter__(self):
        while True:
            q,m = self.client.blpop(self.name)
            yield cPickle.loads(m)



