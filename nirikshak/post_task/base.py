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

POST_TASK_PLUGIN_MAPPER = {}


def register(post_task):
    def register_post_task(cls):
        global POST_TASK_PLUGIN_MAPPER

        if post_task in POST_TASK_PLUGIN_MAPPER:
            LOG.info("For %s post task, plugin is already "
                     "registered", post_task)
        else:
            POST_TASK_PLUGIN_MAPPER[post_task] = cls()

        return cls

    return register_post_task


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def format_output(self, **kwargs):
        pass


def format_for_output(**kwargs):
    values = kwargs.values()[0]
    # fixme(thenakliman) It is a workaround to avoid the situation
    # where both output and post task are not defined. Some
    # standard way can be developed to avoid this workaround

    if values.get('output', {}).get('type', 'console') == 'console':
        post_task = values.get('post_task', 'console')
    else:
        post_task = values.get('post_task', 'dummy')

    try:
        plugin = POST_TASK_PLUGIN_MAPPER[post_task]
    except KeyError:
        LOG.error("%s plugin for task could not be found", post_task)
        return kwargs

    try:
        soochis = getattr(plugin, 'format_output')(**kwargs)
    except Exception:
        LOG.error("Error in formatting %s jaanch for %s post_task",
                  kwargs.keys()[0], post_task, exc_info=True)
    else:
        LOG.info("%s jaanch has been formatter by %s plugin",
                 kwargs.keys()[0], post_task)

    return soochis
