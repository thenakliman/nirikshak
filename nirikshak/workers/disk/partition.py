import psutil

from nirikshak.workers import base
# parted can be used, but it requires root privilege and libparted-dev


@base.match_expected_output
@base.validate(required=('device',),
               optional=('fstype', 'mountpoint',))
def work(**kwargs):
    k = kwargs['input']['args']
    disks = psutil.disk_partitions()
    result = False
    for disk in disks:
        if k['device'] == disk.device:
            result = True
            for key, value in k.items():
                result = result & (getattr(disk, key) == value)

            return result

    logging.error("%s device could not be found on the syste." % k['device'])
    return None
