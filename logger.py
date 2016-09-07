import zmq
import argparse

__version__ = 1.0

def logger(server, port, id, message):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    uri = 'tcp://%s:%s' % (server, port)
    zmq_socket.connect(uri)
    message = { 'id': id, 'message': message }
    zmq_socket.send_json(message)

def log():
    description = 'Simple ZMQ Socket Logger'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-m', '--message', help='Message to send', required=True)
    parser.add_argument('-i', '--id', help='Unique ID', required=True)
    parser.add_argument('-s', '--server', help='Message receiver', required=True)
    parser.add_argument('-p', '--port', help='Port for message receiver', required=True)
    args = parser.parse_args()
    logger(args.server, args.port, args.id, args.message)

if __name__ == '__main__':
    log()

