from abc import ABCMeta, abstractmethod
import logging
import os
import six

import nirikshak
from nirikshak.common import exceptions
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
            deps = self._get_group_dependencies(group, main_file)
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

    def _get_executable_soochis(self, soochis, groups):
        content = self.get_yaml_file(self.main_file)
        groups = self._get_groups(content, groups)
        s = set(soochis)
        for group in groups:
            if 'soochis' in content[group]:
                s |= set(content[group]['soochis'].keys())

        LOG.info("%s soochis to be executed." % s)
        return list(s)

    def get_soochis(self, soochis, groups):
        s = []
        soochis = self._get_executable_soochis(soochis, groups)
        for soochi in soochis:
            s.append(self.get_soochi_content(soochi))

        return s


def get_soochis(soochis=[], groups=[]):
    input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
    plugin = INPUT_PLUGIN_MAPPER[input_type]
    soochis = getattr(plugin, 'get_soochis')(soochis=soochis, groups=groups)
    LOG.info("%s soochis has been returned by the plugin" % soochis)
    return soochis
