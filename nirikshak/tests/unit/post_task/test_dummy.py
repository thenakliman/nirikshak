import mock
import unittest

from nirikshak.post_task import dummy
from nirikshak.tests.unit import base


class PostTaskTest(unittest.TestCase):
    def test_format_main_dict(self):
        dct = base.get_main_yaml()
        self.assertEqual(str(dct), dummy.format_it(**dct))


    def test_format_soochi(self):
        dct = base.get_test_keystone_soochi()
        self.assertEqual(str(dct), dummy.format_it(**dct))


if __name__ == '__main__':
    unittest.main()
