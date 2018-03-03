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


def add_plugin(plugin_name, plugin):
    POST_TASK_PLUGIN_MAPPER[plugin_name] = plugin()


def get_plugin(plugin_name):
    return POST_TASK_PLUGIN_MAPPER.get(plugin_name)


def register(post_task):
    def register_post_task(cls):
        if get_plugin(post_task) is None:
            add_plugin(post_task, cls)
        else:
            LOG.info("For %s post task, plugin is already "
                     "registered", post_task)

        return cls

    return register_post_task


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def format_output(self, **kwargs):
        pass


def format_for_output(**kwargs):
    values = list(kwargs.values())[0]
    if values.get('post_task', 'console') == 'console':
        post_task = values.get('post_task', 'console')
    else:
        post_task = values.get('post_task', 'dummy')

    plugin = get_plugin(post_task)
    soochis = None
    try:
        soochis = getattr(plugin, 'format_output')(**kwargs)
    except AttributeError:
        LOG.error("%s plugin for task could not be found", post_task)
        return kwargs
    except Exception:
        LOG.error("Error in formatting %s jaanch for %s post_task",
                  list(kwargs.keys())[0], post_task, exc_info=True)
    else:
        LOG.info("%s jaanch has been formatter by %s plugin",
                 list(kwargs.keys())[0], post_task)

    return soochis
