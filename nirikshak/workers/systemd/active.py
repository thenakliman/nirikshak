# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import dbus

from nirikshak.common import plugins
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@plugins.register('systemd_active')
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
                LOG.info("%s unit is active", k['service'])
                return str(unit[3])

        LOG.info("%s unit is not active", k['service'])
        return ''
