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
import socket
import unittest

from nirikshak.tests.unit import base
# FIXME(thenakliman): imported package inside base apt is not
# available for pip installation yet.
from nirikshak.workers.network import network_port


class WorkerTest(unittest.TestCase):
    def setUp(self):
        sample_jaanch = {}
        sample_jaanch = base.get_test_keystone_soochi()
        sample_jaanch = sample_jaanch['jaanches']['port_5000']
        self.sample_jaanch = sample_jaanch
        super(WorkerTest, self).setUp()

    @mock.patch.object(socket, 'socket')
    def test_work_with_invalid_port(self, socket):
        mock_sock = mock.Mock()
        mock_sock.connect_ex = mock.Mock(return_value=1)
        socket.return_value = mock_sock
        self.sample_jaanch['input']['result'] = 1
        res = network_port.NetworkPortWorker().work(**self.sample_jaanch)
        self.assertEqual(res, self.sample_jaanch)
