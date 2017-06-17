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
            f = '/var/lib/nirikshak/result.csv'

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
