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
from nirikshak.common import utils
from nirikshak.input import input as input_base

LOG = logging.getLogger(__name__)

INPUT_PLUGIN_MAPPER = {}


def register(input_type):
    def register_input(cls):
        global INPUT_PLUGIN_MAPPER

        if input_type in INPUT_PLUGIN_MAPPER:
            LOG.info("For %s input type, plugin is already "
                     "registered", input_type)

        INPUT_PLUGIN_MAPPER[input_type] = cls()
        return cls

    return register_input


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

    @classmethod
    def _merge_config(cls, group_config, soochi_config):
        config = {}
        for key, value in group_config.iteritems():
            if soochi_config.get(key):
                if isinstance(soochi_config[key], dict):
                    config[key] = cls._merge_config(group_config[key],
                                                    soochi_config[key])
                else:
                    config[key] = value
            else:
                config[key] = copy.deepcopy(value)

        return config

    def _get_executable_soochis(self, soochis, groups):
        group_config = {}

        try:
            content = self.get_main_file()
        except exceptions.FileNotFound:
            LOG.error("main file could not found.")
            return []

        groups = self._get_groups(content, groups)

        t_soochis = {}
        for soochi in soochis:
            t_soochis[soochi] = {
                'soochi': soochi,
                'config': {}
            }

        for group in groups:
            group_config[group] = self._get_config(content, group)
            if 'soochis' in content[group]:
                for name, soochi_def in content[group]['soochis'].iteritems():
                    config = copy.deepcopy(soochi_def.get('config', {}))
                    utils.merge_dict(config, group_config[group])
                    t_soochis[name] = {'config': config}

        LOG.info("%s soochis to be executed.", t_soochis)
        soochis_with_config = []
        for soochi, config in t_soochis.iteritems():
            soochis_with_config.append({soochi: config})
        return soochis_with_config

    def get_soochis(self, soochis, groups):
        t_soochis = []
        soochis = self._get_executable_soochis(soochis, groups)
        for soochi in soochis:
            name = soochi.keys()[0]
            soochi_content = []
            try:
                soochi_content = self.get_soochi_content(name)
            except exceptions.FileNotFound:
                LOG.error("%s file not found", name)
            except exceptions.InvalidFormatException:
                LOG.error("%s file has invalid format", name)
            else:
                soochi = (soochi[name]['config'], soochi_content)
                t_soochis.append(soochi)

        return t_soochis


def get_soochis(soochis=None, groups=None):
    input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
    try:
        plugin = INPUT_PLUGIN_MAPPER[input_type]
    except KeyError:
        LOG.error("%s plugin for input could not found", input_type)
        return []

    soochis = getattr(plugin, 'get_soochis')(soochis=soochis, groups=groups)
    LOG.info("%s soochis has been returned by the plugin", soochis)
    return soochis
