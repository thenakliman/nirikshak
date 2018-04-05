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

import unittest

import mock
import ping

from nirikshak.workers.network import connectivity


class NetworkConnectivityTest(unittest.TestCase):
    @property
    def connectivity_jaanch(self):
        return {
            "name": "google_connectivity",
            "type": "network_connectivity",
            "input": {
                "args": {
                    "host": "hostname.com",
                }
            }
        }

    @mock.patch.object(ping, 'quiet_ping')
    def test_connection_pass(self, mock_ping):
        mock_ping.return_value = (0, 0.1212, 12.1222)
        connectivity_worker = connectivity.Connectivity()
        actual_jaanch_result = connectivity_worker.work(
            **self.connectivity_jaanch)
        exp_result = self.connectivity_jaanch
        exp_result['input']['result'] = True
        self.assertDictEqual(exp_result, actual_jaanch_result)

    @mock.patch.object(ping, 'quiet_ping')
    def test_connection_fail(self, mock_ping):
        mock_ping.return_value = (100, None, None)
        connectivity_worker = connectivity.Connectivity()
        actual_jaanch_result = connectivity_worker.work(
            **self.connectivity_jaanch)
        exp_result = self.connectivity_jaanch
        exp_result['input']['result'] = False
        self.assertDictEqual(exp_result, actual_jaanch_result)
