import logging
import json
import os

import nirikshak
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@base.register('json')
class JSONFormatOutput(base.FormatOutput):
    def output(self, **kwargs):
        try:
            f = nirikshak.CONF['output_json']['output_dir']
        except KeyError:
            f = '/var/nirikshak/result.json'

        try:
            if os.stat(f).st_size:
                with open(f, 'r') as output:
                    output_file = json.load(output)
            else:
                output_file = {}
        except OSError:
            output_file = {}

        key = kwargs.keys()[0]
        try:
            expected_result = kwargs[key]['output']['result']
        except KeyError:
            expected_result = None

        jaanch = base.make_output_dict(key, expected_result, **kwargs)
        if not output_file:
            output_file = jaanch
        else:
            output_file.update(jaanch)

        with open(f, "w") as output:
            str_ = json.dumps(output_file, indent=4,
                              sort_keys=True, separators=(',', ': '))
            output.write(str_)

        LOG.info("Output has been dumped in %s" % f)
        output.close()
