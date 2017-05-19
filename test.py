from nirikshak.workers.network import network_port
inti = {'port': {{'input': {{'args': {{'ip': '192.168.181.103'}, {'port': '22'}}}, {'output': {{'type': 'console'}, {'result': 0}}}}}}}
#a = {'port_22': [{'input': {'args': {'ip': '192.168.181.103'}, {'port': '22'}}}, {'output': {'type': 'console'}, {'result': 0}}]}

network_port.work(**inti)
