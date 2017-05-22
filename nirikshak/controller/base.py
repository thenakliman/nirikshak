import time
import logging
import multiprocessing

import nirikshak
from nirikshak.common import exceptions


def load_module(modname):
    try:
        module = __import__(modname, globals(), locals(), [modname], -1)
    except ImportError:
        logging.error('Unable to load module at %s' % modname)
        raise ImportError

    return module


def worker(queue, soochi):
    for n, jaanch in soochi['jaanches'].items():
        name = jaanch['type']
        name = name.replace('/', '.')
        modname = jaanch['type'].split('/')[-1:]
        a_name = ("nirikshak.workers.%s" % name)
        module = load_module(a_name)
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

    # TODO(thenakliman): May be these methods can be moved to
    # some generic method loading method.
    @classmethod
    def _get_soochis(cls, soochis=None, groups=None):
        input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
        modname = input_type.split('_')[1:]
        modname = ''.join(modname)
        modname = ('nirikshak.input.%s' % modname)
        module = load_module(modname)

        try:
            soochis = cls._call_method(module, 'get_soochis', soochis=soochis,
                                       groups=groups)
        except Exception:
            logging.error("Unable to get list of soochis from the %s input "
                          "type." % input_type)
            raise exceptions.InputExecutionException(input=input_type)

        logging.info("Soochi list has been fetched from the input module")
        return soochis

    @classmethod
    def _format_output(cls, **k):
        kwargs = k.values()[0]
        post_task = kwargs['input'].get('post_task', 'dummy')
        modname = ('nirikshak.post_task.%s' % post_task)
        module = load_module(modname)
        try:
            formatted = cls._call_method(module, 'format_it', **k)
        except Exception:
            msg = ("Error in performing post task for output")
            raise exceptions.PostTaskException()

        logging.info("Post task has been completed for %s jaanch" % (
                         k.keys()[0]))

        return formatted

    @classmethod
    def _output_result(cls, **k):
        kwargs = k.values()[0]
        output = kwargs['output'].get('type', 'console')
        modname = ('nirikshak.output.%s' % output)
        module = load_module(modname)

        try:
            cls._call_method(module, 'output', **k)
        except Exception:
            msg = ("Error in performing output")
            logging.error(msg)
            raise exceptions.OutputExecutionException(output=modname)

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
