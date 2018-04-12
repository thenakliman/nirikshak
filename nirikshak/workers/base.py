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

from abc import ABCMeta
from abc import abstractmethod
import copy
import logging
import six

from nirikshak.common import exceptions
from nirikshak.common import plugins

LOG = logging.getLogger(__name__)

WORKER_PLUGIN_MAPPER = {}


def validate(required=(), optional=()):
    def func(function):
        def validator(self, **kwargs):
            require = set(required)
            try:
                available = set(list(kwargs['input']['args'].keys()))
            except KeyError:
                available = set()
            except AttributeError:
                available = set()
            except Exception as e:
                print(e)
                available = set()


            missing = require - available
            if missing:
                raise exceptions.MissingRequiredArgsException(jaanch=missing)

            require.update(set(optional))
            extra = available - require
            if extra:
                raise exceptions.ExtraArgsException(params=[list(extra)])

            return function(self, **kwargs)
        return validator
    return func


@six.add_metaclass(ABCMeta)
class Worker(object):
    @abstractmethod
    def work(self, **kwargs):
        pass


def match_expected_output(validator):
    def convert_output(self, **kwargs):
        tmp = validator(self, **kwargs)
        if 'result' in kwargs.get('output', {}):
            tmp = (tmp == kwargs['output']['result'])

        kwargs['input']['result'] = tmp
        return kwargs

    return convert_output


def do_work(**kwargs):
    try:
        worker = kwargs['type']
    except KeyError:
        LOG.error("type for worker is not defined")
        return kwargs

    plugin = plugins.get_plugin(worker)
    result = copy.deepcopy(kwargs)
    try:
        result = getattr(plugin, 'work')(**kwargs)
    except Exception:
        LOG.error("%s worker failed", exc_info=True)
        return kwargs
    else:
        LOG.info("%s jaanch has been completed by the plugin", kwargs['name'])

    return result
