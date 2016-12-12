import re

from lib.base import JamBase


class IrcMessage(JamBase):

    """IRC message definition"""

    def __init__(self, raw=''):
        """Initialise an IRC message.

        :raw: Raw message string to construct IrcMessage from.

        """
        JamBase.__init__(self)

        self.channel = None
        self.username = None
        self.content = None

        if raw:
            self.channel = self._parse_channel(raw)
            self.username = self._parse_username(raw)
            self.content = self._parse_content(raw)

    def _parse_channel(self, raw_message):
        regex = r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :'
        return re.findall(regex, raw_message)[0]

    def _parse_username(self, raw_message):
        regex = r'^:([a-zA-Z0-9_]+)\!'
        return re.findall(regex, raw_message)[0],

    def _parse_content(self, raw_message):
        regex = r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)'
        return re.findall(regex, raw_message)[0].decode('utf8')
