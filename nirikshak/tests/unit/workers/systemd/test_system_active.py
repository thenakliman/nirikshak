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

import mock

from nirikshak.tests.unit import base
from nirikshak.workers.systemd import active


class SystemdActiveWorkerTest(base.BaseTestCase):

    @staticmethod
    def _get_fake_systemd_active_jaanch():
        jaanch = {
            'type': 'systemd_active',
            'input': {
                'args': {
                    'service': 'ssh.service'
                }
            }
        }

        return jaanch

    @staticmethod
    def _get_fake_systemd_unit():
        units = [['ssh.service', 'test', 'test1', 'active'],
                 ['test.service', 'test', 'test2', 'inactive']]
        return units

    @mock.patch('dbus.Interface')
    @mock.patch('dbus.SystemBus')
    def test_system_active(self, mock_system_bus, mock_interface):
        sys = mock.Mock()
        sys.get_object = mock.Mock(return_value=mock.Mock())
        mock_system_bus.return_value = sys
        mock_interface.return_value = mock.Mock()
        mock_interface.return_value.ListUnits = mock.Mock()
        return_value = self._get_fake_systemd_unit()
        mock_interface.return_value.ListUnits.return_value = return_value
        jaanch = self._get_fake_systemd_active_jaanch()
        result = active.SystemdActiveWorker().work(**jaanch)
        self.assertEqual('active', result['input']['result'])

    @mock.patch('dbus.Interface')
    @mock.patch('dbus.SystemBus')
    def test_system_invalid_active(self, mock_system_bus, mock_interface):
        sys = mock.Mock()
        sys.get_object = mock.Mock(return_value=mock.Mock())
        mock_system_bus.return_value = sys
        mock_interface.return_value = mock.Mock()
        ret_value = self._get_fake_systemd_unit()
        ret_value[0][0] = 'test_service'
        mock_interface.return_value.ListUnits = mock.Mock()
        mock_interface.return_value.ListUnits.return_value = ret_value
        jaanch = self._get_fake_systemd_active_jaanch()
        result = active.SystemdActiveWorker().work(**jaanch)
        self.assertEqual('', result['input']['result'])
