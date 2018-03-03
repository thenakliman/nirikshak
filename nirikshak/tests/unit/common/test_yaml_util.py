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
import yaml

from nirikshak.common import yaml_util
from nirikshak.common import exceptions


class TestYamlUtil(unittest.TestCase):
    @mock.patch.object(yaml_util.yaml, 'load')
    @mock.patch.object(yaml_util, 'open')
    def test_get_invalid_yaml(self, mock_yaml_open, mock_yaml_load):
        location = 'tmp_location'
        mock_yaml_load.side_effect = yaml.scanner.ScannerError
        self.assertRaises(exceptions.InvalidFormatException,
                          yaml_util.get_yaml, location)
        mock_yaml_open.assert_called_once_with(location, 'r')

    @mock.patch.object(yaml_util, 'open')
    def test_get_non_existent_file(self, mock_yaml_open):
        location = 'tmp_location'
        mock_yaml_open.side_effect = IOError
        self.assertRaises(exceptions.FileNotFound,
                          yaml_util.get_yaml, location)
        mock_yaml_open.assert_called_once_with(location, 'r')

    @mock.patch.object(yaml_util.yaml, 'load')
    @mock.patch.object(yaml_util, 'open')
    def test_get_yaml_file(self, mock_yaml_open, mock_yaml_load):
        location = 'tmp_location'
        content = {'key': 'value'}
        mock_yaml_load.return_value = content
        self.assertDictEqual(content, yaml_util.get_yaml(location))
        mock_yaml_open.assert_called_once_with(location, 'r')
