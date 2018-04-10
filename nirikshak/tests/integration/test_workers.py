import copy
import os
import mock
import unittest


from nirikshak.common import utils
from nirikshak.workers import base
from nirikshak.workers.disk import available


class TestBaseWorker(unittest.TestCase):
    def setUp(self):
        utils.load_modules_from_location([os.path.dirname(base.__file__)])

    @property
    def fake_jaanch(self):
        return {
            "name": "fake_jaanch",
            "type": "disk_free_space",
            "input": {
                "args": {
                    "mountpoint": "/fake_mountpoint"
                },
                "result": 10
            }
        }

    @mock.patch.object(available.os, "statvfs")
    def test_worker_exception_raised_return_same_jaanch(self, mock_stat_vfs):
        expected_result = self.fake_jaanch
        mock_stat_vfs.side_effect = Exception

        jaanch_result = base.do_work(**self.fake_jaanch)

        self.assertDictEqual(expected_result, jaanch_result)

    @mock.patch.object(available.os, "statvfs", side_effect=Exception)
    def test_worker_does_not_change_jaanch(self, mock_stat_vfs):
        input_jaanch = self.fake_jaanch
        duplicate_jaanch = copy.deepcopy(input_jaanch)

        base.do_work(**self.fake_jaanch)

        self.assertDictEqual(duplicate_jaanch, input_jaanch)
