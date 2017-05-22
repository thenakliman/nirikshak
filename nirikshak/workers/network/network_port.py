import logging
import socket

from nirikshak.workers import base


PROTOCOL_MAPPING = {
    'tcp': socket.SOCK_STREAM,
    'udp': socket.SOCK_DGRAM
}


@base.match_expected_output
@base.validate(required=('ip', 'port'), optional=('protocol',))
def work(**kwargs):
    k = kwargs['input']['args']
    host = k['ip']
    port = k['port']
    protocol = kwargs.get('protocol', 'tcp')
    sock = socket.socket(socket.AF_INET,
                         PROTOCOL_MAPPING[protocol])
    sock.settimeout(1)
    status = sock.connect_ex((host, port))
    logging.info("Reurnted code for %s host and %s ip is %d", k['ip'],
                 k['port'], status)
    sock.close()
    return status
