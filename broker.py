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

    msg_fields = ['type', 'id', 'status', 'message']
    cmd_fields = ['command', 'build', 'src', 'platform']
    
    while True:
        work = broker_receiver.recv_json()
        if all(msg_field in msg_fields for msg_field in work):
            print 'Received Message: Type: %s Status:' \
            ' %s %s from %s' % (work['type'], work['status'], work['message'], work['id'])
            print 'Publishing Message'
            broker_publisher.send_json(work)
        if all(cmd_field in cmd_fields for cmd_field in work):
            print 'Command Received'
            if 'start' == work['command']:
                api = pykube.HTTPClient(pykube.KubeConfig.from_service_account())
                with open('zephyr.yaml', 'r') as r:
                    raw = r.read()
                    pod = yaml.load(raw)
                    for section in pod['spec']['containers']:
                        if 'env' in section:
                            for env_v in section['env']:
                                if 'ZEPHYR_SOURCE' in env_v['name']:
                                    env_v['value'] = work['src']
                                elif 'ZEPHYR_BUILD_ID' in env_v['name']:
                                    env_v['value'] = work['build']
                                elif 'ZEPHYR_PLATFORM' in env_v['name']:
                                    env_v['value'] = work['platform']
                    pykube.Pod(api, pod).create()
                    print 'Pod Created'

if __name__ == '__main__':
    broker()
