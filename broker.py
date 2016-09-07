import time
import zmq
import random

def broker():
    context = zmq.Context()
    # recieve work
    broker_receiver = context.socket(zmq.PULL)
    broker_receiver.bind("tcp://0.0.0.0:5555")
    # send work
    #broker_sender = context.socket(zmq.PUSH)
    #broker_sender.connect("tcp://127.0.0.1:5558")
    
    while True:
        work = broker_receiver.recv_json()
        if 'message' in work and 'id' in work:
            print 'Received Message: %s from %s' % (work['message'], work['id'])
        if 'command' in work:
            print 'Command Received'

broker()
