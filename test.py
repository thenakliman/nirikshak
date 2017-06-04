from nirikshak.common import yaml_util
from nirikshak.workers.packages import apt_install


def test_worker():
    inp = yaml_util.get_yaml('/var/nirikshak/paypal.yaml')
    apt_install.APTWorker().work(**(inp['jaanches'].values()[0]))


test_worker()
