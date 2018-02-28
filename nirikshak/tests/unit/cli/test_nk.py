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
import sys

import mock

import nirikshak
from nirikshak.cli import nk
from nirikshak.controller import base
from nirikshak.tests.unit import base as test_base


class TestMain(test_base.BaseTestCase):
    @staticmethod
    @mock.patch.object(nk.logging, 'info')
    @mock.patch.object(base, 'Router')
    @mock.patch.object(nirikshak, 'initialize_config')
    @mock.patch.object(nirikshak, 'initialize_logging')
    def test_main(mock_config, mock_logging, mock_router, mock_info):
        sys.argv = ['--group=deployment']
        nk.main()
        mock_config.assert_called_once_with()
        mock_router.assert_called()
        mock_logging.assert_called_once_with()
        mock_info.assert_called()
