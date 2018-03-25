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
import mock

import unittest

import multiprocessing
import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import plugins
from nirikshak.controller import base as base_controller
from nirikshak.input import base as input_base
from nirikshak.output import base as output
from nirikshak.post_task import base as base_post_task
from nirikshak.tests.unit import base
from nirikshak.workers import base as base_worker


class WorkerTest(unittest.TestCase):
    def setUp(self):
        super(WorkerTest, self).setUp()
        base.create_conf()

    def tearDown(self):
        super(WorkerTest, self).tearDown()
        plugins._PLUGINS.clear()

    @staticmethod
    def _get_fake_jaanch():
        return [
            [{'key1': 'value1'},
             {'jaanches': [
                 {'name': 'jaanch1', 'jaanch1_param': 'jaanch1_body'}]}],
            [{'key2': 'value2'}, {
                'jaanches': [{
                    'name': 'jaanch2', 'jaanch2_param': 'jaanch2_body', 'k2': 'v2'}]}]
        ]

    @mock.patch.object(base_post_task, 'format_for_output')
    @mock.patch.object(output, 'output')
    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(input_base, 'get_soochis')
    def test_run_worker(self, mock_get_soochis, mock_do_work,
                        mock_output, mock_post_task):

        def do_worker(**kwargs):
            return {'work': True}           # pragma: no cover

        def post_task(**kwargs):
            kwargs['post_task'] = True
            return kwargs

        def output(**kwargs):
            return

        mock_get_soochis.return_value = self._get_fake_jaanch()
        mock_do_work.side_effect = do_worker
        mock_output.side_effect = output
        mock_post_task.side_effect = post_task

        base_controller.execute(soochis=['soochi'], groups=['group'])

        mock_get_soochis.assert_called_once_with(['soochi'], ['group'])
        post_task_calls = [mock.call(work=True), mock.call(work=True)]
        mock_post_task.assert_has_calls(post_task_calls, any_order=True)
        mock_output = mock.call(work=True, post_task=True)
        mock_output.assert_has_calls([mock_output, mock_output])

    def _test_post_task_failure(self, mock_get_soochis, mock_do_work,
                                mock_post_task):

        def do_worker(**kwargs):
            return {'work': True}           # pragma: no cover

        mock_get_soochis.return_value = self._get_fake_jaanch()
        mock_do_work.side_effect = do_worker
        base_controller.execute(soochis=['soochi'], groups=['group'])

        mock_get_soochis.assert_called_once_with(['soochi'], ['group'])
        post_task_calls = [mock.call(work=True), mock.call(work=True)]
        mock_post_task.assert_has_calls(post_task_calls, any_order=True)

    @mock.patch.object(base_post_task, 'format_for_output',
                       side_effect=ImportError)
    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(input_base, 'get_soochis')
    def test_get_run_worker_import_error(self, mock_get_soochis, mock_do_work,
                                         mock_post_task):
        self._test_post_task_failure(mock_get_soochis, mock_do_work,
                                     mock_post_task)

    @mock.patch.object(base_post_task, 'format_for_output',
                       side_effect=exceptions.PostTaskException)
    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(input_base, 'get_soochis')
    def test_get_run_worker_post_task_error(self, mock_get_soochis,
                                            mock_do_work, mock_post_task):
        self._test_post_task_failure(mock_get_soochis, mock_do_work,
                                     mock_post_task)

    def test_workers_are_set_from_config(self):
        nirikshak.CONF['default']['workers'] = -1
        self.assertEqual(multiprocessing.cpu_count(),
                         base_controller._get_workers_pool()._processes)


class WorkerInvokeTest(unittest.TestCase):
    @mock.patch.object(nirikshak.workers, 'load_workers',
                       side_effect=ImportError)
    def test_worker_load_fails(self, mock_worker):
        jaanches = {'jaanches': {}}
        base_controller.worker(mock.Mock(), jaanches)
        mock_worker.assert_called_once_with()

    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(nirikshak.workers, 'load_workers')
    def test_worker_failed_in_queue_put(self, mock_load_worker,
                                        mock_do_worker):

        jaanches = {'jaanches': [{'name': 'fake_jaanch'}]}
        mock_queue = mock.Mock(put=mock.Mock(side_effect=Exception))

        base_controller.worker(mock_queue, jaanches)

        mock_load_worker.assert_called_once_with()
        mock_do_worker.assert_called_with(name='fake_jaanch')
        mock_queue.put.assert_called_once()

    @mock.patch.object(base_worker, 'do_work')
    @mock.patch.object(nirikshak.workers, 'load_workers')
    def test_worker_get_jaanch(self, mock_load_workers, mock_base_worker):

        def side_effect(**jaanch):
            return 10

        mock_base_worker.side_effect = side_effect
        jaanches = {'jaanches': [{'name': 'fake_jaanch'}]}
        mock_queue = mock.Mock(put=mock.Mock())

        base_controller.worker(mock_queue, jaanches)

        mock_base_worker.assert_called_with(name='fake_jaanch')
        mock_queue.put.assert_called_once_with(10)
        mock_load_workers.assert_called_once_with()
