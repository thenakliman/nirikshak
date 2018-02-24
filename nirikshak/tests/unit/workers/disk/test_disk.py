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
from nirikshak.workers import base as base_worker
from nirikshak.workers.disk import partition


class DiskPartitionWorkerTest(base.BaseTestCase):
    @staticmethod
    def get_mocked_disk():
        mock_device1 = mock.Mock()
        mock_device2 = mock.Mock()
        mock_device1.device = '/dev/sda5'
        mock_device1.mountpoint = '/'
        mock_device1.fstype = 'ext4'
        mock_device1.opts = 'rw,relatime,errors=remount-ro,data=ordered'
        mock_device2.device = '/dev/sda1'
        mock_device2.mountpoint = '/'
        mock_device2.fstype = 'ext4'
        mock_device2.opts = 'rw,relatime,errors=remount-ro,data=ordered'
        return [mock_device1, mock_device2]

    @mock.patch.object(psutil, 'disk_partitions')
    def test_disk_partition(self, mock_disk_partition):
        jaanch = base.get_disk_jaanch()
        mock_disk_partition.return_value = self.get_mocked_disk()
        result = partition.DiskPartitionWorker().work(**jaanch)
        self.assertTrue(result['input']['result'])

    @mock.patch.object(psutil, 'disk_partitions')
    def test_disk_partition_not_exist(self, mock_disk_partition):
        jaanch = base.get_disk_jaanch()
        jaanch['input']['args']['device'] = '/dev/vda1'
        mock_disk_partition.return_value = self.get_mocked_disk()
        result = partition.DiskPartitionWorker().work(**jaanch)
        jaanch['input']['result'] = None
        self.assertEqual(result, jaanch)
