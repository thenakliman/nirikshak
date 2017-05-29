import json
import logging
import requests

import nirikshak
from nirikshak.output import base

LOG = logging.getLogger(__name__)

SECTION = 'output_send'


@base.register('send')
class NetworkSendOutput(base.FormatOutput):
    def output(self, **kwargs):
        host = nirikshak.CONF[SECTION]['host']
        port = nirikshak.CONF[SECTION]['port']
        method = nirikshak.CONF[SECTION].get('method', 'put')
        protocol = nirikshak.CONF[SECTION].get('protocol', 'http')
        url = nirikshak.CONF[SECTION].get('url', '')
        url = ("%s://%s:%s/%s" % (protocol, host, port, url))
        key = kwargs.keys()[0]
        try:
            expected_result = kwargs[key]['output']['result']
        except KeyError:
            expected_result = None
        jaanch = base.make_output_dict(key, expected_result, **kwargs)
        payld = json.dumps(jaanch)
        try:
            getattr(requests, method)(url, data=payld)
        except requests.exceptions.ConnectionError:
            LOG.error("Error in output sent to %s host on %s port" % (
                      host, port))

        LOG.error("Output sent to %s host on %s port" % (host, port))