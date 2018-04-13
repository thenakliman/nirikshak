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

from nirikshak.common import plugins


LOG = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def output(self, **kwargs):
        pass


def output(**jaanch_parameters):
    output_plugin = jaanch_parameters.get('output', {}).get('type', 'console')

    # NOTE(thenakliman): if plugin is not registered then it returns kwargs
    plugin = plugins.get_plugin(output_plugin)
    soochis = jaanch_parameters
    try:
        soochis = getattr(plugin, 'output')(**jaanch_parameters)
    except Exception:
        LOG.error("%s jaanch get failed for %s output.",
                  jaanch_parameters['name'], output_plugin, exc_info=True)
    else:
        LOG.info("%s soochis has been returned by the plugin", soochis)

    return soochis


def make_output_dict(expected_result, **kwargs):
    output_dict = {}
    try:
        output_dict = {'actual_output': kwargs['input']['result']}
    except KeyError:
        LOG.error("result key does not exist in the dictionary")

    if expected_result is not None:
        output_dict['expected_output'] = expected_result

    jaanch = {}
    try:
        jaanch['input'] = kwargs['input']['args']
    except KeyError:
        pass

    jaanch['name'] = kwargs['name']
    jaanch['output'] = output_dict or None
    return jaanch
