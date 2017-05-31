import logging

import nirikshak
from nirikshak.common import exceptions

LOG = logging.getLogger(__name__)


def config_validator(section, config_opts=()):
    if section not in nirikshak.CONF:
        LOG.error("%s section could not be found in "
                  "configuration file", section)

        raise exceptions.SectionNotFoundException(section=section)

    for opt in config_opts:
        if opt not in nirikshak.CONF[section]:
            LOG.error("%s configuration option could not be "
                      "found in %s section.", section, opt)

            raise exceptions.ConfigurationNotFoundException(section=section)

    def func(f):
        return f

    return func
