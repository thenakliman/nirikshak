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
import ping

from nirikshak.workers import base
from nirikshak.common import plugins

LOG = logging.getLogger(__name__)


@plugins.register("network_connectivity")
class Connectivity(base.Worker):
    @base.match_expected_output
    @base.validate(required=("host",))
    def work(self, **kwargs):
        host = kwargs["input"]["args"]["host"]
        # If ping packet loss is 100% then there is no connectivity
        if ping.quiet_ping(host)[0] == 100:
            LOG.info("Failed to connect to %s host", host)
            return False

        LOG.info("Connected to %s host", host)
        return True
