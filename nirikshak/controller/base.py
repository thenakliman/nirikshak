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
import os

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

    for name, jaanch in soochi['jaanches'].items():
        try:
            queue.put({name: base_worker.do_work(**{name: jaanch})})
        except Exception:
            LOG.error("%s jaanch failed to get executed", name)


def _get_workers_pool():
    workers_num = nirikshak.CONF['default'].get('workers', -1)
    workers_num = int(workers_num)
    # fixme(thenakliman): Verify locking is really being done
    lock = []
    for resource in constants.LOCKABLE_RESOURCES_INDEX.__dict__:
        if not resource.startswith('__'):
            lock.append(multiprocessing.Lock())

    if workers_num == -1:
        workers_num = multiprocessing.cpu_count()

    return multiprocessing.Pool(workers_num,
                                initializer=synchronizer.init_locks,
                                initargs=(lock,))


def _load_modules():
    utils.load_modules_from_location(get_module_path(output))
    utils.load_modules_from_location(get_module_path(inputs))


def get_module_path(module):
    return [os.path.dirname(module.__file__)]


def _get_soochis(soochis=None, groups=None):
    """Calls the input module to return soochis to be executed"""
    return inputs.get_soochis(soochis, groups)


def _format_output(**k):
    """Calls post task formatting to be done."""
    return post_task.format_for_output(**k)


def _output_result(**k):
    """Output the result through plugins defined in the configuration"""
    return output.output(**k)


def _start_worker(soochis_def):
    """Dispatch the worker to process pool"""
    queue = multiprocessing.Manager().Queue()
    pool = _get_workers_pool()
    for soochi in soochis_def:
        pool.apply_async(worker, args=(queue, soochi))

    pool.close()
    pool.join()
    while not queue.empty():
        try:
            jaanch = queue.get()
            formatted_output = _format_output(**jaanch)
            _output_result(**formatted_output)
        except ImportError:
            pass
        except exceptions.PostTaskException:
            pass


def _merge_configs(soochis_def):
    """Merge configuration dictionaries"""
    new_def = []
    for soochis in soochis_def:
        config = soochis[0]
        for jaanch in soochis[1]['jaanches']:
            utils.merge_dict(soochis[1]['jaanches'][jaanch], config)
        new_def.append(soochis[1])

    return new_def


def execute(soochis=None, groups=None):
    """Start jaanch process"""
    LOG.info("Starting execution of soochis.")
    _load_modules()
    soochis_def = _get_soochis(soochis, groups)
    soochis_def = _merge_configs(soochis_def)
    _start_worker(soochis_def)
    LOG.info("Execution of soochis are finished.")
