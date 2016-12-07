

class Invoker(object):

    def __init__(self, bot):
        self.commands = {}
        self.bot = bot
        self.irc = bot.irc

    def register(self, command, command_handler):
        self.commands[command] = command_handler

    def has(self, command):
        # Check command list by both command name and command handler
        return command in self.commands.keys() or command in self.commands.values()

    def list_commands(self):
        self.irc.msg_channel('Commands: {}'.format(self.commands.keys()))

    def invoke(self, command, user=None):
        command_str = command.split()
        cmd = command_str[0]
        if cmd == 'list':
            self.list_commands()
        elif cmd == 'help':
            self.irc.msg_channel('Type !list for a list of commands!')
        elif cmd in self.commands:
            return self.commands[cmd](self.bot).execute(user, command_str[1:])
