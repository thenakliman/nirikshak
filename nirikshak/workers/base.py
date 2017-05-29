from abc import ABCMeta
from abc import abstractmethod
import logging
import six

from nirikshak.common import exceptions

LOG = logging.getLogger(__name__)

WORKER_PLUGIN_MAPPER = {}


def register(worker):
    def register_worker(cls):
        global WORKER_PLUGIN_MAPPER

        if worker in WORKER_PLUGIN_MAPPER:
            LOG.info("For %s worker type, plugin is already "
                     "registered" % worker)

        WORKER_PLUGIN_MAPPER[worker] = cls()
        return cls

    return register_worker


def validate(required=(), optional=()):
    def func(f):
        def validator(self, **kwargs):
            require = set(required)
            try:
                available = set(kwargs['input']['args'].keys())
            except KeyError:
                available = set()

            missing = require - available
            if missing:
                raise excpetions.MissingRquiredArgException(jaanch=missing)

            require.update(set(optional))
            extra = available - require
            if extra:
                raise exceptions.ExtraArgException(params=[list(extra)])

            return f(self, **kwargs)
        return validator
    return func


class Worker(object):
    @abstractmethod
    def work(self, **kwargs):
        pass


def match_expected_output(validator):
    def convert_output(self, **kwargs):
        tmp = validator(self, **kwargs)
        if 'result' in kwargs['output']:
            tmp = (tmp == kwargs['output']['result'])

        kwargs['input']['result'] = tmp
        return kwargs

    return convert_output


def do_work(**kwargs):
    key = kwargs.keys()[0]
    kwargs = kwargs[key]
    worker = kwargs['type']
    plugin = WORKER_PLUGIN_MAPPER[worker]
    result = getattr(plugin, 'work')(**kwargs)
    LOG.info("%s jaanch has been completed by the plugin" % key)
    return result