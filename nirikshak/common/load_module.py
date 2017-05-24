import logging


def load(modname):
    try:
        module = __import__(modname, globals(), locals(), [modname], -1)
    except ImportError:
        logging.error('Unable to load module at %s' % modname)
        raise ImportError

    return module
