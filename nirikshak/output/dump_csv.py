import logging
import csv

import nirikshak
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@base.register('csv')
class CSVFormatOutput(base.FormatOutput):
    def output(self, **kwargs):
        try:
            f = nirikshak.CONF['output_csv']['output_dir']
        except KeyError:
            f = '/var/nirikshak/result.csv'

        output_file = []
        try:
            with open(f, 'r') as fobj:
                reader = csv.reader(fobj, delimiter=' ', quotechar='|')
                for row in reader:
                    output_file.append(row)
        except IOError:
            pass

        key = kwargs.keys()[0]
        try:
            expected_result = kwargs[key]['output']['result']
        except KeyError:
            expected_result = None

        jaanch = ("%s,input") % key
        for k, v in kwargs[key]['input']['args'].iteritems():
            jaanch = ("%s,%s,%s" % (jaanch, k, v))

            jaanch = ("%s,output,expected_output,%s,actual_output,%s" % (
                      jaanch, expected_result, kwargs[key]['input']['result']))

        output_file.append([jaanch])
        with open(f, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in output_file:
                csv_writer.writerow(row[0].split(','))

        LOG.info("Output has been dumped in %s file" % f)
        csv_file.close()
