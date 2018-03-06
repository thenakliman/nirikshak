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

import json
import logging
import requests

import nirikshak
from nirikshak.output import base
from nirikshak.common import plugins
from nirikshak.common import validators

LOG = logging.getLogger(__name__)

SECTION = 'output_send'


@plugins.register('send')
class NetworkSendOutput(base.FormatOutput):
    @validators.config_validator(SECTION, ('host', 'port'))
    def output(self, **kwargs):
        host = nirikshak.CONF[SECTION]['host']
        port = nirikshak.CONF[SECTION]['port']
        method = nirikshak.CONF[SECTION].get('method', 'put')
        protocol = nirikshak.CONF[SECTION].get('protocol', 'http')
        url = nirikshak.CONF[SECTION].get('url', '')
        url = ("%s://%s:%s/%s" % (protocol, host, port, url))
        key = list(kwargs.keys())[0]
        try:
            expected_result = kwargs[key]['output']['result']
        except KeyError:
            expected_result = None
        jaanch = base.make_output_dict(key, expected_result, **kwargs)
        payld = json.dumps(jaanch)
        try:
            getattr(requests, method)(url, data=payld)
        except requests.exceptions.ConnectionError:
            LOG.error("Error in output sent to %s host on %s port", host, port)

        LOG.info("Output sent to %s host on %s port", host, port)
