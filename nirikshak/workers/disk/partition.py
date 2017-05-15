import psutil
# parted can be used, but it requires root privilege and libparted-dev


def work(**kwargs):
    k = kwargs['input']['args']
    disks = psutil.disk_partitions()
    result = False
    for disk in disks:
        if k['device'] == disk.device:
            result = True
            for key, value in k.items():
                result = result & (getattr(disk, key) == value)

            break

    kwargs['input']['result'] = result
    return kwargs
