# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import print_function
import logging
try:
    # for python3.5
    import configparser
except ImportError:
    # for python2.7
    import ConfigParser as configparser

CONF = None


def make_dict(config):
    dict1 = {}
    sections = config.sections()
    for section in sections:
        options = config.options(section)
        dict2 = {}
        for option in options:
            try:
                dict2[option] = config.get(section, option)
            except Exception:
                dict2[option] = None

        dict1[section] = dict2

    return dict1


def initialize_config(config_file=None):
    global CONF
    if not config_file:
        config_file = '/etc/nirikshak/nirikshak.conf'

    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except Exception:
        print("Unable to load configuration file at %s." % config_file)

    CONF = make_dict(config)


def initialize_logging():
    """Initilization of logging module."""
    global CONF
    if not CONF['default'].get('log_file', False):
        CONF['default']['log_file'] = '/var/log/nirikshak.log'

    log_level = CONF['default'].get('log_level', 'info')
    formatter = ("%(asctime)s %(levelname)s %(name)s %(funcName)s():%(lineno)s"
                 " PID:%(process)d %(message)s")

    logging.basicConfig(filename=CONF['default']['log_file'],
                        level=getattr(logging, log_level.upper()),
                        format=formatter)

    logging.info("Logging module loaded successfully")
