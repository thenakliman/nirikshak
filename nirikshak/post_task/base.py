from abc import ABCMeta, abstractmethod
import logging
import os
import six

import nirikshak
from nirikshak.common import exceptions
from nirikshak.input import input

POST_TASK_PLUGIN_MAPPER = {}


def register(post_task):
    def register_post_task(cls):
        global POST_TASK_PLUGIN_MAPPER

        if post_task in POST_TASK_PLUGIN_MAPPER:
            logging.info("For %s post task, plugin is already "
                         "registered" % post_task)
        else:
            POST_TASK_PLUGIN_MAPPER[post_task] = cls()

        return cls

    return register_post_task


@six.add_metaclass(ABCMeta)
class FormatOutput(object):

    @abstractmethod
    def format_output(**args):
        pass


def format_for_output(**kwargs):
    values = kwargs.values()[0]
    post_task = values['input'].get('post_task', 'dummy')
    plugin = POST_TASK_PLUGIN_MAPPER[post_task]
    soochis = getattr(plugin, 'format_output')(**kwargs)
    logging.info("%s soochis has been returned by the plugin" % soochis)
    return soochis
