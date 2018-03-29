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
from nirikshak.common import plugins
from nirikshak.output import base

LOG = logging.getLogger(__name__)


@plugins.register('csv')
class CSVFormatOutput(base.FormatOutput):
    @staticmethod
    def _get_output_file_location():
        output_file_loc = None
        try:
            output_file_loc = nirikshak.CONF['output_csv']['output_dir']
        except KeyError:
            output_file_loc = '/var/lib/nirikshak/result.csv'

        return output_file_loc

    @staticmethod
    def _read_csv_file(file_location):
        output_file_content = []
        try:
            with open(file_location, 'r') as fobj:
                reader = csv.reader(fobj, delimiter=' ', quotechar='|')
                for row in reader:
                    output_file_content.append(row)
        except IOError:
            pass

        return output_file_content

    @staticmethod
    def _format_output_for_csv(**kwargs):
        try:
            expected_result = kwargs['output']['result']
        except KeyError:
            expected_result = None

        jaanch = ("%s,input") % kwargs['name']
        for k, value in kwargs['input']['args'].items():
            jaanch = ("%s,%s,%s" % (jaanch, k, value))
            jaanch = ("%s,output,expected_output,%s,actual_output,%s" % (
                jaanch, expected_result,
                kwargs['input'].get('result')))

        return jaanch

    @staticmethod
    def _write_csv_file(content, file_location):
        with open(file_location, "w") as csv_file:
            csv_writer = csv.writer(csv_file)
            for row in content:
                csv_writer.writerow(row[0].split(','))

    def output(self, **kwargs):
        output_file_location = self._get_output_file_location()
        output_file_content = self._read_csv_file(output_file_location)
        formatted_output = self._format_output_for_csv(**kwargs)
        output_file_content.append([formatted_output])
        self._write_csv_file(output_file_content, output_file_location)
        LOG.info("Output has been dumped in %s file", output_file_location)
