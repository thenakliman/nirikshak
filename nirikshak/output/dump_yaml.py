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
import yaml

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.common import yaml_util
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@plugins.register('yaml')
class YAMLFormatOutput(base.FormatOutput):

    @staticmethod
    def read_file(f_name):
        try:
            if os.stat(f_name).st_size:
                output_file = yaml_util.get_yaml(f_name)
            else:
                output_file = {}
        except IOError:
            output_file = {}
        except exceptions.FileNotFound:
            output_file = {}
        except Exception:
            output_file = {}

        return output_file

    @staticmethod
    def _write_file(output_file, f_name):
        with open(f_name, "w") as output:
            yaml.dump(output_file, output, default_flow_style=False)

    def output(self, **kwargs):
        try:
            out_file = nirikshak.CONF['output_yaml']['output_dir']
        except KeyError:
            out_file = '/var/lib/nirikshak/result.yaml'

        output_file = self.read_file(out_file)
        try:
            expected_result = kwargs['output']['result']
        except KeyError:
            expected_result = None

        jaanch = base.make_output_dict(expected_result, **kwargs)
        if not output_file:
            output_file = [jaanch]
        else:
            output_file.append(jaanch)

        self._write_file(output_file, out_file)
        LOG.info("Output has been dumped in %s file", out_file)
