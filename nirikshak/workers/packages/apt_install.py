import logging
import apt

from nirikshak.common import constants
from nirikshak.common import synchronizer
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


LOCK_NAME = 'APT'


@base.register('packages')
class APTWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('package',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        LOCK_INDEX = getattr(constants.LOCKABLE_RESOURCES_INDEX, LOCK_NAME)
        synchronizer.lock[LOCK_INDEX].acquire()
        cache = apt.cache.Cache()
        cache.update()
        pkg = cache[k['package']]
        status = pkg.is_installed
        sychronizer.lock[LOCK_INDEX].release()
        LOG.info("%s package is %s" % (k['package'], status))
        return status
