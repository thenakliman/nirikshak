import logging
import apt

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('packages')
class APTWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('package',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        cache = apt.cache.Cache()
        cache.update()
        pkg = cache[k['package']]
        status = pkg.is_installed
        LOG.info("%s package is %s" % (k['package'], status))
        return status
