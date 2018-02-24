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
import os

import mock
import nirikshak

from nirikshak.output import dump_yaml
from nirikshak.tests.unit import base as base_test


class YAMLFormatOutputTest(base_test.BaseTestCase):
    def setUp(self):
        super(YAMLFormatOutputTest, self).setUp()
        base_test.create_conf()

    def tearDown(self):
        super(YAMLFormatOutputTest, self).tearDown()
        nirikshak.CONF.clear()

    # pylint: disable=no-self-use
    @mock.patch.object(dump_yaml.YAMLFormatOutput, 'read_file')
    @mock.patch.object(dump_yaml.YAMLFormatOutput, '_write_file')
    def test_conf_without_section(self, mock_output_yaml, mock_output_file):
        f_name = '/var/lib/nirikshak/result.yaml'
        soochis = base_test.get_test_keystone_soochi()['jaanches']
        mock_output_file.return_value = {'port_5000': soochis['port_5000']}
        exp = {'port_35357': soochis['port_35357']}
        dump_yaml.YAMLFormatOutput().output(**exp)
        result = {
            'port_35357': {
                'input': soochis['port_35357']['input']['args'],
                'output': None
            }
        }
        result.update({'port_5000': soochis['port_5000']})
        mock_output_file.assert_called_with(f_name)
        mock_output_yaml.assert_called_with(result, f_name)

    @mock.patch.object(dump_yaml.YAMLFormatOutput, 'read_file')
    @mock.patch.object(dump_yaml.YAMLFormatOutput, '_write_file')
    def test_conf_with_section(self, mock_output_yaml, mock_output_file):
        nirikshak.CONF['output_yaml'] = {'output_dir':
                                         '/var/nirikshak/result.yaml'}
        f_name = nirikshak.CONF['output_yaml']['output_dir']
        soochis = base_test.get_test_keystone_soochi()['jaanches']
        soochis['port_35357']['output']['result'] = 'test'
        soochis['port_35357']['input']['result'] = 'test'
        mock_output_file.return_value = {}
        exp = {'port_35357': soochis['port_35357']}
        dump_yaml.YAMLFormatOutput().output(**exp)
        result = {
            'port_35357': {
                'input': soochis['port_35357']['input']['args'],
                'output': {'actual_output': 'test', 'expected_output': 'test'}
            }
        }
        mock_output_file.assert_called_with(f_name)
        mock_output_yaml.assert_called_with(result, f_name)

    @mock.patch.object(os, 'stat')
    def test_get_output_file(self, mock_os):
        mock_os.return_value = mock.Mock(st_size=False)
        yaml = dump_yaml.YAMLFormatOutput().read_file('test_file')
        self.assertEqual({}, yaml)
        mock_os.assert_called_with('test_file')

    @mock.patch.object(os, 'stat')
    def test_get_output_file_error(self, mock_os):

        def test():
            raise OSError()

        mock_os.side_effect = test
        yaml = dump_yaml.YAMLFormatOutput().read_file('test_file')
        self.assertEqual({}, yaml)
        mock_os.assert_called_with('test_file')
