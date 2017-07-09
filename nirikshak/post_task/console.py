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

    def format_output(self, **kwargs):
        name = kwargs.keys()[0]
        val = kwargs[name]
        inpt = ''
        for key, value in val['input']['args'].items():
            inpt = ("%s%s:%s," % (inpt, key, value))

        type_ = val['type']

        result = ''
        if 'result' in kwargs:
            if str(val['args']['result']) == str(kwargs['result']):
                result = 'pass'
            else:
                result = 'fail'

        if not result:
            result = val['input']['result']

        rslt = ("%s,%s,%s" % (name, type_, inpt))
        rslt = ("%s%s%s" % (rslt, (120 - len(rslt)) * '.', result))
        kwargs[name]['formatted_output'] = rslt
        LOG.info("%s output has been formatted for console", rslt)
        return kwargs
