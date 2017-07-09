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
# pylint: disable=import-error
import apt

from nirikshak.common import constants
from nirikshak.common import synchronizer
from nirikshak.workers import base

LOG = logging.getLogger(__name__)

# pylint: disable=invalid-name
LOCK_NAME = 'APT'


@base.register('apt_install')
class APTWorker(base.Worker):

    @base.match_expected_output
    @base.validate(required=('package',))
    def work(self, **kwargs):
        k = kwargs['input']['args']
        LOCK_INDEX = getattr(constants.LOCKABLE_RESOURCES_INDEX, LOCK_NAME)
        LOG.info("Acquiring lock for %s jaanch", kwargs)
        with synchronizer.LOCK[LOCK_INDEX]:
            LOG.info("Acquired lock for %s jaanch", kwargs)
            cache = apt.cache.Cache()
            cache.update()
            pkg = cache[k['package']]
            status = pkg.is_installed

        LOG.info("Released lock for %s jaanch", kwargs)
        LOG.info("%s package is %s", k['package'], status)
        return status
