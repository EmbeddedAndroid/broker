import zmq

def broker():
    context = zmq.Context()
    # recieve work
    broker_receiver = context.socket(zmq.PULL)
    broker_receiver.bind("tcp://*:5555")
    # publish work
    broker_publisher = context.socket(zmq.PUB)
    broker_publisher.bind("tcp://*:5556")
    
    while True:
        work = broker_receiver.recv_json()
        if 'message' in work and 'id' in work:
            print 'Received Message: %s from %s' % (work['message'], work['id'])
            broker_publisher.send(work['id'], work['message'])
        if 'command' in work:
            print 'Command Received'

if __name__ == '__main__':
    broker()
