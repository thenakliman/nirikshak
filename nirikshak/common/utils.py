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

from copy import deepcopy


def merge_dict(dict2, dict1):
    for k, v in dict1.iteritems():
        if dict2.get(k):
            if isinstance(dict2[k], dict):
                merge_dict(dict2[k], dict1[k])
        else:
            dict2[k] = deepcopy(v)
