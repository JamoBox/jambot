from lib.base import JamBase


class Channel(JamBase):

    """IRC Channel object"""

    def __init__(self, name, server, password=''):
        """Create IRC Channel object.

        :name: Name of channel
        :server: IRC server the channel resides on
        :password: Optional channel password

        """
        JamBase.__init__(self)

        self._name = name
        self._server = server
        self._password = password

    def get_users(self):
        pass

    def get_options(self):
        pass
