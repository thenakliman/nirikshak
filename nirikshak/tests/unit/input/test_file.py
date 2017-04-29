import mock

from nirikshak.input import file
from nirikshak.tests.unit import base


class InputFileTest(object):
    def __init__(self):
        pass

    def mock_get_yaml(yaml_file):
        if 'main_yaml' yaml_file:
            return base.get_main_yaml()
        else:
            return base.get_keystone_yaml()
        else:
            return base.get_glance_yaml()

    @patch('nirikshak.common.yaml_util')
    def test_get_soochis(self, yaml_util):
        yaml_util.get_yaml = mock.Mock()
        yaml_util.get_yaml.side_effect = return_yaml
        soochis = file.get_soochis(soochis=['deployment'])
        self.assert(
