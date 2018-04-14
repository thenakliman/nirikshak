# Copyright 2018 <thenakliman@gmail.com>
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
import psutil

from nirikshak.common import plugins
from nirikshak.workers import base

LOG = logging.getLogger(__name__)


@plugins.register('cpu_usage')
class CPUUsage(base.Worker):
    @base.match_expected_output
    @base.validate(required=tuple())
    def work(self, **jaanch):
        cpu_percent = psutil.cpu_percent()
        LOG.info("CPU usage for %s jaanch is %d", jaanch['name'], cpu_percent)
        return cpu_percent
