import abc


class Command(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, bot):
        self._bot = bot

    @abc.abstractmethod
    def execute(self, user, *args):
        return NotImplemented
