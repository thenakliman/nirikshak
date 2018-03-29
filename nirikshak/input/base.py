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

from abc import ABCMeta, abstractmethod
import copy
import logging
import six

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.common import utils
from nirikshak.input import input as input_base

LOG = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class Input(input_base.Input):
    @staticmethod
    def _get_group_dependencies(group, main_file):
        gps = set()
        to_process = [group]
        for grp in to_process:
            if grp not in gps:
                gps.add(grp)
                if not main_file.get(grp, False):
                    raise exceptions.GroupNotFoundException(group=grp)
                try:
                    to_process += main_file[grp]['groups']
                except KeyError:
                    pass

        return gps

    def _get_groups(self, main_file, groups):
        gps = set()
        for group in groups:
            try:
                deps = self._get_group_dependencies(group, main_file)
            except exceptions.GroupNotFoundException:
                LOG.error("%s group could not be found", group)
            else:
                gps |= deps
                gps.add(group)

        LOG.info("%s groups are to be executed.", gps)
        return list(gps)

    @abstractmethod
    def get_yaml_file(self, location):
        pass

    @abstractmethod
    def get_soochi_content(self, soochi):
        pass

    @abstractmethod
    def get_main_file(self):
        pass

    @staticmethod
    def _get_config(configuration, group):
        return configuration[group].get('config', {})

    def _get_executable_soochis(self, soochis, groups):
        try:
            content = self.get_main_file()
        except exceptions.FileNotFound:
            LOG.error("main file could not found.")
            return []

        groups = self._get_groups(content, groups)

        soochis_name_with_config = {}
        for soochi in soochis:
            soochis_name_with_config[soochi] = {}

        group_config = {}
        for group in groups:
            group_config[group] = self._get_config(content, group)
            if 'soochis' in content[group]:
                for name, soochi_config in content[group]['soochis'].items():
                    config = copy.deepcopy(soochi_config.get('config', {}))
                    utils.merge_dict(config, group_config[group])
                    soochis_name_with_config[name] = config

        LOG.info("%s soochis to be executed.",
                 list(soochis_name_with_config.keys()))
        soochis_with_config = []
        for soochi, config in soochis_name_with_config.items():
            soochis_with_config.append({soochi: config})

        return soochis_with_config

    def get_soochis(self, soochis, groups):
        soochis_with_content_and_config = []
        soochis = self._get_executable_soochis(soochis, groups)
        for soochi in soochis:
            soochi_content = []
            soochi_name, soochi_config = soochi.items()[0]
            try:
                soochi_content = self.get_soochi_content(soochi_name)
            except exceptions.FileNotFound:
                LOG.error("%s file not found", soochi_name)
            except exceptions.InvalidFormatException:
                LOG.error("%s file has invalid format", soochi_name)
            else:
                soochis_with_content_and_config.append(
                    (soochi_config, soochi_content))

        return soochis_with_content_and_config


def get_soochis(soochis=None, groups=None):
    input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
    plugin = plugins.get_plugin(input_type)
    try:
        soochis = getattr(plugin, 'get_soochis')(soochis=soochis,
                                                 groups=groups)
    except Exception:
        LOG.error("Error in getting soochis from %s plugin", input_type)
        return []

    LOG.info("%s soochis has been returned by the plugin", soochis)
    return soochis
