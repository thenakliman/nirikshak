# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at #
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import psutil

from nirikshak.common import plugins
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@plugins.register('process_running')
class RunningProcessWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('name',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        name = k['name']
        for proc in psutil.process_iter():
            try:
                if proc.name() == name:
                    LOG.info("%s process is running", name)
                    return True
            except psutil.NoSuchProcess:
                pass

        LOG.info("%s process is not running", name)
        return False
