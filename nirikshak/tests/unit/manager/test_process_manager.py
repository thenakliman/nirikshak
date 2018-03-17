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

import os
import mock

from nirikshak.input import base as base_input
from nirikshak.manager import process
from nirikshak.workers import base as base_worker
from nirikshak.output import base as base_output
from nirikshak.post_task import base as base_post_task


class ProcessWorkManager(unittest.TestCase):
    @mock.patch.object(base_input, 'get_soochis', return_value=[])
    def test_get_soochis_with_empty_soochi_and_group(self, mock_get_soochis):
        process.start(soochis=[], groups=[])
        mock_get_soochis.assert_called_once_with(soochis=[], groups=[])

    @staticmethod
    def _get_fake_jaanch():
        return [
                [{'key1': 'value1'},
                    {'jaanch1': {'jaanch1_param': 'jaanch1_body'}}],
                [{'key2': 'value2'},
                    {'jaanch2': {'jaanch2_param': 'jaanch2_body', 'k2': 'v2'}}]
        ]

    @staticmethod
    def _get_expected_jaanch():
        return [{'jaanch1_param': 'jaanch1_body', 'key1': 'value1'},
                {'jaanch2_param': 'jaanch2_body',
                 'key2': 'value2', 'k2': 'v2'}]

    # NOTE(thenakliman): However _enrich_config is a private method to
    # the module, we are testing to spot bugs  easily.
    def test_get_soochis_called_with_multiple_soochis(self):
        jaanch = process._enrich_config(self._get_fake_jaanch())
        exp_jaanches = self._get_expected_jaanch()
        for actual_jaanch, expected_jaanch in zip(jaanch, exp_jaanches):
            self.assertDictEqual(actual_jaanch, expected_jaanch)

    @mock.patch.object(process, '_handle_post_processing')
    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(base_input, 'get_soochis')
    def test_process_are_being_created_for_soochis(
            self, mock_get_soochis,
            mock_do_work,
            mock_handle_post_processing):

        def side_effect(**kwargs):
            return {'pid': os.getpid()}

        mock_do_work.side_effect = side_effect
        mock_get_soochis.return_value = self._get_fake_jaanch()
        process.start(soochis=['keystone, glance'])
        self.assertEqual(2, mock_handle_post_processing.call_count)
        calls = [call.__repr__() for call in
                 mock_handle_post_processing.call_args_list]
        self.assertEqual(len(calls), len(set(calls)))

    @mock.patch.object(base_output, 'output')
    @mock.patch.object(base_post_task, 'format_for_output')
    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(base_input, 'get_soochis')
    def test_output_has_been_called(self, mock_get_soochis, mock_do_work,
                                    mock_post_task, mock_output):
        def do_work_side_effect(**kwargs):
            return {'do_work': True}

        def post_task_side_effect(**kwargs):
            kwargs['post_task'] = True
            return kwargs

        def output_side_effect(**kwargs):
            kwargs['output'] = True
            return kwargs

        mock_get_soochis.return_value = self._get_fake_jaanch()
        mock_do_work.side_effect = do_work_side_effect
        mock_post_task.side_effect = post_task_side_effect
        mock_output.side_effect = output_side_effect

        process.start(soochis=['keystone, glance'])

        post_task_call = mock.call(do_work=True)
        mock_post_task.assert_has_calls([post_task_call, post_task_call])
        mock_output_call = mock.call(do_work=True, post_task=True)
        mock_output.assert_has_calls([mock_output_call, mock_output_call])
