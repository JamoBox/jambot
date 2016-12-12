import socket
import sys
import re
import time

from lib.misc import pp, pbot
from lib.base import JamBase


class IrcServer(JamBase):

    connection_retry_count = 0

    def __init__(self, name, address, port, max_reconnects=2):
        self.name = name
        self.address = address
        self.port = port
        self.max_reconnects = max_reconnects
        self._connection = None

        #TODO: Change this
        self.config = None

    def _send_raw(self, raw_message):
        self._connection.send(raw_message)

    def send(self, message):
        msg = message.replace('\r\n', '  ')
        self._send_raw('{0}\r\n'.format(msg))

    def connect(self, timeout=10):
        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._connection.settimeout(timeout)

        username = self.config.account.username.lower()
        password = self.config.account.password

        try:
            self._connection.connect((self.address, self.port))
        except:
            # pp('Error connecting to IRC server. ({0}:{1}) ({2})'
            #    .format(server, port, self.connection_retry_count + 1),
            #    'error')

            if self.connection_retry_count < self.max_reconnects:
                self.connection_retry_count += 1
                return self.connect()
            else:
                sys.exit()

        self._connection.settimeout(None)

        self._connection.send('USER {0}'.format(username))
        self._connection.send('PASS {0}'.format(password))
        self._connection.send('NICK {0}'.format(username))

        if not self.check_login_status(self.recv()):
            pp('Invalid login.', 'error')
            sys.exit()
        else:
            pp('Login successful!')

    def ping(self, data):
        if data.startswith('PING'):
            self._connection.send(data.replace('PING', 'PONG'))

    def recv(self, amount=1024):
        return self._connection.recv(amount)

    def recv_messages(self, amount=1024):
        messages = []
        data = self.recv(amount)

        if not data:
            pbot('Lost connection, reconnecting.')
            self.connect()
        self.ping(data)

        if self.check_has_message(data):
            messages = []
            for line in filter(None, data.split('\r\n')):
                messages.append(self.parse_message(line))

        return messages

    def check_login_status(self, data):
        #FIXME: remove twitch stuff
        return not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data)

    def check_has_message(self, data):
        #FIXME: remove twitch stuff
        return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)
