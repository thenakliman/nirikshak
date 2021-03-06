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
import yaml

from nirikshak.common import exceptions

LOG = logging.getLogger(__name__)


def get_yaml(location):
    try:
        with open(location, 'r') as fid:
            try:
                content = yaml.load(fid)
            except yaml.scanner.ScannerError:
                raise exceptions.InvalidFormatException(location=location,
                                                        format='yaml')
    except IOError:
        raise exceptions.FileNotFound(location=location)

    return content
