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
import configparser

import mock

from nirikshak.tests.unit import base
from nirikshak.workers.files import ini


class INIConfigValidatorWorkerTest(base.BaseTestCase):

    # pylint: disable=unused-argument
    @mock.patch.object(configparser.ConfigParser, 'read')
    @mock.patch.object(configparser.ConfigParser, 'get')
    def test_init_config_validtor(self, mock_config_get, mock_config_parser):
        jaanch = base.get_ini_jaanch()

        def test_get(section, key):
            return 'debug'

        mock_config_get.side_effect = test_get
        result = ini.INIConfigValidatorWorker().work(**jaanch)
        self.assertEqual(result, jaanch)

    @mock.patch.object(configparser.ConfigParser, 'read')
    def test_init_invalid_config(self, mock_config_parser):
        jaanch = base.get_ini_jaanch()

        def test_get(section=None, key=None):
            raise ValueError

        mock_config_parser.get = test_get
        result = ini.INIConfigValidatorWorker().work(**jaanch)
        self.assertEqual(result, jaanch)
