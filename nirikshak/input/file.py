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

import logging
import os

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.common import yaml_util
from nirikshak.input import base

LOG = logging.getLogger(__name__)

INPUT_TYPE_NAME = 'input_file'


@plugins.register(INPUT_TYPE_NAME)
class InputFile(base.Input):
    @property
    def main_file(self):
        try:
            return nirikshak.CONF[INPUT_TYPE_NAME]['main_file']
        except KeyError:
            raise exceptions.ConfigurationNotFoundException(
                option='main_file',
                section='input_file')

    def _get_soochi_dir(self):
        return os.path.dirname(self.main_file)

    def get_soochi_content(self, soochi):
        directory = self._get_soochi_dir()
        location = ("%s/%s.yaml" % (directory, soochi))
        return self.get_yaml_file(location)

    def get_main_file(self):
        return self.get_yaml_file(self.main_file)

    def get_yaml_file(self, location):
        try:
            content = yaml_util.get_yaml(location)
        except exceptions.FileNotFound:
            raise exceptions.FileNotFound(location=self.main_file)

        LOG.info("%s content of the main file", content)
        return content
