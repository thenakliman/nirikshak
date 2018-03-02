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

import mock
import unittest

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import validators


class ConfigValidatorTest(unittest.TestCase):
    def setUp(self):
        super(ConfigValidatorTest, self).setUp()
        nirikshak.CONF = {
            'default': {
                'key1': 'value1',
                'key2': 'value2'
            }
        }

    def tearDown(self):
        super(ConfigValidatorTest, self).tearDown()
        del nirikshak.CONF

    def _get_dummy_object(self, section, config_opts):
        class DummyClass(object):
            @validators.config_validator(section, config_opts)
            def dummy_method(self, **kwargs):
                return kwargs

        return DummyClass()

    def test_validate_for_invalid_section(self):
        dummy_object = self._get_dummy_object('default1', [])
        with mock.patch.object(validators, 'LOG'):
            self.assertRaises(exceptions.SectionNotFoundException,
                              dummy_object.dummy_method)

    def test_validate_for_invalid_config_options(self):
        dummy_object = self._get_dummy_object('default', ['invalid_opts'])
        with mock.patch.object(validators, 'LOG'):
            self.assertRaises(exceptions.ConfigurationNotFoundException,
                              dummy_object.dummy_method)

    def test_validate_for_validate(self):
        dummy_object = self._get_dummy_object('default', ['key1'])
        with mock.patch.object(validators, 'LOG'):
            self.assertEqual({'key': 'value'},
                             dummy_object.dummy_method(key='value'))
