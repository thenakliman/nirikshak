import time
import logging
import multiprocessing

import nirikshak
from nirikshak.common import exceptions


def worker(queue, soochi):
    for n, jaanch in soochi['jaanches'].items():
        name = jaanch['type']
        name = name.replace('/', '.')
        modname = jaanch['type'].split('/')[-1:]
        a_name = ("nirikshak.workers.%s" % name)
        print(a_name)
        try:
            module = __import__(a_name, globals(), locals(), modname, -1)
        except ImportError as e:
            logging.error("Unable to find %s type of jaanch" %
                          jaanch['type'])
            continue

        try:
            queue.put({n: getattr(module, 'work')(**jaanch)})
        except Exception as e:
            print(e)
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

    # TODO(thenakliman): May be these methods can be moved to
    # some generic method loading method.
    def _get_soochis(self, soochis=None, groups=None):
        input_type = nirikshak.CONF['default'].get('input_type', 'input_file')
        mod_name = input_type.split('_')[1:]
        mod_name = ''.join(mod_name)
        mod_loc = ('nirikshak.input.%s' % mod_name)
        try:
            module = __import__(mod_loc, globals(), locals(), [mod_name], -1)
        except ImportError:
            logging.error('Unable to load module at %s' % mod_loc)
            raise ImportError

        try:
            soochis = getattr(module, 'get_soochis')(soochis=soochis,
                                                     groups=groups)
        except Exception:
            logging.error("Unable to get list of soochis from the %s input "
                          "type." % input_type)
            raise exceptions.InputExecutionException(input=input_type)

        logging.info("Soochi list has been fetched from the input module")
        return soochis

    @staticmethod
    def _format_output(**k):
        kwargs = k.values()[0]
        post_task = kwargs['input'].get('post_task', 'dummy')
        modname = ('nirikshak.post_task.%s' % post_task)
        try:
            module = __import__(modname, globals(), locals(), [post_task], -1)
        except ImportError:
            logging.error("Unable to load %s module." % modname)
            raise ImportError

        try:
            return getattr(module, 'format_it')(**k)
        except Exception:
            msg = ("Error in performing post task for output")
            raise exceptions.PostTaskException()

    @staticmethod
    def _output_result(**k):
        kwargs = k.values()[0]
        output = kwargs['output'].get('type', 'console')
        modname = ('nirikshak.output.%s' % output)

        try:
            module = __import__(modname, globals(), locals(), [output], -1)
        except ImportError:
            logging.error("Unable to load %s module." % modname)
            raise ImportError

        try:
            return getattr(module, 'output')(**k)
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
