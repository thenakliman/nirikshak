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
import mock 

from nirikshak.tests.unit import base as test_base
from nirikshak.post_task import console


class TestFormatOutputConsole(test_base.BaseTestCase):
    def setUp(self):
        super(TestFormatOutputConsole, self).setUp()


    def tearDown(self):
        super(TestFormatOutputConsole, self).tearDown()


    @staticmethod
    def _get_fake_jaanch():
        fake_jaanch = {'jaanch': {}}
        fake_jaanch['jaanch'] = {
            'input': {
                'args': {'key': 'value'},
                'result': 10
                },
            'type': 'console',
             'output': {
                 'result': 10
             }
        }
        return fake_jaanch

    # NOTE(thenakliman): This method is tighly coupled with _get_fake_jaanch
    # so need to be updated on that method update.
    @staticmethod
    def _get_output_for_fake_jaanch(**jaanch):
        all_args_formatted = ''
        for key, value in jaanch['jaanch']['input']['args'].items():
            all_args_formatted += ('%s:%s,' % (key, value))

        jaanch_name_type_args_appended = ('%s,%s,%s' % ('jaanch', 'console',
                                                        all_args_formatted))
        required_empty_spaces = 120 - len(jaanch_name_type_args_appended)
        jaanch_result = None
        try:
            jaanch_result = "pass" if jaanch['jaanch']['input']['result'] == jaanch['jaanch']['output']['result'] else "fail"
        except KeyError:
            jaanch_result = jaanch['jaanch']['input']['result']

        jaanch['jaanch']['formatted_output'] = ('%s%s%s' % (jaanch_name_type_args_appended,
                                                 '.' * required_empty_spaces,
                                                 jaanch_result)) 

        return jaanch

    def _test_post_task_with_given_jaanch(self, fake_jaanch, mock_info_log):
        console_post_task = console.FormatOutputConsole()
        formatted_output = console_post_task.format_output(**fake_jaanch)
        # print(formatted_output, self._get_output_for_fake_jaanch(**copy.deepcopy(fake_jaanch)))
        self.assertDictEqual(formatted_output,
                             self._get_output_for_fake_jaanch(**copy.deepcopy(fake_jaanch)))
        mock_info_log.assert_called()

    @mock.patch.object(console.LOG, 'info')
    def test_post_task_for_console(self, mock_info_log):
        fake_jaanch = self._get_fake_jaanch()
        self._test_post_task_with_given_jaanch(fake_jaanch, mock_info_log)

    @mock.patch.object(console.LOG, 'info')
    def test_post_task_for_console_with_multiple_args(self, mock_info_log):
        fake_jaanch = self._get_fake_jaanch()
        fake_jaanch['jaanch']['input']['args']['key1'] = 'value1'
        self._test_post_task_with_given_jaanch(fake_jaanch, mock_info_log)

    @mock.patch.object(console.LOG, 'info')
    def test_post_task_for_console_that_fail(self, mock_info_log):
        fake_jaanch = self._get_fake_jaanch()
        fake_jaanch['jaanch']['output']['result'] = 20
        self._test_post_task_with_given_jaanch(fake_jaanch, mock_info_log)

    @mock.patch.object(console.LOG, 'info')
    def test_post_task_for_console_if_expected_output_not_given(self, mock_info_log):
        fake_jaanch = self._get_fake_jaanch()
        del fake_jaanch['jaanch']['output']['result']
        self._test_post_task_with_given_jaanch(fake_jaanch, mock_info_log)
