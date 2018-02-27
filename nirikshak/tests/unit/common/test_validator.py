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

    def _get_decorated_method(self, section, config_opts):
        @validators.config_validator(section, config_opts)
        def dummy_method(self, **kwargs):
            return kwargs

        return dummy_method

    def test_validate_for_invalid_section(self):
        with mock.patch.object(validators, 'LOG'):
            self.assertRaises(exceptions.SectionNotFoundException,
                              self._get_decorated_method,
                              'default1', [])

    def test_validate_for_invalid_config_options(self):
        with mock.patch.object(validators, 'LOG'):
            self.assertRaises(exceptions.ConfigurationNotFoundException,
                              self._get_decorated_method,
                              'default', ['invalid_opts'])

    def test_validate_for_validate(self):
        with mock.patch.object(validators, 'LOG'):
            dummy_method = self._get_decorated_method('default', ['key1'])
            self.assertEqual({'key': 'value'}, dummy_method(self, key='value'))
