import abc


class Command(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        super(Command, self).__init__(kwargs)
        [setattr(self, k, v) for k, v in kwargs.iteritems()]

    @abc.abstractmethod
    def execute(self, user, *args):
        return NotImplemented
