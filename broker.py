import zmq
import yaml
import pykube

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
            print 'Publishing Message'
            broker_publisher.send_json(work)
        if 'command' in work and 'build' in work and 'src' in work and 'key' in work:
            print 'Command Received'
            if 'start' == work['command']:
                api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())
                with open('zephyr.yaml', 'r') as r:
                    raw = r.read()
                    pod = yaml.load(raw)
                    pykube.Pod(api, pod).create()
                    print 'Pod Created'

if __name__ == '__main__':
    broker()
