import socket
import sys
import re
import time

from lib.misc import pp, pbot
from lib.base import JamBase


class IrcServer(JamBase):

    socket_retry_count = 0

    def __init__(self, config):
        self.config = config

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = sock

        sock.settimeout(10)

        username = self.config.account.username.lower()
        password = self.config.account.password

        server = self.config.irc.server
        port = self.config.irc.port

        try:
            sock.connect((server, port))
        except:
            pp('Error connecting to IRC server. ({0}:{1}) ({2})'
               .format(server, port, self.socket_retry_count + 1),
               'error')

            if self.socket_retry_count < 2:
                self.socket_retry_count += 1
                return self.connect()
            else:
                sys.exit()

        sock.settimeout(None)

        sock.send('USER %s\r\n' % username)
        sock.send('PASS %s\r\n' % password)
        sock.send('NICK %s\r\n' % username)

        if not self.check_login_status(self.recv()):
            pp('Invalid login.', 'error')
            sys.exit()
        else:
            pp('Login successful!')

    def ping(self, data):
        if data.startswith('PING'):
            self.sock.send(data.replace('PING', 'PONG'))

    def recv(self, amount=1024):
        return self.sock.recv(amount)

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
