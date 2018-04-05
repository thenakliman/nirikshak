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

    @mock.patch.object(ping, 'Ping')
    def test_connection_pass(self, mock_ping):
        mock_ping_do = mock.Mock(do=mock.Mock(return_value=10))
        mock_ping.return_value = mock_ping_do
        connectivity_worker = connectivity.Connectivity()
        actual_jaanch_result = connectivity_worker.work(
            **self.connectivity_jaanch)
        exp_result = self.connectivity_jaanch
        exp_result['input']['result'] = True
        self.assertDictEqual(exp_result, actual_jaanch_result)

    @mock.patch.object(ping, 'Ping')
    def test_connection_fail(self, mock_ping):
        mock_ping_do = mock.Mock(do=mock.Mock(return_value='timeout error'))
        mock_ping.return_value = mock_ping_do
        connectivity_worker = connectivity.Connectivity()
        actual_jaanch_result = connectivity_worker.work(
            **self.connectivity_jaanch)
        exp_result = self.connectivity_jaanch
        exp_result['input']['result'] = False
        self.assertDictEqual(exp_result, actual_jaanch_result)
