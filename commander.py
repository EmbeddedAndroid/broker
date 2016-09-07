import zmq
import argparse

__version__ = 1.0

def logger(server, port, command, build, src, key):
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    uri = 'tcp://%s:%s' % (server, port)
    zmq_socket.connect(uri)
    message = { 'command': command, 'build': build, 'src': src, 'key': key }
    zmq_socket.send_json(message)

def log():
    description = 'Simple ZMQ Socket Commander'
    parser = argparse.ArgumentParser(version=__version__, description=description)
    parser.add_argument('-s', '--server', help='Message receiver', required=True)
    parser.add_argument('-p', '--port', help='Port for message receiver', required=True)
    parser.add_argument('-c', '--command', help='Command to send', required=True)
    parser.add_argument('-b', '--build', help='Build ID', required=True)
    parser.add_argument('-sc', '--src', help='Source Code URI', required=True)
    parser.add_argument('-k', '--key', help='Key to use', required=True)
    args = parser.parse_args()
    logger(args.server, args.port, args.command, args.build, args.src, args.key)

if __name__ == '__main__':
    log()

