from lib.command import Command
from config.irc_config import IrcConfig

class ListCommand(Command):

    def __init__(self, bot):
        self._irc = bot.irc

    def list_commands(self):
        self._irc.msg_channel('Commands: {}'.format(self.commands.keys()))

    def execute(self, user, *args):
        self.list_commands()
