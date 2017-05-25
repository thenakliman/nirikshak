import logging
import socket

from nirikshak.workers import base

LOG = logging.getLogger(__name__)

PROTOCOL_MAPPING = {
    'tcp': socket.SOCK_STREAM,
    'udp': socket.SOCK_DGRAM
}


@base.register('network_port')
class NetworkPortWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('ip', 'port'), optional=('protocol',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        host = k['ip']
        port = k['port']
        protocol = kwargs.get('protocol', 'tcp')
        sock = socket.socket(socket.AF_INET,
                             PROTOCOL_MAPPING[protocol])
        sock.settimeout(1)
        status = sock.connect_ex((host, port))
        LOG.info("Reurnted code for %s host and %s ip is %d", k['ip'],
                 k['port'], status)
        sock.close()
        return status
