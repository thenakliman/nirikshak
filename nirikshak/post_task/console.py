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

    def format_output(self, **args):
        name = args.keys()[0]
        v = args[name]
        inpt = ''
        for key, value in v['input']['args'].items():
            inpt = ("%s%s:%s," % (inpt, key, value))

        type_ = v['type']

        result = ''
        if 'result' in args:
            if str(v['args']['result']) == str(args['result']):
                result = 'pass'
            else:
                result = 'fail'

        if not result:
            result = v['input']['result']

        rs = ("%s,%s,%s" % (name, type_, inpt))
        rs = ("%s%s%s" % (rs, (120 - len(rs)) * '.', result))
        args[name]['formatted_output'] = rs
        LOG.info("Output has been formaated for console")
        return args
