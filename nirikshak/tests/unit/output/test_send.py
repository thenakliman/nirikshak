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
import unittest

import mock
import requests

import nirikshak
from nirikshak.tests.unit import base as base_test
from nirikshak.output import base
from nirikshak.output import send

class TestSend(base_test.BaseTestCase):
    @staticmethod
    def _get_request_param():
        return {
            'host': 'tmp_host',
            'port': 101010,
            'method': 'put',
            'protocol': 'https',
            'url': 'v1/api'
        }

    def setUp(self):
        super(TestSend, self).setUp()
        base_test.create_conf()
        nirikshak.CONF['output_send'] = self._get_request_param()

    def tearDown(self):
        super(TestSend, self).tearDown()
        nirikshak.CONF.clear()

    def _make_url(self):
        request_parameters = self._get_request_param()
        return ("%s://%s:%s/%s" % (
            request_parameters['protocol'],
            request_parameters['host'],
            request_parameters['port'],
            request_parameters['url'],
        ))

    @mock.patch.object(send.LOG, 'error')
    @mock.patch.object(send.requests, 'put')
    @mock.patch.object(send.json, 'dumps')
    @mock.patch.object(base, 'make_output_dict')
    def test_output_send_fail(self, mock_base_make_dict, mock_json_dumps,
                              mock_put_request, mock_error_log):

        data = {'jaanch': {'result': {}}}
        def make_dict(key, exp, **kwargs):
            kwargs[key]['result']['output'] = exp
            return kwargs


        def dump_json(jaanch):
            return jaanch

        mock_base_make_dict.side_effect = make_dict
        mock_json_dumps.side_effect = dump_json
        mock_put_request.side_effect = requests.exceptions.ConnectionError
        send.NetworkSendOutput().output(**data)
        mock_put_request.assert_called_once_with(self._make_url(), data=data)
        mock_error_log.assert_called()

    @mock.patch.object(send.LOG, 'info')
    @mock.patch.object(send.requests, 'put')
    @mock.patch.object(send.json, 'dumps')
    @mock.patch.object(base, 'make_output_dict')
    def test_output_send_pass(self, mock_base_make_dict, mock_json_dumps,
                              mock_put_request, mock_info_log):

        data = {'jaanch': {'result': {}}}
        def make_dict(key, exp, **kwargs):
            kwargs[key]['result']['output'] = exp
            return kwargs

        def dump_json(jaanch):
            return jaanch

        mock_base_make_dict.side_effect = make_dict
        mock_json_dumps.side_effect = dump_json
        send.NetworkSendOutput().output(**data)
        mock_put_request.assert_called_once_with(self._make_url(), data=data)
        mock_info_log.assert_called()
