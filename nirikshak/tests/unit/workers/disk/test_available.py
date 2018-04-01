# Copyright 2018 <thenakliman@gmail.com>
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
import os

import unittest

from nirikshak.workers.disk import available


class DiskAvailabilityTest(unittest.TestCase):
    @property
    def fake_jaanch(self):
        return {
            'name': 'disk_available',
            'input': {
                'args': {
                    'mountpoint': '/root'
                }
            }
        }

    @mock.patch.object(os, 'statvfs')
    def test_disk_available_size(self, mocked_os_statvfs):
        f_frsize = 1024
        f_bavail = 10000
        stat = mock.Mock(f_frsize=f_frsize, f_bavail=f_bavail)
        mocked_os_statvfs.return_value = stat
        expected_result = self.fake_jaanch
        expected_result['input']['result'] = f_frsize * f_bavail
        self.assertDictEqual(
                available.DiskAvailable().work(**self.fake_jaanch),
                expected_result)
        mocked_os_statvfs.assert_called_once_with('/root')

    @mock.patch.object(os, 'statvfs')
    def test_disk_not_available_size(self, mocked_os_statvfs):
        mocked_os_statvfs.side_effect = OSError
        expected_result = self.fake_jaanch
        expected_result['input']['result'] = None
        self.assertDictEqual(
                available.DiskAvailable().work(**self.fake_jaanch),
                expected_result)
        mocked_os_statvfs.assert_called_once_with('/root')
