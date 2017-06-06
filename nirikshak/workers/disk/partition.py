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
import psutil

from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@base.register('disk_partition')
class DiskPartitionWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('device',),
                   optional=('fstype', 'mountpoint',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        disks = psutil.disk_partitions()
        result = False
        for disk in disks:
            if k['device'] == disk.device:
                result = True
                for key, value in k.items():
                    result = result & (getattr(disk, key) == value)

                return result

        LOG.error("%s device could not be found on the syste." % k['device'])
        return None
