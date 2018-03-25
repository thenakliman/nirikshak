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
    def format_output(self, **kwargs):
        pass


def format_for_output(**kwargs):
    if kwargs.get('post_task', 'console') == 'console':
        post_task = kwargs.get('post_task', 'console')
    else:
        post_task = kwargs.get('post_task', 'dummy')

    plugin = plugins.get_plugin(post_task)
    soochis = None
    try:
        soochis = getattr(plugin, 'format_output')(**kwargs)
    except AttributeError:
        LOG.error("%s plugin for task could not be found", post_task)
        return kwargs
    except Exception:
        LOG.error("Error in formatting %s jaanch for %s post_task",
                  kwargs['name'], post_task, exc_info=True)
    else:
        LOG.info("%s jaanch has been formatter by %s plugin",
                 kwargs['name'], post_task)

    return soochis
