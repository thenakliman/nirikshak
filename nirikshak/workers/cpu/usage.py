import logging
import psutil

from nirikshak.common import plugins
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@plugins.register('cpu_usage')
class CPUUsage(base.Worker):
    @base.match_expected_output
    @base.validate(required=tuple())
    def work(self, **jaanch):
        cpu_percent = psutil.cpu_percent()
        LOG.info("CPU usage for %s jaanch is %d", jaanch['name'], cpu_percent)
        return cpu_percent
