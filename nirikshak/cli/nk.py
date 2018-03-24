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

import argparse
import logging

import nirikshak
from nirikshak.controller import base


def process_args():
    parser = argparse.ArgumentParser(description='Process nirikshak command '
                                                 'line arguments')

    parser.add_argument('--soochis', metavar='s', type=str, nargs='+',
                        default=[], help='List of soochi for verification')
    parser.add_argument('--config-file', metavar='c', type=str,
                        default=[], help='Path of configuration '
                        'file for nirikshak')
    parser.add_argument('--groups', metavar='g', type=str, nargs='+',
                        default=[], help='List of groups to be executed')

    return parser.parse_args()


def main():
    args = process_args()
    argument = vars(args)
    # fixme(thenakliman): Allow passing of configuration file
    # for the execution of jaanch. Currently config is loaded
    # during module load therefore it is not possible to use CLI passed
    # configuration file.
    del argument['config_file']
    nirikshak.initialize_config()
    nirikshak.initialize_logging()
    base.execute(**argument)
    logging.info("Jaanch has been finished, check results")
