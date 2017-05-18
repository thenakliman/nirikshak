import dbus


def work(**kwargs):
    k = kwargs['input']['args']
    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1',
                                 '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')
    service = k['service']
    kwargs['input']['result'] = manager.GetUnitFileState(service)
    return kwargs
