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

import unittest

from nirikshak.common import utils

class TestUtil(unittest.TestCase):
    def _test_dict_merge(self, dict1, dict2, exp_dict):
        utils.merge_dict(dict1, dict2)
        self.assertDictEqual(dict1, exp_dict)

    def test_merge_one_empty_one_nonempty(self):
        dict1 = {}
        dict2 = {1: 3, 2: 'r'}
        exp_dict = {1: 3, 2: 'r'}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_both_non_empty(self):
        dict1 = {'a': 2, 'b': 3}
        dict2 = {'c': 1}
        exp_dict = {'a': 2, 'b': 3, 'c': 1}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_one_nested_dict(self):
        dict1 = {'a': 2, 'b': 3, 'd': {'e': 1}}
        dict2 = {'c': 1}
        exp_dict = {'a': 2, 'b': 3, 'c': 1, 'd': {'e': 1}}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_two_nested_non_overlapping_key_dicts(self):
        dict1 = {'a': 2, 'd': {'e': 1}}
        dict2 = {'c': 1, 'f': {'g': 2}, 'h': [1, 2]}
        exp_dict = {'a': 2, 'c': 1, 'h': [1, 2], 'd': {'e': 1}, 'f': {'g': 2}}
        self._test_dict_merge(dict1, dict2, exp_dict)

    def test_merge_two_nested_overlapping_key_dicts(self):
        dict1 = {
            'a': 2,
            'd': {
                'e': 1,
                'k': {
                    'l': [2, 3]
                }
            }
        }
        dict2 = {
            'c': 1,
            'd': {
                'g': 2,
                'k': {
                    'm': {'n': 2}
                }
            },
            'h': [1, 2]
        }
        exp_dict = {
            'a': 2,
            'c': 1,
            'h': [1, 2],
            'd': {
                'e': 1,
                'g': 2,
                'k': {
                    'l': [2, 3],
                    'm': {'n':2}
                }
            }
        }
        self._test_dict_merge(dict1, dict2, exp_dict)
