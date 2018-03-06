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

import copy
import mock

from nirikshak.common import plugins
from nirikshak.output import base

PLUGIN_NAME = 'dummy_output'


def register_plugin():
    @plugins.register(PLUGIN_NAME)
    class DummyClass(base.FormatOutput):
        def output(self, **kwargs):
            if kwargs['jaanch'].get('raise_exception'):
                raise Exception

            kwargs['jaanch']['test_result'] = 'pass'
            return kwargs


def get_fake_jaanch():
    return {
        'jaanch': {
            'output': {
                'type': PLUGIN_NAME,
                'result': 10
            },
            'input': {
                'args': {
                    'key': 'value'
                }
            }
        }
    }


class TestOutputBase(unittest.TestCase):
    def tearDown(self):
        super(TestOutputBase, self).tearDown()
        plugins._PLUGINS.clear()

    @mock.patch.object(base.LOG, 'error')
    def test_output_for_non_existing_type(self, mock_error_log):
        fake_jaanch = get_fake_jaanch()
        fake_jaanch['jaanch']['output']['type'] = 'fake_plugin'
        self.assertDictEqual(fake_jaanch, base.output(**fake_jaanch))
        mock_error_log.assert_called()

    @staticmethod
    @mock.patch.object(base.LOG, 'error')
    def test_output_if_plugin_fails(mock_error_log):
        register_plugin()
        # NOTE(thenakliman): Register the same plugin multiple times
        register_plugin()
        fake_jaanch = get_fake_jaanch()
        fake_jaanch['jaanch']['raise_exception'] = True
        base.output(**fake_jaanch)
        mock_error_log.assert_called()

    @mock.patch.object(base.LOG, 'info')
    def test_output_if_plugin_run_sucessfully(self, mock_info_log):
        register_plugin()
        fake_jaanch = get_fake_jaanch()
        exp_jaanch = copy.deepcopy(fake_jaanch)
        exp_jaanch['jaanch']['test_result'] = 'pass'
        self.assertDictEqual(exp_jaanch, base.output(**fake_jaanch))
        mock_info_log.assert_called()


class TestMakeOutputDict(unittest.TestCase):
    def test_make_output_dict(self):
        fake_jaanch = get_fake_jaanch()
        exp_jaanch = base.make_output_dict('jaanch', 10,
                                           **copy.deepcopy(fake_jaanch))
        fake_jaanch['jaanch']['input'] = fake_jaanch['jaanch']['input']['args']
        fake_jaanch['jaanch']['output'] = {'expected_output': 10}
        self.assertDictEqual(exp_jaanch, fake_jaanch)

    def test_make_output_dict_from_succesful_worker_execution(self):
        fake_jaanch = get_fake_jaanch()
        fake_jaanch['jaanch']['input']['result'] = 10
        exp_jaanch = base.make_output_dict('jaanch', 10,
                                           **copy.deepcopy(fake_jaanch))
        fake_jaanch['jaanch']['input'] = fake_jaanch['jaanch']['input']['args']
        fake_jaanch['jaanch']['output'] = {
            'expected_output': 10,
            'actual_output': 10
        }
        self.assertDictEqual(exp_jaanch, fake_jaanch)

    def test_make_output_dict_if_args_not_available(self):
        fake_jaanch = get_fake_jaanch()
        del fake_jaanch['jaanch']['input']
        exp_jaanch = base.make_output_dict('jaanch', 10,
                                           **copy.deepcopy(fake_jaanch))
        fake_jaanch['jaanch']['output'] = {'expected_output': 10}
        self.assertDictEqual(exp_jaanch, fake_jaanch)
