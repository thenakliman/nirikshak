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


_PLUGINS = {}


def add_plugin(plugin_name, plugin):
    _PLUGINS[plugin_name] = plugin


def get_plugin(plugin_name):
    if plugin_name in _PLUGINS:
        return _PLUGINS[plugin_name]()

    return None


def register(plugin_name):
    def save_plugin(cls):
        add_plugin(plugin_name, cls)
        return cls

    return save_plugin
