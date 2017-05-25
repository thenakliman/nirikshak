import logging
import yaml

LOG = logging.getLogger(__name__)


def get_yaml(location):
    with open(location, 'r') as f:
        try:
            content = yaml.load(f)
        # FIXME(thenakliman): Not being raised
        except yaml.scanner.ScannerError:
            msg = ("Invalid %s yaml file" % (location))
            LOG.error(msg)
            raise InvalidFormatException(location=location)
        except IOError:
            msg = ("%s file not found")
            LOG.error(msg)
            raise FileNotFound(location)

    return content
