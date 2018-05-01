from redis import Redis
from rq import Connection, Queue, Worker

if __name__ == '__main__':
    with Connection(Redis('localhost', 6379)):
        q = Queue()
        Worker(q).work()
