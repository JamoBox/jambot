import importlib
from lib.irc import Irc
from lib.invoker import Invoker


class Bot:

    def __init__(self, config):
        self.config = config
        self.irc = Irc(config)

        self._commands = []

        self.cmd_prefix = config.misc.cmd_prefix
        self.ops = config.ops

        self._whitelist = None
        self._blacklist = None

        self._invoker = Invoker(self)

    def register_commands(self):
        for command in self.config.commands:
            importlib.import_module('commands.{}'
                                    .format(command))
            self.register_command(command)

    def register_command(self, cmd):
        self._invoker.register(cmd)

    def handle_command(self, username, command):
        if username in self.ops:
            self._invoker.invoke(command, user=username)

    def audit_action(self, username):
        #TODO: FIX THIS
        if self._invoker.has('wl'):
            if not self._whitelist:
                self._whitelist = self._invoker.invoke('wl')
                self._whitelist.load_whitelist()
            if self._whitelist.load_whitelist():
                if username.lower() in self._whitelist.load_whitelist():
                    pass
                else:
                    return
        if self._invoker.has('bl'):
            if not self._blacklist:
                self._blacklist = self._invoker.invoke('bl')
                self._blacklist.load_blacklist()
            if username.lower() not in self._blacklist.load_blacklist():
                pass
        else:
            pass

    def run(self):
        while True:
            for message in self.irc.recv_messages(1024):
                username = message['username'].lower()
                if message['message'][0] == self.cmd_prefix:
                    self.handle_command(username, message['message'][1:])
