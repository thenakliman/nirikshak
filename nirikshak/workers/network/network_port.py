# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
