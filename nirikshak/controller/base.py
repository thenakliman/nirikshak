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
import multiprocessing

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import utils
from nirikshak.common import constants
from nirikshak.common import synchronizer
from nirikshak.input import base as inputs
from nirikshak.post_task import base as post_task
from nirikshak.output import base as output
from nirikshak import workers
from nirikshak.workers import base as base_worker

LOG = logging.getLogger(__name__)


def worker(queue, soochi):
    """Calls wotker specific to a jaanch"""

    try:
        workers.load_workers()
    except Exception:
        LOG.error("Failed to load workers.", exc_info=True)
    else:
        LOG.info("Loading worker modules.")

    for name, jaanch in soochi['jaanches'].iteritems():
        try:
            queue.put({name: base_worker.do_work(**{name: jaanch})})
        except Exception:
            LOG.error("%s jaanch failed to get executed", name)


class Router(object):
    """This class routes the work to proper modules and load them
       as per requirement."""
    def __init__(self):
        workers_num = nirikshak.CONF['default'].get('workers', -1)
        workers_num = int(workers_num)
        lock = []
        for resource in constants.LOCKABLE_RESOURCES_INDEX.__dict__:
            if not resource.startswith('__'):
                lock.append(multiprocessing.Lock())

        if workers_num == -1:
            workers_num = multiprocessing.cpu_count()

        # fixme(thenakliman): Verify locking is really being done
        self.pool = multiprocessing.Pool(workers_num,
                                         initializer=synchronizer.init_locks,
                                         initargs=(lock,))

        self.queue = multiprocessing.Manager().Queue()
        LOG.info("Router has been initilized")

    @staticmethod
    def _call_method(module, method, *args, **kwargs):
        """Generfic method to call method defined in other module"""
        return getattr(module, method)(*args, **kwargs)

    @staticmethod
    def _get_soochis(soochis=None, groups=None):
        """Calls the input module to return soochis to be executed"""
        return inputs.get_soochis(soochis, groups)

    @staticmethod
    def _format_output(**k):
        """Calls post task formatting to be done."""
        return post_task.format_for_output(**k)

    @staticmethod
    def _output_result(**k):
        """Output the result through plugins defined in the configuration"""
        return output.output(**k)

    def _start_worker(self, soochis_def):
        """Dispatch the worker to process pool"""
        for soochi in soochis_def:
            self.pool.apply_async(worker, args=(self.queue, soochi))

        self.pool.close()
        self.pool.join()
        while not self.queue.empty():
            try:
                jaanch = self.queue.get()
                formatted_output = self._format_output(**jaanch)
                self._output_result(**formatted_output)
            except ImportError:
                pass
            except exceptions.PostTaskException:
                pass

    @staticmethod
    def _merge_configs(soochis_def):
        """Merge configuration dictionaries"""
        new_def = []
        for soochis in soochis_def:
            config = soochis[0]
            for jaanch in soochis[1]['jaanches']:
                utils.merge_dict(soochis[1]['jaanches'][jaanch], config)
            new_def.append(soochis[1])

        return new_def

    def start(self, soochis=None, groups=None):
        """Start jaanch process"""
        LOG.info("Starting execution of soochis.")
        soochis_def = self._get_soochis(soochis, groups)
        soochis_def = self._merge_configs(soochis_def)
        self._start_worker(soochis_def)
        LOG.info("Execution of soochis are finished.")
