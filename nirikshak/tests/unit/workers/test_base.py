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
import copy

import unittest

from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.tests.unit import base
from nirikshak.workers import base as worker_base


class WorkBaseTest(unittest.TestCase):
    def setUp(self):
        super(WorkBaseTest, self).setUp()
        self.sample_jaanch = base.get_ini_jaanch()

    @property
    def jaanch(self):
        return copy.deepcopy(self.sample_jaanch)

    def test_if_type_not_defined(self):
        jaanch = self.jaanch
        del jaanch['type']
        self.assertDictEqual(jaanch, worker_base.do_work(**jaanch))

    @staticmethod
    def _register_plugin():
        @plugins.register('ini')
        class FakePlugin(object):
            pass

        return FakePlugin

    def test_plugin_fails(self):
        self._register_plugin()
        self.assertDictEqual(self.jaanch, worker_base.do_work(**self.jaanch))

    def test_do_work(self):
        fake_result = 'fake_result'

        def work(self, **kwargs):
            return fake_result

        self._register_plugin().work = work
        self.assertEqual(fake_result, worker_base.do_work(**self.jaanch))

    def test_does_not_match_expected_output(self):

        @worker_base.match_expected_output
        def work(self, **kwargs):
            return 10

        self._register_plugin().work = work
        exp_jaanch = self.jaanch
        exp_jaanch['input']['result'] = 10
        self.assertDictEqual(exp_jaanch, work('fake_worker', **self.jaanch))

    def test_match_expected_output(self):

        @worker_base.match_expected_output
        def work(self, **kwargs):
            return 10

        self._register_plugin().work = work
        exp_jaanch = self.jaanch
        jaanch = self.jaanch
        jaanch['output']['result'] = 10
        exp_jaanch['output']['result'] = 10
        exp_jaanch['input']['result'] = True

        self.assertDictEqual(exp_jaanch, work('fake_worker', **jaanch))

    def test_if_args_are_not_provided_at_all(self):
        @plugins.register('ini')
        class FakePlugin(object):
            @worker_base.validate(required=("abc"))
            def func(self, **kwargs):
                pass

        jaanch = self.jaanch
        del jaanch['input']
        self.assertRaises(exceptions.MissingRequiredArgsException,
                          FakePlugin().func, **jaanch)

    def test_if_args_are_not_required_for_a_jaanch(self):
        @plugins.register('ini')
        class FakePlugin(object):
            @worker_base.validate(required=tuple())
            def func(self, **kwargs):
                return 10

        jaanch = self.jaanch
        del jaanch['input']
        self.assertEqual(10, FakePlugin().func(**jaanch))

    def test_if_extra_args_are_provided(self):
        @plugins.register('ini')
        class FakePlugin(object):
            @worker_base.validate(required=())
            def func(self, **kwargs):
                pass

        self.assertRaises(exceptions.ExtraArgsException,
                          FakePlugin().func, **self.jaanch)
