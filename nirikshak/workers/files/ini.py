import logging
import ConfigParser

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('ini')
class INIConfigValidatorWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('file', 'section', 'key'))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        config = ConfigParser.ConfigParser()
        config.read(k['file'])
        value = None
        try:
            value = config.get(k['section'], k['key'])
            LOG.info("%s configuration option found in %s section",
                     k['section'], k['key'])
        except Exception:
            LOG.error("Not able to find %s configuration parameter in %s "
                      "section" % (k['key'], k['section']))

        return value
