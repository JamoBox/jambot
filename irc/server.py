""" IRC Server definition """

import socket
import re

from lib.base import JamBase


class IrcServer(JamBase):

    """ IRC Server Definition. """

    connection_retry_count = 0

    def __init__(self, name, address, port=6667, max_reconnects=2):
        """ Create an IRC server instance.

        Provides abstraction to interface with an IRC server.

        :name: Common name of IRC server.
        :address: FQDN or IP address of the server.
        :port: Server port to connect to.
        :max_reconnects: Maximum reconnection attempts.

        """

        JamBase.__init__(self)

        self.name = name
        self.address = address
        self.port = port
        self.max_reconnects = max_reconnects
        self._connection = None

    def _send_raw(self, raw_message):
        self._connection.send(raw_message)

    def send(self, message):
        """ Send a message to the IRC server.

        Use to send messages to the IRC server. Sends the
        appropriate line termination characters and strips
        any of these out of the original message to avoid
        accidental partial messages.

        Do not use this to directly message channels; see the
        Channel object's `send_message` method instead, which
        sends the additional required strings.

        :message: Message to send to the IRC server.

        """

        msg = message.replace('\r\n', '  ')
        self._send_raw('{0}\r\n'.format(msg))

    def connect(self, timeout=10):
        """ Connect to the IRC server.

        This creates a network connection to the IRC server.
        After establishing a successful network connection however,
        it DOES NOT continue to send any of the mandatory initial
        connection strings to the server. It is up to the caller to
        send these using the IrcAccount object's `join_server` method.

        """

        self._connection.settimeout(timeout)

        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._connection.settimeout(timeout)

        self._connect_to_server()

        self._connection.settimeout(None)

    def _connect_to_server(self):
        try:
            self._connection.connect((self.address, self.port))
        except socket.error:
            self._logger.error('Error connecting to IRC server. ({%s}:{%s})',
                               self.name, self.port)

            if self.connection_retry_count < self.max_reconnects:
                self.connection_retry_count += 1
                return self.connect()
            else:
                raise IOError('Max reconnect attempts to {0} reached.'
                              .format(self.name))

    def ping(self, data):
        """ Respond to ping from server.

        Sends a PONG response back to the server when receiving a PING.

        """

        if data.startswith('PING'):
            # Make sure we send back the PING meta string.
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

#     def check_login_status(self, data):
#         #FIXME: remove twitch stuff
#         return not re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data)

    def check_has_message(self, data):
        #FIXME: remove twitch stuff
        return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)
