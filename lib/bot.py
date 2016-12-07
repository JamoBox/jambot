from config.config import config
from lib.irc import Irc
from lib.game import Game
from lib.misc import pbutton
from lib.invoker import Invoker
from commands.whitelist import WhitelistCommand
from commands.blacklist import BlacklistCommand
from commands.goal import GoalCommand


class Bot:

    def __init__(self):
        self.config = config
        self.irc = Irc(config)
        self.game = Game()
        self.message_buffer = [{'username': '', 'button': ''}] * self.config['misc']['chat_height']
        self.cmd_prefix = config['misc']['cmd_prefix']
        self.ops = config['ops']
        self._whitelist = []
        self._blacklist = []
        self.invoker = Invoker(self)
        self._register_commands()

    def _register_commands(self):
        # Register your command here
        self.invoker.register('wl', WhitelistCommand)
        self.invoker.register('bl', BlacklistCommand)
        self.invoker.register('goal', GoalCommand)

    def handle_command(self, username, command):
        if username in self.ops:
            self.invoker.invoke(command, user=username)

    def set_message_buffer(self, message):
        self.message_buffer.insert(self.config['misc']['chat_height'] - 1, message)
        self.message_buffer.pop(0)

    def audit_action(self, username, button):
        if self.invoker.has('wl'):
            if not self._whitelist:
                self._whitelist = self.invoker.invoke('wl')
                self._whitelist.load_whitelist()
            if self._whitelist.load_whitelist():
                if username.lower() in self._whitelist.load_whitelist():
                    self.game.push_button(button)
                    self.set_message_buffer({'username': username, 'button': button})
                    pbutton(self.message_buffer)
                else:
                    return
        if self.invoker.has('bl'):
            if not self._blacklist:
                self._blacklist = self.invoker.invoke('bl')
                self._blacklist.load_blacklist()
            if username.lower() not in self._blacklist.load_blacklist():
                self.game.push_button(button)
                self.set_message_buffer({'username': username, 'button': button})
                pbutton(self.message_buffer)
        else:
            self.game.push_button(button)
            self.set_message_buffer({'username': username, 'button': button})
            pbutton(self.message_buffer)

    def run(self):
        while True:
            new_messages = self.irc.recv_messages(1024)

            if not new_messages:
                continue

            for message in new_messages:
                username = message['username'].lower()
                if message['message'][0] == self.cmd_prefix:
                    self.handle_command(username, message['message'][1:])

                button = message['message'].lower()
                self.audit_action(username, button)
