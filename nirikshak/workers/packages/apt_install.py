import logging
import apt

from nirikshak.workers import base


@base.match_expected_output
@base.validate(('package',), tuple())
def work(**kwargs):
    k = kwargs['input']['args']
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[k['package']]
    status = pkg.is_installed
    logging.info("%s package is %s" % (k['package'], status))
    return status
