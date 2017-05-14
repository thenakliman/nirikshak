import abc
import six


@six.add_metaclass(abc.ABCMeta)
class Input(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_soochis(self, **kwargs):
        pass
