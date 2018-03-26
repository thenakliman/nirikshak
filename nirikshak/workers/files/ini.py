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
try:
    import configparser
except ImportError:                        # pragma: no cover
    import ConfigParser as configparser

from nirikshak.common import plugins
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@plugins.register('ini')
class INIConfigValidatorWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('file', 'section', 'key'))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        config = configparser.ConfigParser()
        config.read(k['file'])
        value = None
        try:
            value = config.get(k['section'], k['key'])
            LOG.info("%s configuration option found in %s section",
                     k['section'], k['key'])
        except Exception:
            LOG.error("Not able to find %s configuration parameter in %s "
                      "section", k['key'], k['section'], exc_info=True)

        return value
