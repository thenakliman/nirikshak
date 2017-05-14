import socket


PROTOCOL_MAPPING = {
    'tcp': socket.SOCK_STREAM,
    'udp': socket.SOCK_DGRAM
}


def work(**kwargs):
    k = kwargs['input']['args']
    host = k['ip']
    port = k['port']
    protocol = kwargs.get('protocol', 'tcp')
    sock = socket.socket(socket.AF_INET,
                         PROTOCOL_MAPPING[protocol])
    sock.settimeout(1)
    kwargs['input']['result'] = sock.connect_ex((host, port))
    sock.close()
    return kwargs
