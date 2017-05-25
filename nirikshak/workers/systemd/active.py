import logging
import dbus

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('systemd_active')
class SystemdActiveWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('service',), optional=('status',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        sysbus = dbus.SystemBus()
        systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                     '/org/freedesktop/systemd1')
        manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
        service = k['service']
        units = manager.ListUnits()
        kwargs['input']['result'] = False
        for unit in units:
            if unit[0] == service:
                LOG.info("%s unit is active" % k['service'])
                return str(unit[3])

        LOG.info("%s unit is not active" % k['service'])
        return ''
