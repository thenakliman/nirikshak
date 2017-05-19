import psutil

from nirikshak.workers import base


@base.match_expected_output
@base.validate(required=('name',), optional=tuple())
def work(**kwargs):
    k = kwargs['input']['args']
    name = k['name']
    for proc in psutil.process_iter():
        try:
            if proc.name() == name:
                return True
        except psutil.NoSuchProcess:
            pass

    return False
