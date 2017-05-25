import logging
import dbus

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('systemd_enabled')
class SystemdEnabledWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('service',), optional=('status',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                     '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        service = k['service']
        status = str(manager.GetUnitFileState(service))
        LOG.info("%s service is %s" % (k['service'],  status))
        return status
