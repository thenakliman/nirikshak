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
import copy
import os

import mock
import yaml

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import yaml_util
from nirikshak.output import dump_yaml
from nirikshak.tests.unit import base as base_test

TEST_FILE = 'test_file'


class YAMLFormatOutputTest(base_test.BaseTestCase):
    def setUp(self):
        super(YAMLFormatOutputTest, self).setUp()
        base_test.create_conf()

    def tearDown(self):
        super(YAMLFormatOutputTest, self).tearDown()
        nirikshak.CONF.clear()

    # pylint: disable=no-self-use
    @mock.patch.object(dump_yaml, 'open')
    @mock.patch.object(dump_yaml.YAMLFormatOutput, 'read_file')
    @mock.patch.object(yaml, 'dump')
    def test_conf_without_section(self, mock_yaml_dump,
                                  mock_read_file, mock_open):

        f_name = '/var/lib/nirikshak/result.yaml'
        soochi1, soochi2 = base_test.get_test_keystone_soochi()
        mock_read_file.return_value = copy.deepcopy([soochi1])
        dump_yaml.YAMLFormatOutput().output(**soochi2)
        exp_result = {
            'name': 'port_3537',
            'input': soochi2['input']['args'],
            'output': {}
        }
        exp_soochis = [copy.deepcopy(soochi1), exp_result]
        mock_read_file.assert_called_with(f_name)
        mock_yaml_dump.assert_called_once_with(exp_soochis, mock.ANY,
                                               default_flow_style=False)
        mock_open.assert_called_once_with(f_name, "w")

    @mock.patch.object(dump_yaml.YAMLFormatOutput, 'read_file')
    @mock.patch.object(dump_yaml.YAMLFormatOutput, '_write_file')
    def test_conf_with_section(self, mock_output_yaml, mock_output_file):
        nirikshak.CONF['output_yaml'] = {'output_dir':
                                         '/var/nirikshak/result.yaml'}
        f_name = nirikshak.CONF['output_yaml']['output_dir']
        soochi1, soochi2 = base_test.get_test_keystone_soochi()
        soochi2['output']['result'] = 'test'
        soochi2['input']['result'] = 'test'
        mock_output_file.return_value = []
        dump_yaml.YAMLFormatOutput().output(**soochi2)
        exp_result = [{
                'name': soochi2['name'],
                'input': soochi2['input']['args'],
                'output': {'actual_output': 'test', 'expected_output': 'test'}
            }]
        mock_output_file.assert_called_with(f_name)
        mock_output_yaml.assert_called_with(exp_result, f_name)

    @mock.patch.object(os, 'stat')
    def test_get_output_file(self, mock_os):
        mock_os.return_value = mock.Mock(st_size=False)
        yaml = dump_yaml.YAMLFormatOutput().read_file(TEST_FILE)
        self.assertEqual({}, yaml)
        mock_os.assert_called_with(TEST_FILE)

    @mock.patch.object(os, 'stat')
    def test_get_output_file_error(self, mock_os_stat):

        def test(fileLocation):
            raise OSError()

        mock_os_stat.side_effect = test
        yaml = dump_yaml.YAMLFormatOutput().read_file(TEST_FILE)
        self.assertEqual({}, yaml)
        mock_os_stat.assert_called_with(TEST_FILE)

    @mock.patch.object(yaml_util, 'get_yaml', return_value={})
    @mock.patch.object(os, 'stat')
    def test_get_output_file_get_yaml_success(self, mock_os, mock_get_yaml):
        mock_os.return_value = mock.Mock(st_size=1000)
        yaml = dump_yaml.YAMLFormatOutput().read_file(TEST_FILE)
        self.assertEqual({}, yaml)
        mock_os.assert_any_call(TEST_FILE)
        mock_get_yaml.assert_called_once_with(TEST_FILE)

    @mock.patch.object(yaml_util, 'get_yaml',
                       side_effect=exceptions.FileNotFound(location=TEST_FILE))
    @mock.patch.object(os, 'stat')
    def test_get_output_file_FileNotFoundError(self, mock_os, mock_get_yaml):
        yaml = dump_yaml.YAMLFormatOutput().read_file(TEST_FILE)
        self.assertEqual({}, yaml)
        mock_os.assert_any_call(TEST_FILE)
        mock_get_yaml.assert_called_once_with(TEST_FILE)

    @mock.patch.object(yaml_util, 'get_yaml', side_effect=IOError)
    @mock.patch.object(os, 'stat')
    def test_get_output_file_IOError(self, mock_os, mock_get_yaml):
        yaml = dump_yaml.YAMLFormatOutput().read_file(TEST_FILE)
        self.assertEqual({}, yaml)
        mock_os.assert_any_call(TEST_FILE)
        mock_get_yaml.assert_called_once_with(TEST_FILE)
