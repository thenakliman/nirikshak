import logging
import ConfigParser

from nirikshak.workers import base


@base.match_expected_output
@base.validate(required=('service',), optional=('status',))
def work(**kwargs):
    k = kwargs['input']['args']
    config = ConfigParser.ConfigParser()
    config.read(k['file'])
    value = None
    try:
        value = config.get(k['section'], k['key'])
        logging.info("%s configuration option found in %s section",
                     k['section'], k['key'])
    except Exception:
        logging.error("Not able to find %s configuration parameter in %s "
                      "section" % (k['key'], k['section']))

    return value
