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

import json
import mock

import nirikshak
from nirikshak.output import dump_json
from nirikshak.tests.unit import base as base_test


class JSONFormatOutputTest(base_test.BaseTestCase):
    def setUp(self):
        super(JSONFormatOutputTest, self).setUp()
        base_test.create_conf()

    def tearDown(self):
        super(JSONFormatOutputTest, self).tearDown()
        nirikshak.CONF.clear()

    # pylint: disable=no-self-use
    @mock.patch.object(dump_json.JSONFormatOutput, 'get_output_file')
    @mock.patch.object(json, 'dumps')
    def test_conf_without_section(self, mock_output_json, mock_output_file):
        f_name = '/var/lib/nirikshak/result.json'
        soochis = base_test.get_test_keystone_soochi()['jaanches']
        mock_output_file.return_value = {'port_5000': soochis['port_5000']}
        exp = {'port_35357': soochis['port_35357']}
        # fixme(thenakliman): mock open method properly
        with mock.patch.object(dump_json, 'open') as mock_open:
            dump_json.JSONFormatOutput().output(**exp)
        result = {
            'port_35357': {
                'input': soochis['port_35357']['input']['args'],
                'output': {}
            }
        }
        result.update({'port_5000': soochis['port_5000']})
        mock_output_file.assert_called_once_with(f_name)
        mock_output_json.assert_called_once_with(result, indent=4,
                                                 sort_keys=True,
                                                 separators=(',', ': '))
        mock_open.assert_called_once_with(f_name, 'w')

    @mock.patch.object(dump_json.JSONFormatOutput, 'get_output_file')
    @mock.patch.object(dump_json.JSONFormatOutput, '_output_json')
    def test_conf_with_section(self, mock_output_json, mock_output_file):
        nirikshak.CONF['output_json'] = {'output_dir':
                                         '/var/nirikshak/result.json'}
        f_name = nirikshak.CONF['output_json']['output_dir']
        soochis = base_test.get_test_keystone_soochi()['jaanches']
        soochis['port_35357']['output']['result'] = 'test'
        soochis['port_35357']['input']['result'] = 'test'
        mock_output_file.return_value = {}
        exp = {'port_35357': soochis['port_35357']}
        dump_json.JSONFormatOutput().output(**exp)
        result = {
            'port_35357': {
                'input': soochis['port_35357']['input']['args'],
                'output': {'actual_output': 'test', 'expected_output': 'test'}
            }
        }
        mock_output_file.assert_called_once_with(f_name)
        mock_output_json.assert_called_once_with(result, f_name)

    @mock.patch.object(os, 'stat')
    def test_get_output_file(self, mock_os):
        mock_os.return_value = mock.Mock(st_size=False)
        exp = dump_json.JSONFormatOutput().get_output_file('test_file')
        self.assertEqual({}, exp)
        mock_os.assert_called_once_with('test_file')

    @mock.patch.object(os, 'stat')
    def test_get_output_file_error(self, mock_os):
        # pylint: disable=unused-argument
        def test(loc):
            raise OSError()

        mock_os.side_effect = test
        exp = dump_json.JSONFormatOutput().get_output_file('test_file')
        self.assertEqual({}, exp)
        mock_os.assert_called_once_with('test_file')

    @mock.patch.object(json, 'load', return_value={})
    @mock.patch.object(dump_json, 'open')
    @mock.patch.object(os, 'stat')
    def test_get_output_file_json_dump_called(self, mock_os, mock_open, mock_json_load):
        mock_os.return_value = mock.Mock(st_size=1000)
        exp = dump_json.JSONFormatOutput().get_output_file('test_file')
        self.assertEqual({}, exp)
        mock_os.assert_called_once_with('test_file')
        mock_json_load.assert_called_once()
        mock_open.assert_called_once()

    @mock.patch.object(dump_json.LOG, 'error')
    @mock.patch.object(json, 'load', side_effect=ValueError)
    @mock.patch.object(dump_json, 'open')
    @mock.patch.object(os, 'stat')
    def test_get_output_file_content_json_error(self, mock_os, mock_open,
                                                mock_json_load, mock_error_log):
        mock_os.return_value = mock.Mock(st_size=1000)
        exp = dump_json.JSONFormatOutput().get_output_file('test_file')
        self.assertEqual({}, exp)
        mock_os.assert_any_call('test_file')
        mock_json_load.assert_called_once()
        mock_error_log.assert_called_once()
        mock_open.assert_called_once()
