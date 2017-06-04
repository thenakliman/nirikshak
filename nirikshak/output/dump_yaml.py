import logging
import yaml

import nirikshak
from nirikshak.common import yaml_util
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@base.register('yaml')
class YAMLFormatOutput(base.FormatOutput):
    def output(self, **kwargs):
        try:
            f = nirikshak.CONF['output_file']['output_dir']
        except KeyError:
            f = '/var/nirikshak/result.yaml'

        try:
            output_file = yaml_util.get_yaml(f)
        except IOError:
            output_file = {}
        except ValueError:
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
            yaml.dump(output_file, output, default_flow_style=False)
        LOG.info("Output has been dumped in %s file" % f)
        output.close()
