# Copyright 2018 <thenakliman@gmail.com>
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
import os

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import yaml_util
from nirikshak.input import file as input_file
from nirikshak.tests.unit import base


class InputFileTest(unittest.TestCase):
    def setUp(self):
        super(InputFileTest, self).setUp()
        base.create_conf()

    def tearDown(self):
        nirikshak.CONF.clear()
        super(InputFileTest, self).setUp()

    def test_raises_if_main_not_defined(self):
        del nirikshak.CONF['input_file']
        self.assertRaises(exceptions.ConfigurationNotFoundException,
                          input_file.InputFile().get_main_file)

    @mock.patch.object(yaml_util, 'get_yaml')
    def test_get_not_existing_yaml(self, mock_yaml_util):
        mock_yaml_util.side_effect = exceptions.FileNotFound(
            location='location')
        self.assertRaises(exceptions.FileNotFound,
                          input_file.InputFile().get_yaml_file, 'location')

    @mock.patch.object(os.path, 'dirname', return_value='dir')
    @mock.patch.object(yaml_util, 'get_yaml')
    def test_get_soochi_content(self, mock_yaml_util, mock_dir):
        exp_value = {'default': {}}
        mock_yaml_util.return_value = exp_value
        soochis = input_file.InputFile().get_soochi_content('soochi')
        self.assertDictEqual(soochis, exp_value)
