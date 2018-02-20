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

import copy
import pkgutil


def merge_dict(dict2, dict1):
    for key, value in dict1.iteritems():
        if dict2.get(key):
            if isinstance(dict2[key], dict):
                merge_dict(dict2[key], dict1[key])
        else:
            dict2[key] = copy.deepcopy(value)


def load_modules_from_location(location):
    for loader, name, _ in pkgutil.walk_packages(location):
        loader.find_module(name).load_module(name)
