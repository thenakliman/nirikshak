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
import copy
import multiprocessing

from nirikshak.common import utils
from nirikshak.input import base as base_input
from nirikshak.workers import base as base_worker
from nirikshak.output import base as base_output
from nirikshak.post_task import base as base_post_task


CORES = multiprocessing.cpu_count()


def _work(queue, kwargs):
    result = base_worker.do_work(**kwargs)
    queue.put(result)


def _handle_post_processing(**jaanch):
    formatted_output = base_post_task.format_for_output(**jaanch)
    base_output.output(**formatted_output)


# NOTE(thenakliman): callback could be provided for post tasks rather than
# using queue. But synchronization issue will get complicated, while writing
# output to a json, yaml files. For now, let's use queue and then later on,
# could be removed once, synchronization issue is resolved.
def _dispatch_workers(soochis):
    pool = multiprocessing.Pool(processes=min(CORES, soochis))
    queue = multiprocessing.Manager().Queue()
    for soochi in soochis:
        pool.apply_async(_work, (queue, soochi))

    pool.close()
    pool.join()

    while not queue.empty():
        _handle_post_processing(**(queue.get()))


def _enrich_config(soochis):
    enriched_jaanches = []
    for soochi_config, jaanches in soochis:
        for jaanch in list(jaanches.values()):
            duplicate_jaanch = copy.deepcopy(jaanch)
            utils.merge_dict(duplicate_jaanch, soochi_config)
            enriched_jaanches.append(duplicate_jaanch)

    return enriched_jaanches


def start(soochis=None, groups=None):
    soochis = base_input.get_soochis(soochis=[], groups=[])
    return _dispatch_workers(_enrich_config(soochis))
