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

from nirikshak.post_task import base

LOG = logging.getLogger(__name__)


@base.register('console')
class FormatOutputConsole(base.FormatOutput):
    @staticmethod
    def _get_jaanch_result(jaanch_parameter):
        jaanch_result = ''
        if 'result' in jaanch_parameter['output']:
            if str(jaanch_parameter['output']['result']) == str(jaanch_parameter['input']['result']):
                return 'pass'
            else:
                return 'fail'

        if jaanch_result == '':
            return jaanch_parameter['input']['result']

    def format_output(self, **kwargs):
        jaanch_name = list(kwargs.keys())[0]
        jaanch_parameter = kwargs[jaanch_name]
        input_parameter = ''
        for key, value in jaanch_parameter['input']['args'].items():
            input_parameter = ("%s%s:%s," % (input_parameter, key, value))

        jaanch_result = self._get_jaanch_result(jaanch_parameter)
        jaanch_type = jaanch_parameter['type']
        jaanch_name_type_param = ("%s,%s,%s" % (jaanch_name, jaanch_type, input_parameter))
        formatted_output = ("%s%s%s" % (jaanch_name_type_param,
                                        (120 - len(jaanch_name_type_param)) * '.',
                                        jaanch_result))
        jaanch_parameter['formatted_output'] = formatted_output
        LOG.info("%s output has been formatted for console", formatted_output)
        return kwargs
