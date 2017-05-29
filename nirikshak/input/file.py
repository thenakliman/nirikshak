import logging
import os

import nirikshak
from nirikshak.common import yaml_util
from nirikshak.common import validators
from nirikshak.input import base

LOG = logging.getLogger(__name__)

INPUT_TYPE_NAME = 'input_file'


@validators.config_validator(INPUT_TYPE_NAME, ('main_file',))
@base.register(INPUT_TYPE_NAME)
class InputFile(base.Input):
    def __init__(self):
        # TODO(thenakliman): Unable to find InputFile in global variables
        # Fix this error
        # super(InputFile, self).__init__()
        try:
            self.main_file = nirikshak.CONF[INPUT_TYPE_NAME]['main_file']
        except KeyError:
            raise exceptions.ConfigurationNotFound(option='main_file',
                                                   section='input_file')

        LOG.info("Main file location is %s" % self.main_file)

    def _get_soochi_dir(self):
        return os.path.dirname(self.main_file)

    def get_soochi_content(self, soochi):
        directory = self._get_soochi_dir()
        location = ("%s/%s.yaml" % (directory, soochi))
        return yaml_util.get_yaml(location)

    def get_yaml_file(self, location):
        try:
            content = yaml_util.get_yaml(location)
        except exceptions.FileNotFound:
            raise exceptions.FileNotFound(location=self.main_file)

        LOG.info("%s content of the main file" % content)
        return content
