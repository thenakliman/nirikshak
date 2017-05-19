import ConfigParser

from nirikshak.workers import base


@base.match_expected_output
@base.validate(required=('service',), optional=('status',))
def work(**kwargs):
    k = kwargs['input']['args']
    config = ConfigParser.ConfigParser()
    config.read(k['file'])
    return config.get(k['section'], k['key'])
