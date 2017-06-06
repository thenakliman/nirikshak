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
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@base.register('json')
class JSONFormatOutput(base.FormatOutput):
    def output(self, **kwargs):
        try:
            f = nirikshak.CONF['output_json']['output_dir']
        except KeyError:
            f = '/var/nirikshak/result.json'

        try:
            if os.stat(f).st_size:
                with open(f, 'r') as output:
                    output_file = json.load(output)
            else:
                output_file = {}
        except OSError:
            output_file = {}

        key = kwargs.keys()[0]
        try:
            expected_result = kwargs[key]['output']['result']
        except KeyError:
            expected_result = None

        jaanch = base.make_output_dict(key, expected_result, **kwargs)
        if not output_file:
            output_file = jaanch
        else:
            output_file.update(jaanch)

        with open(f, "w") as output:
            str_ = json.dumps(output_file, indent=4,
                              sort_keys=True, separators=(',', ': '))
            output.write(str_)

        LOG.info("Output has been dumped in %s" % f)
        output.close()
