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
from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.common import utils
from nirikshak.input import base as input_base
from nirikshak.tests.unit import base


class InputFileTest(base.BaseTestCase):
    def setUp(self):
        base.create_conf()
        utils.load_modules_from_location(
            [os.path.dirname(input_base.__file__)])

        super(InputFileTest, self).setUp()

    def tearDown(self):
        super(InputFileTest, self).tearDown()
        nirikshak.CONF.clear()

    @staticmethod
    def match_soochi_format(soochis):
        result = []
        for soochi in soochis:
            result.append(({}, soochi))

        return result

    @staticmethod
    def mock_get_yaml(yaml_file):
        if 'main' in yaml_file:
            return base.get_main_yaml()
        elif 'test_keystone' in yaml_file:
            return base.get_test_keystone_soochi()
        elif 'test_glance' in yaml_file:
            return base.get_test_glance_soochi()

        # fixme(thenakliman): Correct it
        return ''

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_keystone(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=['test_keystone'], groups=[])
        exp_output = [base.get_test_keystone_soochi()]
        expected_output = self.match_soochi_format(exp_output)
        self.assertEqual(soochis, expected_output)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_glance(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=['test_glance'], groups=[])
        exp_output = [base.get_test_glance_soochi()]
        expected_output = self.match_soochi_format(exp_output)
        self.assertEqual(soochis, expected_output)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_both(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(
            soochis=['test_glance', 'test_keystone'],
            groups=[])

        exp_output = [base.get_test_keystone_soochi(),
                      base.get_test_glance_soochi()]
        expected_output = self.match_soochi_format(exp_output)
        for exp in expected_output:
            self.assertIn(exp, soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_with_group_monitor(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])

        for _, soochi in soochis:
            self.assertIn(soochi, [base.get_test_keystone_soochi(),
                                   base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_with_group(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['deployment'])

        for _, soochi in soochis:
            self.assertIn(soochi, [base.get_test_keystone_soochi(),
                                   base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_two_group(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor', 'deployment'])

        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        for _, soochi in soochis:
            self.assertIn(soochi, exp_soochis)

        self.assertEqual(len(soochis), len(exp_soochis))
        self.assertEqual(get_yaml.call_count, 3)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_invalid_jaanch(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor', 'deployment'])

        exp_soochis = [base.get_test_keystone_soochi()]
        tmp = base.get_test_glance_soochi()
        tmp.pop(0)
        exp_soochis.append(tmp)

        for _, soochi in soochis:
            if soochi[0]['name'] == 'port_9292':
                soochi.pop(0)

            self.assertIn(soochi, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_soochi_group(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t_soochis = base.get_main_yaml()
                del t_soochis['monitor']['soochis']['test_keystone']
                del t_soochis['monitor']['groups']
                return t_soochis

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=['test_keystone'],
                                         groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        for _, soochi in soochis:
            self.assertIn(soochi, exp_soochis)

        self.assertEqual(len(soochis), len(exp_soochis))

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_with_no_input(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t_soochis = base.get_main_yaml()
                del t_soochis['monitor']['soochis']['test_keystone']
                del t_soochis['monitor']['groups']
                return t_soochis

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])
        exp_soochis = self.match_soochi_format([base.get_test_glance_soochi()])
        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_soochis_no_soochi_groups(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t_soochis = base.get_main_yaml()
                del t_soochis['monitor']['soochis']['test_keystone']
                del t_soochis['deployment']['soochis']['test_keystone']
                return t_soochis

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])
        exp_soochis = [base.get_test_glance_soochi()]
        exp_soochis = self.match_soochi_format(exp_soochis)
        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_with_all_soochi_groups(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t_soochis = base.get_main_yaml()
                del t_soochis['monitor']['soochis']['test_keystone']
                del t_soochis['deployment']['soochis']['test_glance']
                return t_soochis

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        expected_output = self.match_soochi_format(exp_soochis)
        for soochi in expected_output:
            self.assertIn(soochi, soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_with_no_soochi_groups_(self, get_yaml):
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])
        get_yaml.assert_called_once()
        self.assertEqual(soochis, [])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_with_invalid_soochi(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t_soochis = base.get_main_yaml()
                t_soochis['monitor']['soochis']['test_soochi'] = {
                    'soochi': 'test_soochi'}

                return t_soochis

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=[],
                                         groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        for soochi in exp_soochis:
            self.assertIn(({}, soochi), soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_with_invalid_groups(self, get_yaml):
        def get_yaml_file(location):
            t_soochis = base.get_main_yaml()
            t_soochis['monitor']['groups'] = ['test_group']
            return t_soochis

        get_yaml.side_effect = get_yaml_file
        soochis = input_base.get_soochis(soochis=[], groups=['monitor'])

        self.assertEqual([], soochis)

    @staticmethod
    def _get_fake_plugin():
        @plugins.register('input_file')
        class FakePlugin(input_base.Input):
            def get_main_file(self):
                pass

            def get_soochi_content(self, soochi):
                pass

            def get_yaml_file(self):
                pass

        return FakePlugin

    def test_soochi_with_error(self):
        self._get_fake_plugin()

        self.assertEqual([], input_base.get_soochis())

    def test_get_soochi_file_not_found(self):

        def get_main_file(self):
            raise exceptions.FileNotFound

        fake_plugin = self._get_fake_plugin()
        fake_plugin.get_main_file = get_main_file

        self.assertEqual([], input_base.get_soochis())

    def test_get_soochi_file_failed(self):
        fake_plugin = self._get_fake_plugin()

        def get_soochi_content(self, soochi):
            raise exceptions.FileNotFound

        def _get_executable_soochis(self, soochis, group):
            return [{'name': {}}]

        fake_plugin.get_soochi_content = get_soochi_content
        fake_plugin._get_executable_soochis = _get_executable_soochis

        self.assertEqual([], input_base.get_soochis())

    def test_get_invalid_soochi_file_failed(self):
        fake_plugin = self._get_fake_plugin()

        def get_soochi_content(self, soochi):
            raise exceptions.InvalidFormatException

        def _get_executable_soochis(self, soochis, group):
            return [{'name': {}}]

        fake_plugin.get_soochi_content = get_soochi_content
        fake_plugin._get_executable_soochis = _get_executable_soochis

        self.assertEqual([], input_base.get_soochis())
