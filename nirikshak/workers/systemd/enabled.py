import dbus

from nirikshak.workers import base


@base.match_expected_output
@base.validate(required=('service',), optional=('status',))
def work(**kwargs):
    k = kwargs['input']['args']
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                 '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
    service = k['service']
    return manager.GetUnitFileState(service)
