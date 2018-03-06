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

from nirikshak.output import console
from nirikshak.tests.unit import base


class OutputTest(base.BaseTestCase):
    # pylint: disable=no-self-use
    def test_output(self):
        fake_jaanch = {
            'fake_jaanch': {
                'formatted_output': 'test-jaanch'
                }
            }
        with mock.patch.object(console, 'print') as mock_print:
            console.ConsoleFormatOutput().output(**fake_jaanch)
            mock_print.assert_called_once_with('test-jaanch')
