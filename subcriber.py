import time
import zmq
import argparse

__version__ = 1.0

def subscriber(server, port):
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://%s:%s")
    while True:
        data = subscriber.recv()
        time.sleep(1)

def subscribe():
    description = 'Simple ZMQ Message Subscriber'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-s', '--server', help='Message receiver', required=True)
    parser.add_argument('-p', '--port', help='Port for message receiver', required=True)
    args = parser.parse_args()
    subscriber(args.server, args.port)

if __name__ == '__main__':
    subscribe()
