import logging
import yaml

LOG = logging.getLogger(__name__)


def get_yaml(location):
    try:
        with open(location, 'r') as f:
            try:
                content = yaml.load(f)
            except yaml.scanner.ScannerError:
                raise InvalidFormatException(location=location)
    except IOError:
        raise FileNotFound(location)

    return content
