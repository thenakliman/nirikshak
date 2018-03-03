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

import nirikshak
from nirikshak.common import exceptions

LOG = logging.getLogger(__name__)


def config_validator(section, config_opts=()):
    def validate():
        if section not in nirikshak.CONF:
            LOG.error("%s section could not be found in "
                      "configuration file", section)

            raise exceptions.SectionNotFoundException(section=section)

        for opt in config_opts:
            if opt not in nirikshak.CONF[section]:
                LOG.error("%s configuration option could not be "
                          "found in %s section.", opt, section)

                raise exceptions.ConfigurationNotFoundException(
                    section=section, option=opt)

    def func(function):
        def inject_validation(self, **kwargs):
            validate()
            return function(self, **kwargs)

        return inject_validation

    return func
