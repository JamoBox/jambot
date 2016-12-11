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
            self.parse_message(raw)

    def parse_message(self, raw_message):
        self.channel = self.parse_channel(raw_message)
        self.username = self.parse_username(raw_message)
        self.content = self.parse_content(raw_message)

    def parse_channel(self, raw_message):
        regex = r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :'
        return re.findall(regex, raw_message)[0]

    def parse_username(self, raw_message):
        regex = r'^:([a-zA-Z0-9_]+)\!'
        return re.findall(regex, raw_message)[0],

    def parse_content(self, raw_message):
        regex = r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)'
        return re.findall(regex, raw_message)[0].decode('utf8')
