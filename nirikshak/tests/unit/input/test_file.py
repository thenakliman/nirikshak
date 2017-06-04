import mock
import unittest

from nirikshak.common import configuration
from nirikshak.common import exceptions
from nirikshak.input import file
from nirikshak.tests.unit import base


class InputFileTest(unittest.TestCase):
    def setUp(self):
        base.create_conf()
        configuration.initilize_config()
        configuration.initilize_logging()
        super(InputFileTest, self).setUp()

    @staticmethod
    def mock_get_yaml(yaml_file):
        if 'main' in yaml_file:
            return base.get_main_yaml()
        elif 'test_keystone' in yaml_file:
            return base.get_test_keystone_soochi()
        elif 'test_glance' in yaml_file:
            return base.get_test_glance_soochi()

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_keystone(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=['test_keystone'], groups=[])
        self.assertEqual(soochis, [base.get_test_keystone_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_glance(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=['test_glance'], groups=[])
        self.assertEqual(soochis, [base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_both(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=['test_glance', 'test_keystone'],
                                   groups=[])

        self.assertEqual(soochis, [base.get_test_keystone_soochi(),
                         base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_group_monitor(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])

        for soochi in soochis:
            self.assertIn(soochi, [base.get_test_keystone_soochi(),
                          base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_group_deployment(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=[],
                                   groups=['deployment'])

        for soochi in soochis:
            self.assertIn(soochi, [base.get_test_keystone_soochi(),
                          base.get_test_glance_soochi()])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_both_group(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor', 'deployment'])

        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        for soochi in soochis:
            self.assertIn(soochi, exp_soochis)

        self.assertEqual(len(soochis), len(exp_soochis))

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_delete_1_jaanch(self, get_yaml):
        get_yaml.side_effect = self.mock_get_yaml
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor', 'deployment'])

        exp_soochis = [base.get_test_keystone_soochi()]
        tmp = base.get_test_glance_soochi()
        del tmp['jaanches']['port_9292']
        exp_soochis.append(tmp)

        for soochi in soochis:
            if soochi['jaanches'].get('port_9292'):
                del soochi['jaanches']['port_9292']

            self.assertIn(soochi, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_soochi_group(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                del t['monitor']['soochis']['test_keystone']
                del t['monitor']['groups']
                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = file.get_soochis(soochis=['test_keystone'],
                                   groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        for soochi in soochis:
            self.assertIn(soochi, exp_soochis)

        self.assertEqual(len(soochis), len(exp_soochis))

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_no_soochi_group(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                del t['monitor']['soochis']['test_keystone']
                del t['monitor']['groups']
                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])
        exp_soochis = [base.get_test_glance_soochi()]
        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_no_soochi_groups(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                del t['monitor']['soochis']['test_keystone']
                del t['deployment']['soochis']['test_keystone']
                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])
        exp_soochis = [base.get_test_glance_soochi()]
        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_all_soochi_groups(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                del t['monitor']['soochis']['test_keystone']
                del t['deployment']['soochis']['test_glance']
                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi()]

        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_no_soochi_groups_(self, get_yaml):
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])
        self.assertEqual(soochis, [])

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_invalid_soochi(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                t['monitor']['soochis']['test_soochi'] = {
                    'soochi': 'test_soochi'}

                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        soochis = file.get_soochis(soochis=[],
                                   groups=['monitor'])
        exp_soochis = [base.get_test_keystone_soochi(),
                       base.get_test_glance_soochi(), None]

        self.assertEqual(soochis, exp_soochis)

    @mock.patch('nirikshak.common.yaml_util.get_yaml')
    def test_get_soochis_with_invalid_groups(self, get_yaml):
        def get_yaml_file(location):
            if 'main' in location:
                t = base.get_main_yaml()
                t['monitor']['groups'] = ['test_group']
                return t

            return self.mock_get_yaml(location)

        get_yaml.side_effect = get_yaml_file
        self.assertRaises(exceptions.GroupNotFoundException,
                          file.get_soochis, soochis=[],
                          groups=['monitor'])


unittest.main()
