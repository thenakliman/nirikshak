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
import unittest

from nirikshak.workers.cpu import usage


class TestCPUUsage(unittest.TestCase):
    @mock.patch.object(usage.psutil, 'cpu_percent')
    def test_cpu_usage(self, mock_psutil):
        cpu_jaanch = {
            "name": "cpu_usage",
            "type": "cpu_usage",
        }

        mock_psutil.return_value = 10.01
        cpu_usage_jaanch = usage.CPUUsage().work(**cpu_jaanch)
        self.assertEqual(cpu_usage_jaanch['input']['result'], 10.01)
