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

import mock

from nirikshak.output import console
from nirikshak.tests.unit import base

@unittest.skip("Correct print function for python3")
class OutputTest(base.BaseTestCase):
    # pylint: disable=no-self-use
    def ttest_output(self):
        inp = {}
        t_soochis = base.get_test_keystone_soochi()['jaanches']['port_5000']
        inp['port_5000'] = t_soochis
        inp['port_5000']['formatted_output'] = 'test_output'
        with mock.patch.object(builtin, 'print') as mock_print:
            console.ConsoleFormatOutput().output(**inp)
            # fixme(thenakliman): mock print
            mock_print.assert_called()