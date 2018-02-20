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
from nirikshak.workers.systemd import enabled


class SystemdActiveWorkerTest(base.BaseTestCase):

    @staticmethod
    def _get_fake_systemd_enabled_jaanch():
        jaanch = {
            'type': 'systemd_enabled',
            'input': {
                'args': {
                    'service': 'ssh.service'
                }
            }
        }

        return jaanch

    @mock.patch('dbus.Interface')
    @mock.patch('dbus.SystemBus')
    def test_system_enabled(self, mock_system_bus, mock_interface):
        sys = mock.Mock()
        sys.get_object = mock.Mock(return_value=mock.Mock())
        mock_system_bus.return_value = sys
        mock_interface.return_value = mock.Mock()
        mock_interface.return_value.GetUnitFileState = mock.Mock()
        mock_interface.return_value.GetUnitFileState.return_value = 'enabled'
        jaanch = self._get_fake_systemd_enabled_jaanch()
        result = enabled.SystemdEnabledWorker().work(**jaanch)
        self.assertEqual('enabled', result['input']['result'])

    @mock.patch('dbus.Interface')
    @mock.patch('dbus.SystemBus')
    def test_system_invalid_enabled(self, mock_system_bus, mock_interface):
        sys = mock.Mock()
        sys.get_object = mock.Mock(return_value=mock.Mock())
        mock_system_bus.return_value = sys
        mock_interface.return_value = mock.Mock()
        mock_interface.return_value.GetUnitFileState = mock.Mock()
        mock_interface.return_value.GetUnitFileState.side_effect = Exception()
        jaanch = self._get_fake_systemd_enabled_jaanch()
        result = enabled.SystemdEnabledWorker().work(**jaanch)
        self.assertEqual(None, result['input']['result'])
