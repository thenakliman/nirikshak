import time
import logging
import multiprocessing

import nirikshak
from nirikshak.common import exceptions
from nirikshak.common import load_module
from nirikshak.input import base as inputs
from nirikshak.post_task import base as post_task
from nirikshak.output import base as output


def worker(queue, soochi):
    for n, jaanch in soochi['jaanches'].items():
        name = jaanch['type']
        name = name.replace('/', '.')
        modname = jaanch['type'].split('/')[-1:]
        a_name = ("nirikshak.workers.%s" % name)
        module = load_module.load(a_name)
        try:
            queue.put({n: getattr(module, 'work')(**jaanch)})
        except Exception as e:
            logging.error("%s jaanch failed to get executed" % n)


class Router(object):
    """This class routes the work to proper modules and load them
       as per requirement."""
    def __init__(self):
        workers = nirikshak.CONF['default'].get('workers', -1)
        workers = int(workers)
        if workers == -1:
            workers = multiprocessing.cpu_count()

        self.pool = multiprocessing.Pool(workers)
        self.queue = multiprocessing.Manager().Queue()
        logging.info("Router has been initilized")

    @classmethod
    def _call_method(cls, module, method, *args, **kwargs):
        return getattr(module, method)(*args, **kwargs)

    @classmethod
    def _get_soochis(cls, soochis=None, groups=None):
        return inputs.get_soochis(soochis, groups)

    @classmethod
    def _format_output(cls, **k):
        return post_task.format_for_output(**k)

    @classmethod
    def _output_result(cls, **k):
        return output.output(**k)

    def _start_worker(self, soochis_def):
        for soochi in soochis_def:
            self.pool.apply_async(worker, args=(self.queue, soochi))

        self.pool.close()
        self.pool.join()
        while not self.queue.empty():
            try:
                jaanch = self.queue.get()
                formatted_output = self._format_output(**jaanch)
                self._output_result(**formatted_output)
            except ImportError, exceptions.PostTaskException:
                pass

    def start(self, tags=[], soochis=[], groups=[], **kwargs):
        logging.info("Starting execution of soochis.")
        soochis_def = self._get_soochis(soochis, groups)
        self._start_worker(soochis_def)
        logging.info("Execution of soochis are finished.")
