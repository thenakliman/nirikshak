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

from nirikshak.common import plugins

FAKE_PLUGIN_NAME = 'fake_plugin'


def register_plugin(plugin_name):
    @plugins.register(plugin_name)
    class DummyPlugin(object):
        name = plugin_name

    return DummyPlugin


class TestPlugin(unittest.TestCase):
    def tearDown(self):
        super(TestPlugin, self).tearDown()
        plugins._PLUGINS.clear()

    def test_plugin_registered(self):
        register_plugin(FAKE_PLUGIN_NAME)
        self.assertEqual(plugins.get_plugin(FAKE_PLUGIN_NAME).name,
                         FAKE_PLUGIN_NAME)

    def test_get_unregistered_plugin(self):
        self.assertIsNone(plugins.get_plugin(FAKE_PLUGIN_NAME))

    def test_register_same_method_two_time(self):
        register_plugin(FAKE_PLUGIN_NAME)

        @plugins.register('fake_plugin')
        class FakePlugin(object):
            name = 'fake_plugin2'

        self.assertEqual(plugins.get_plugin(FAKE_PLUGIN_NAME).name,
                         'fake_plugin2')

    def test_the_same_plugin_object_is_returned(self):
        dummy_plugin = register_plugin(FAKE_PLUGIN_NAME)
        self.assertTrue(isinstance(plugins.get_plugin(FAKE_PLUGIN_NAME),
                                   dummy_plugin))
