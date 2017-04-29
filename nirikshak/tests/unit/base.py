def get_main_yaml():
    main_yaml = {
      'deployment': {
         'groups': ['monitor'],
         'soochis': {
           'keystone': {
             'soochi': 'keystone'
             },
           'glance': {
             'soochi': 'glance'
             }
           },
         },
      'monitor': {
        'groups': ['deployment'],
        'soochis': {
          'keystone': {
            'soochi': 'keystone'
            },
          'glance': {
            'soochi': 'glance'
            }
          }
        }
      }

    return main_yaml

def get_keystone_soochi():
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
            }
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
