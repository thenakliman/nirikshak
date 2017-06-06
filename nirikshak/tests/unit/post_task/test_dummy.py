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
