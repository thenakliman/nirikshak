import json


import nirikshak


def output(**kwargs):
    try:
        f = nirikshak.CONF['output_json']['output_dir']
    except KeyError:
        f = '/var/nirikshak/result.json'

    try:
        with open(f, 'r') as output:
            output_file = json.load(output)
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
        str_ = json.dumps(output_file, indent=4,
                          sort_keys=True, separators=(',', ': '))
        output.write(str_)

    output.close()
