import mock
import socket
import unittest

from nirikshak.tests.unit import base
from nirikshak.workers.network import network_port


class WorkerTest(unittest.TestCase):
    def setUp(self):
        sample_jaanch = {}
        sample_jaanch = base.get_test_keystone_soochi()['jaanches']['port_5000']
        self.sample_jaanch = sample_jaanch
        super(WorkerTest, self).setUp()

    @mock.patch.object(socket, 'socket')
    def test_work_with_invalid_port(self, socket):
        mock_sock = mock.Mock();
        mock_sock.connect_ex = mock.Mock(return_value=1)
        socket.return_value = mock_sock
        self.sample_jaanch['input']['result'] = 1
        self.assertEqual(network_port.work(**self.sample_jaanch),
                         self.sample_jaanch)


unittest.main()
