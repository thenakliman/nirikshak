import logging
import apt

from nirikshak.common import constants
from nirikshak.common import synchronizer
from nirikshak.workers import base

LOG = logging.getLogger(__name__)

LOCK_NAME = 'APT'


@base.register('apt_install')
class APTWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('package',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        LOCK_INDEX = getattr(constants.LOCKABLE_RESOURCES_INDEX, LOCK_NAME)
        LOG.info("Acquiring lock for %s jaanch", kwargs)
        with synchronizer.LOCK[LOCK_INDEX]:
            LOG.info("Acquired lock for %s jaanch", kwargs)
            cache = apt.cache.Cache()
            cache.update()
            pkg = cache[k['package']]
            status = pkg.is_installed
            # synchronizer.LOCK[LOCK_INDEX].release()
        LOG.info("Released lock for %s jaanch", kwargs)
        LOG.info("%s package is %s" % (k['package'], status))
        return status
