import logging
import os

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import yaml_util
from nirikshak.input import input


class FileInput(input.Input):
    def __init__(self):
        try:
            self.main_file = nirikshak.CONF['input_file']['main_file']
        except KeyError:
            msg = ("main input file could not be found in configuration file, "
                   "input_file section")
            logging.error(msg)
            raise exceptions.ConfigurationNotFound(option='main_file',
                                                   section='input_file')

    @staticmethod
    def _get_yaml_file(location):
        try:
            content = yaml_util.get_yaml(location)
        except exceptions.FileNotFound:
            msg = ("File main.yaml not found at %s" % location)
            logging.error(msg)
            raise exceptions.FileNotFound(location=self.main_file)

        return content

    def _get_group_dependencies(self, group, main_yaml):
        gps = set()
        to_process = [group]
        for gp in to_process:
            if gp not in gps:
                gps.add(gp)
                if not main_yaml.get(gp, False):
                    raise exceptions.GroupNotFoundException(group=gp)
                try:
                    to_process += main_yaml[gp]['groups']
                except KeyError:
                    pass

        return gps

    def _get_groups(self, main_yaml, groups):
        gps = set()
        for group in groups:
            deps = self._get_group_dependencies(group, main_yaml)
            gps |= deps
            gps.add(group)

        logging.info("%s groups are to be executed." % gps)
        return list(gps)

    def _get_executable_soochis(self, soochis, groups):
        content = self._get_yaml_file(self.main_file)
        groups = self._get_groups(content, groups)
        s = set(soochis)
        for group in groups:
            if 'soochis' in content[group]:
                s |= set(content[group]['soochis'].keys())

        logging.info("%s soochis to be executed." % s)
        return list(s)

    def _get_soochi_dir(self):
        return os.path.dirname(self.main_file)

    def _get_soochi_content(self, soochi):
        directory = self._get_soochi_dir()
        location = ("%s/%s.yaml" % (directory, soochi))
        return yaml_util.get_yaml(location)

    def get_soochis(self, soochis, groups):
        s = []
        soochis = self._get_executable_soochis(soochis, groups)
        for soochi in soochis:
            s.append(self._get_soochi_content(soochi))

        return s


def get_soochis(soochis=[], groups=[]):
    return FileInput().get_soochis(soochis, groups)
