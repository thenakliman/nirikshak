import logging
import yaml

from nirikshak.common import exceptions

LOG = logging.getLogger(__name__)


def get_yaml(location):
    try:
        with open(location, 'r') as f:
            try:
                content = yaml.load(f)
            except yaml.scanner.ScannerError:
                raise exceptions.InvalidFormatException(location=location)
    except IOError:
        raise exceptions.FileNotFound(location)

    return content
