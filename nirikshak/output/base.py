from abc import ABCMeta, abstractmethod
import logging
import os
import six

import nirikshak
from nirikshak.common import exceptions
from nirikshak.input import input

LOG = logging.getLogger(__name__)

OUTPUT_PLUGIN_MAPPER = {}


def register(output):
    def register_output(cls):
        global OUTPUT_PLUGIN_MAPPER

        if output in OUTPUT_PLUGIN_MAPPER:
            LOG.info("For %s output, plugin is already "
                     "registered" % output)
        else:
            OUTPUT_PLUGIN_MAPPER[output] = cls()

        return cls

    return register_output


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def output(**args):
        pass


def output(**kwargs):
    values = kwargs.values()[0]
    output = values['output'].get('type', 'console')
    plugin = OUTPUT_PLUGIN_MAPPER[output]
    soochis = getattr(plugin, 'output')(**kwargs)
    LOG.info("%s soochis has been returned by the plugin" % soochis)
    return soochis


def make_output_dict(key, expected_result, **kwargs):
    if expected_result:
        output = {
            'actual_output': kwargs[key]['input']['result'],
            'expected_output': expected_result
        }

    else:
        output = {'actual_output': kwargs[key]['input']['result']}

    jaanch = {
        key: {
                'input': kwargs[key]['input']['args'],
                'output': output
            }
        }

    return jaanch