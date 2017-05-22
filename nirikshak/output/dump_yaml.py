import yaml


import nirikshak
from nirikshak.common import yaml_util


def output(**kwargs):
    try:
        f = nirikshak.CONF['output_file']['output_dir']
    except KeyError:
        f = '/var/nirikshak/result.yaml'

    try:
        output_file = yaml_util.get_yaml(f)
    except IOError:
        output_file = {}

    key = kwargs.keys()[0]
    try:
        expected_result = kwargs[key]['output']['result']
    except KeyError:
        expected_result = None

    jaanch = {
        key: {
            'input': kwargs[key]['input']['args'],
            'output': {
                 'expected_output': expected_result,
                 'actual_output': kwargs[key]['input']['result']
            }
        }
    }
 
    if not output_file:
        output_file = jaanch
    else:
        output_file.update(jaanch)

    with open(f, "w") as output:
        yaml.dump(output_file, output, default_flow_style=False)

    output.close()
