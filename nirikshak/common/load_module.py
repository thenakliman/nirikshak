import logging

LOG = logging.getLogger(__name__)


def load(modname):
    try:
        module = __import__(modname, globals(), locals(), [modname], -1)
    except ImportError:
        LOG.error('Unable to load module at %s' % modname)
        raise ImportError

    return module
