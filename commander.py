import zmq
import argparse

__version__ = 1.0

def logger(broker, port, command, id, src, platform):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    uri = 'tcp://%s:%s' % (broker, port)
    zmq_socket.connect(uri)
    message = { 'command': command, 'build': id, 'src': src, 'platform': platform }
    zmq_socket.send_json(message)

def log():
    description = 'Simple ZMQ Socket Commander'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-b', '--broker', help='Message broker', required=True)
    parser.add_argument('-p', '--port', help='Port for message receiver', required=True)
    parser.add_argument('-c', '--command', help='Command to send', required=True)
    parser.add_argument('-i', '--id', help='Build ID', required=True)
    parser.add_argument('-s', '--src', help='Source Code URI', required=True)
    parser.add_argument('-zp', '--platform', help='Platform to build', required=True)
    args = parser.parse_args()
    logger(args.broker, args.port, args.command, args.id, args.src, args.platform)

if __name__ == '__main__':
    log()

