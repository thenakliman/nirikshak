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
import unittest

from nirikshak.workers.memory import usage


class TestMemoryUsage(unittest.TestCase):
    def setUp(self):
        super(TestMemoryUsage, self).setUp()

    @property
    def fake_jaanch(self):
        return {
            "name": "memory_usage",
            "type": "memory_usage",
            "input": {
                "args": {}
            }
        }

    @mock.patch.object(usage.psutil, "virtual_memory")
    def test_memory_usage(self, mock_virtual_memory):
        used_memory = 10.10
        mock_virtual_memory.return_value = mock.Mock(percent=used_memory)
        jaanch_result = usage.MemoryUsage().work(**self.fake_jaanch)
        self.assertEqual(used_memory, jaanch_result["input"]["result"])
        mock_virtual_memory.assert_called_once_with()
