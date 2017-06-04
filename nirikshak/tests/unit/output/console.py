import unittest

from nirikshak.output import console
from nirikshak.tests.unit import base


class OutputTest(unittest.TestCase):
    def test_output(self):
        inp = {}
        t = base.get_test_keystone_soochi()['jaanches']['port_5000']
        inp['port_5000'] = t
        inp['port_5000']['formatted_output'] = 'test_output'
        self.assertcalled(console.output(**inp), 'test_output')


unittest.main()
