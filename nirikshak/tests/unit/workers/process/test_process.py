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
import psutil

from nirikshak.tests.unit import base
from nirikshak.workers.process import running


class RunningProcessWorkerTest(base.BaseTestCase):

    @staticmethod
    def _get_fake_process_jaanch():
        jaanch = {
            'type': 'process_running',
            'input': {
                'args': {
                    'name': 'ssh'
                }
            }
        }

        return jaanch

    @staticmethod
    def _get_fake_process_details():
        mk1 = mock.Mock()
        mk1.name = mock.Mock(return_value='ssh')
        mk2 = mock.Mock()
        mk2.name = mock.Mock(return_value='abssh')
        return [mk1, mk2]

    @mock.patch.object(psutil, 'process_iter')
    def test_process_running(self, mock_psutil):
        jaanch = self._get_fake_process_jaanch()
        mock_psutil.return_value = self._get_fake_process_details()
        result = running.RunningProcessWorker().work(**jaanch)
        self.assertTrue(result['input']['result'])

    @mock.patch.object(psutil, 'process_iter')
    def test_process_running_invalid(self, mock_psutil):
        jaanch = self._get_fake_process_jaanch()
        names = self._get_fake_process_details()
        names[0].name.return_value = 'test_service'
        mock_psutil.return_value = names
        jaanch['input']['args']['name'] = 'invalid_process'
        result = running.RunningProcessWorker().work(**jaanch)
        self.assertFalse(result['input']['result'])

    @mock.patch.object(psutil, 'process_iter')
    def test_process_raise_invalid(self, mock_psutil):
        jaanch = self._get_fake_process_jaanch()
        names = self._get_fake_process_details()
        names[0].name.side_effect = psutil.NoSuchProcess('test')
        mock_psutil.return_value = names
        jaanch['input']['args']['name'] = 'ssh'
        result = running.RunningProcessWorker().work(**jaanch)
        self.assertFalse(result['input']['result'])
