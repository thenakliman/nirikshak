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

import csv
import mock

import nirikshak
from nirikshak.tests.unit import base as base_test
from nirikshak.output import dump_csv


class TestOutputCSV(base_test.BaseTestCase):
    def setUp(self):
        super(TestOutputCSV, self).setUp()
        base_test.create_conf()
        nirikshak.CONF['output_csv'] = {
            'output_dir': 'test_dir'
        }

    def tearDown(self):
        super(TestOutputCSV, self).tearDown()
        nirikshak.CONF.clear()

    @staticmethod
    def _get_fake_jaanch():
        jaanch = {'jaanch': {}}
        jaanch['jaanch'] = {
            'output': {},
            'input': {'args': {'key': 'value'}}
        }
        return jaanch

    # NOTE(thenakliman): this method is tightly coupled with _get_fake_jaanch
    @staticmethod
    def _get_expected_csv_output_from_jaanch(jaanch):
        exp_result = jaanch['jaanch']['output'].get('result')
        return ('jaanch,input,key,value,output,expected_output,%s,'
                'actual_output,None' % exp_result).split(',')

    @mock.patch.object(dump_csv.LOG, 'info')
    @mock.patch.object(csv, 'writer')
    @mock.patch.object(csv, 'reader')
    @mock.patch.object(dump_csv, 'open')
    def test_dump_to_existing_file(self, mock_open, mock_csv_reader,
                                   mock_csv_writer, mock_info_log):
        csv_sample_value = (['test_entry1'], ['test_entry2'])
        jaanch = self._get_fake_jaanch()
        mock_csv_reader.return_value = csv_sample_value
        mock_open.__enter__ = mock.Mock()
        mock_writerow = mock.Mock()
        mock_csv_writer.return_value = mock.Mock(writerow=mock_writerow)
        mock_csv_writer_writerow = mock.Mock()
        mock_csv_writer.writerow = mock_csv_writer_writerow
        dump_csv.CSVFormatOutput().output(**jaanch)
        mock_csv_reader.assert_called_once_with(mock.ANY, delimiter=' ', quotechar='|')
        csv_sample_value += ('jaanch,input,key,value,output,expected_output,None,actual_output,None'.split(','),)
        mock_writerow.assert_has_calls([mock.call(value) for value in csv_sample_value])
        self.assertEqual(3, mock_writerow.call_count)
        mock_info_log.assert_called()

    def _test_for_dump_csv(self, mock_open, mock_csv_writer,
                           mock_info_log, jaanch=None):
        if jaanch is None:
            jaanch = self._get_fake_jaanch()

        def mock_dump_csv_open(file_name, mode):
            if mode == 'w':
                mock_open.__enter__ = mock.Mock()
                mock_open.__exit__ = mock.Mock()
                return mock_open

            raise IOError

        mock_open.side_effect = mock_dump_csv_open
        mock_writerow = mock.Mock()
        mock_csv_writer.return_value = mock.Mock(writerow=mock_writerow)
        mock_csv_writer_writerow = mock.Mock()
        mock_csv_writer.writerow = mock_csv_writer_writerow
        dump_csv.CSVFormatOutput().output(**jaanch)
        csv_sample_value = self._get_expected_csv_output_from_jaanch(jaanch)
        mock_writerow.assert_has_calls([mock.call(csv_sample_value)])
        mock_info_log.assert_called()

    @mock.patch.object(dump_csv.LOG, 'info')
    @mock.patch.object(csv, 'writer')
    @mock.patch.object(dump_csv, 'open')
    def test_dump_to_non_existing_file(self, mock_open, mock_csv_writer,
                                       mock_info_log):
        self._test_for_dump_csv(mock_open, mock_csv_writer, mock_info_log)

    @mock.patch.object(dump_csv.LOG, 'info')
    @mock.patch.object(csv, 'writer')
    @mock.patch.object(dump_csv, 'open')
    def test_dump_to_file_with_expected_result_in_jaanch(self, mock_open,
                                                         mock_csv_writer,
                                                         mock_info_log):
        jaanch = self._get_fake_jaanch()
        jaanch['jaanch']['output']['result'] = 10
        self._test_for_dump_csv(mock_open, mock_csv_writer,
                                mock_info_log, jaanch)

    @mock.patch.object(dump_csv.LOG, 'info')
    @mock.patch.object(csv, 'writer')
    @mock.patch.object(dump_csv, 'open')
    def test_dump_to_file_with_output_dir_not_in_conf(self, mock_open,
                                                      mock_csv_writer,
                                                      mock_info_log):
        del nirikshak.CONF['output_csv']['output_dir']
        self._test_for_dump_csv(mock_open, mock_csv_writer, mock_info_log)
