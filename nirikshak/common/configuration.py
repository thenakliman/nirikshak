import logging
import ConfigParser

import nirikshak

nirikshak.CONF = None


def make_dict(config):
    dict1 = {}
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        dict2 = {}
        for option in options:
            try:
                dict2[option] = config.get(section, option)
            except:
                dict2[option] = None

        dict1[section] = dict2

    return dict1


def initilize_config(config_file=None):
    if not config_file:
        config_file = '/etc/nirikshak/nirikshak.conf'

    config = ConfigParser.ConfigParser()
    try:
        config.read(config_file)
    except:
        print("Unable to load configuration file at %s." % config_file)

    nirikshak.CONF = make_dict(config)


def initilize_logging():
    """Initilization of logging module."""

    if not nirikshak.CONF['default'].get('log_file', False):
        nirikshak.CONF['default']['log_file'] = '/var/log/nirikshak.log'

    log_level = nirikshak.CONF['default'].get('log_level', 'info')
    formatter = ("%(asctime)s %(levelname)s %(name)s %(funcName)s():%(lineno)s"
                 " PID:%(process)d %(message)s")

    logging.basicConfig(filename=nirikshak.CONF['default']['log_file'],
                        level=getattr(logging, log_level.upper()),
                        format=formatter)

    logging.info("Logging module loaded successfully")
