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
import json
import os

import nirikshak
from nirikshak.common import plugins
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@plugins.register('json')
class JSONFormatOutput(base.FormatOutput):
    @staticmethod
    def get_output_file(f_name):
        try:
            if os.stat(f_name).st_size:
                with open(f_name, 'r') as output:
                    output_file = json.load(output)
            else:
                output_file = {}
        except OSError:
            output_file = {}
        except ValueError:
            LOG.error("Invalid json file, creating new file", exc_info=True)
            output_file = {}

        return output_file

    @staticmethod
    def _output_json(output_file, f_name):
        with open(f_name, "w") as output:
            str_ = json.dumps(output_file, indent=4,
                              sort_keys=True, separators=(',', ': '))
            output.write(str_)

    def output(self, **kwargs):
        try:
            out_file = nirikshak.CONF['output_json']['output_dir']
        except KeyError:
            out_file = '/var/lib/nirikshak/result.json'

        output_file = self.get_output_file(out_file)
        try:
            expected_result = kwargs['output']['result']
        except KeyError:
            expected_result = None

        jaanch = base.make_output_dict(expected_result, **kwargs)
        if not output_file:
            output_file = [jaanch]
        else:
            output_file.append(jaanch)

        self._output_json(output_file, out_file)
        LOG.info("Output has been dumped in %s", out_file)
