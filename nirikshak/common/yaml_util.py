import logging
import yaml

def get_yaml(location):
    with open(location, 'r') as f:
        try:
            content = yaml.load(f) 
        except yaml.scanner.ScannerError:
            msg = ("Invalid %s yaml file" % (location))
            logging.error(msg)
            raise InvalidFormatException(location=location)
        except IOError:
            msg = ("%s file not found")
            logging.error(msg)
            raise FileNotFound(location)

    return content
