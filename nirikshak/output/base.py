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

from abc import ABCMeta, abstractmethod
import logging
import six

LOG = logging.getLogger(__name__)

OUTPUT_PLUGIN_MAPPER = {}


def register(plugin_name):
    def register_output(cls):
        global OUTPUT_PLUGIN_MAPPER

        if output in OUTPUT_PLUGIN_MAPPER:
            LOG.info("For %s output, plugin is already "
                     "registered", plugin_name)
        else:
            OUTPUT_PLUGIN_MAPPER[plugin_name] = cls()

        return cls

    return register_output


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def output(self, **kwargs):
        pass


def output(**kwargs):
    values = kwargs.values()[0]
    out = values.get('output', {}).get('type', 'console')

    try:
        plugin = OUTPUT_PLUGIN_MAPPER[out]
    except KeyError:
        LOG.error("%s plugin for output could not be found", out)
        return kwargs

    soochis = kwargs
    try:
        soochis = getattr(plugin, 'output')(**kwargs)
    except Exception:
        LOG.error("%s jaanch get failed for %s output.",
                  kwargs.keys()[0], out, exc_info=True)
    else:
        LOG.info("%s soochis has been returned by the plugin", soochis)

    return soochis


def make_output_dict(key, expected_result, **kwargs):
    try:
        if expected_result:
            out = {
                'actual_output': kwargs[key]['input']['result'],
                'expected_output': expected_result
            }

        else:
            out = {'actual_output': kwargs[key]['input']['result']}
    except KeyError:
        LOG.error("result key does not exist in the dictionary")
        out = None

    try:
        jaanch = {
            key: {
                'input': kwargs[key]['input']['args'],
                'output': out}
            }
    except KeyError:
        jaanch = {key: {'output': out}}

    return jaanch
