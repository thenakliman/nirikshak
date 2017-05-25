import logging
import psutil

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('disk_partition')
class DiskPartitionWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('device',),
                   optional=('fstype', 'mountpoint',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        disks = psutil.disk_partitions()
        result = False
        for disk in disks:
            if k['device'] == disk.device:
                result = True
                for key, value in k.items():
                    result = result & (getattr(disk, key) == value)

                return result

        LOG.error("%s device could not be found on the syste." % k['device'])
        return None
