import time
import zmq
import argparse

__version__ = 1.0

def subscriber(broker, port):
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.setsockopt(zmq.SUBSCRIBE, '')
    subscriber.connect("tcp://%s:%s" % (broker, port))
    while True:
        work = subscriber.recv_json()
        fields = ['type', 'id', 'status', 'message']
        if all(field in fields for field in work):
            print 'Received Message: Type: %s Status:' \
            ' %s %s from %s' % (work['type'], work['status'], work['message'], work['id'])

def subscribe():
    description = 'Simple ZMQ Message Subscriber'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-b', '--broker', help='Message broker', required=True)
    parser.add_argument('-p', '--port', help='Port for message broker', required=True)
    args = parser.parse_args()
    subscriber(args.broker, args.port)

if __name__ == '__main__':
    subscribe()
