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

from nirikshak.post_task import base

PLUGIN_NAME = 'dummy_class'


def register_plugin():
    @base.register(PLUGIN_NAME)
    class DummyClass(base.FormatOutput):
        def format_output(self, **kwargs):
            if kwargs.get('jaanch').get('raise_exception'):
                raise Exception

            return ['soochis']


class TestRegister(unittest.TestCase):
    def tearDown(self):
        super(TestRegister, self).tearDown()
        base.POST_TASK_PLUGIN_MAPPER = {}

    def test_register_post_task(self):
        register_plugin()
        self.assertIsNotNone(base.get_plugin(PLUGIN_NAME))

    @staticmethod
    @mock.patch.object(base.LOG, 'info')
    def test_register_already_registered_plugin(mock_info_log):
        register_plugin()
        register_plugin()
        mock_info_log.assert_called()


class TestFormatForOutput(unittest.TestCase):
    def tearDown(self):
        super(TestFormatForOutput, self).tearDown()
        base.POST_TASK_PLUGIN_MAPPER = {}

    @staticmethod
    def _get_fake_jaanch():
        fake_jaanch = {'jaanch': {}}
        fake_jaanch['jaanch'] = {
            'post_task': 'dummy_class'
        }
        return fake_jaanch

    @mock.patch.object(base.LOG, 'info')
    def test_format_output_if_post_task_defined(self, mock_info_log):
        register_plugin()
        self.assertEqual(base.format_for_output(**self._get_fake_jaanch()),
                         ['soochis'])
        mock_info_log.assert_called()

    @mock.patch.object(base.LOG, 'error')
    def test_format_output_if_post_task_not_defined(self, mock_error_log):
        fake_jaanch = {'jaanch': {}}
        self.assertEqual(base.format_for_output(**fake_jaanch), fake_jaanch)
        mock_error_log.assert_called()

    @mock.patch.object(base.LOG, 'error')
    def test_format_output_if_error_occur_in_post_task(self, mock_error_log):
        register_plugin()
        fake_jaanch = {
            'jaanch': {
                'post_task': 'dummy_class',
                'raise_exception': True
                }
            }
        self.assertIsNone(base.format_for_output(**fake_jaanch))
        mock_error_log.assert_called()
