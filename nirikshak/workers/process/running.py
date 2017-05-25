import logging
import psutil

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('process_running')
class RunningProcessWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('name',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        name = k['name']
        for proc in psutil.process_iter():
            try:
                if proc.name() == name:
                    LOG.info("%s process is running" % name)
                    return True
            except psutil.NoSuchProcess:
                pass

        LOG.info("%s process ins not running")
        return False
