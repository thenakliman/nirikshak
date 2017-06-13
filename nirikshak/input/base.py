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
from copy import deepcopy
import logging
import six

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import utils
from nirikshak.input import input

LOG = logging.getLogger(__name__)

INPUT_PLUGIN_MAPPER = {}


def register(input_type):
    def register_input(cls):
        global INPUT_PLUGIN_MAPPER

        if input_type in INPUT_PLUGIN_MAPPER:
            LOG.info("For %s input type, plugin is already "
                     "registered" % input_type)

        INPUT_PLUGIN_MAPPER[input_type] = cls()
        return cls

    return register_input


@six.add_metaclass(ABCMeta)
class Input(input.Input):
    def __init__(self):
        pass

    def _get_group_dependencies(self, group, main_file):
        gps = set()
        to_process = [group]
        for gp in to_process:
            if gp not in gps:
                gps.add(gp)
                if not main_file.get(gp, False):
                    raise exceptions.GroupNotFoundException(group=gp)
                try:
                    to_process += main_file[gp]['groups']
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

        LOG.info("%s groups are to be executed." % gps)
        return list(gps)

    @abstractmethod
    def get_yaml_file(self):
        pass

    @abstractmethod
    def get_soochi_content(self, soochi):
        pass

    @staticmethod
    def _get_config(configuration, group):
        return configuration[group].get('config', {})

    @classmethod
    def _merge_config(cls, group_config, soochi_config):
        config = {}
        for k, v in group_config.iteritems():
            if soochi_config.get(k):
                if isinstance(soochi_config[k], dict):
                    config[k] = cls._merge_config(group_config[k],
                                                  soochi_config[k])
                else:
                    config[k] = v
            else:
                config[k] = deepcopy(v)

        return config

    def _get_executable_soochis(self, soochis, groups):
        group_config = {}
        content = self.get_yaml_file(self.main_file)
        groups = self._get_groups(content, groups)

        s = {}
        for soochi in soochis:
            s[soochi] = {
                'soochi': soochi,
                'config': {}
            }

        for group in groups:
            group_config[group] = self._get_config(content, group)
            if 'soochis' in content[group]:
                for name, soochi_def in content[group]['soochis'].iteritems():
                    config = deepcopy(soochi_def.get('config', {}))
                    utils.merge_dict(config, group_config[group])
                    s[name] = {'config': config}

        LOG.info("%s soochis to be executed." % s)
        soochis_with_config = []
        for soochi, config in s.iteritems():
            soochis_with_config.append({soochi: config})
        return soochis_with_config

    def get_soochis(self, soochis, groups):
        s = []
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
                s.append(soochi)

        return s


def get_soochis(soochis=[], groups=[]):
    input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
    try:
        plugin = INPUT_PLUGIN_MAPPER[input_type]
    except KeyError:
        LOG.error("%s plugin for input could not found", input_type)
        return []

    soochis = getattr(plugin, 'get_soochis')(soochis=soochis, groups=groups)
    LOG.info("%s soochis has been returned by the plugin" % soochis)
    return soochis
