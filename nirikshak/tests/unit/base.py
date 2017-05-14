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
