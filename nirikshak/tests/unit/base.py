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
import mock
import unittest

import nirikshak


def get_main_yaml():
    main_yaml = {
      'deployment': {
         'groups': ['monitor'],
         'soochis': {
           'test_keystone': {
             'soochi': 'test_keystone'
             },
           'test_glance': {
             'soochi': 'test_glance'
             }
           },
         },
      'monitor': {
        'groups': ['deployment'],
        'soochis': {
          'test_keystone': {
            'soochi': 'test_keystone'
            },
          'test_glance': {
            'soochi': 'test_glance'
            }
          }
        }
      }

    return main_yaml


def get_test_keystone_soochi():
    jaanches = {
      'jaanches': {
        'port_5000': {
          'type': 'file',
          'post_task': 'console',
          'input': {
            'args': {
              'ip': '192.168.1.100',
              'port': 5000
              }
            },
          'output': {
            'type': 'console'
            }
          },
        'port_35357': {
          'type': 'file',
          'post_task': 'console',
          'input': {
            'args': {
              'ip': '192.168.1.100',
              'port': 35357
              }
            },
          'output': {
            'type': 'console'
            }
          }
        }
      }

    return jaanches


def get_test_glance_soochi():
    jaanches = {
      'jaanches': {
        'port_9292': {
          'type': 'file',
          'post_task': 'console',
          'input': {
            'args': {
              'ip': '192.168.1.100',
              'port': 9292
              }
            },
          'output': {
            'type': 'console'
            }
          },
        'port_1234': {
          'type': 'file',
          'post_task': 'console',
          'input': {
            'args': {
              'ip': '192.168.1.100',
              'port': 1234
              }
            },
          'output': {
            'type': 'console'
            }
          }
        }
      }

    return jaanches


def create_conf():
    nirikshak.CONF = {
        'default': {
            'log_file': '/var/log/nirikshak.log',
            'log_level': 'critical',
            'input_type': 'file',
            'workers': 10
        },
        'input_file': {
            'main_file': '/var/nirikshak/main.yaml'
        }
    }


def get_disk_jaanch():
    jaanch = {
        'type': 'disk_partition',
        'input': {
            'args': {
                'device': '/dev/sda1',
                'fstype': 'ext4',
                'mountpoint': '/',
            }
        }
    }

    return jaanch


def get_ini_jaanch():
    jaanch = {
        'type': 'ini',
        'input': {
            'args': {
                'file': '/etc/nirikshak/nirikshak.conf',
                'section': 'default',
                'key': 'log_level',
            },
        },
        'output': {
             'type': 'yaml'
         }
    }

    return jaanch


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        mock.patch('logging.getLogger')
