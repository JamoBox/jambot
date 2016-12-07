from lib.command import Command


class WhitelistCommand(Command):

    def __init__(self, bot):
        self._bot = bot
        self._irc = bot.irc
        self._whitelist_file = self._bot.config['whitelist']
        self.whitelist = []
        self.load_whitelist()

    def add(self, people):
        if people:
            for person in people:
                if person not in self.whitelist:
                    self.whitelist.append(person.lower())
                else:
                    self._irc.msg_channel('{0} is already in whitelist'
                                          .format(person.lower()))
            self.save_whitelist(self.whitelist)
        else:
            self._irc.msg_channel('No people specified!')

    def remove(self, people):
        if people:
            for person in people:
                if person in self.whitelist:
                    self.whitelist.remove(person.lower())
                else:
                    self._irc.msg_channel('{0} is not in whitelist'
                                          .format(person.lower()))
            self.save_whitelist(self.whitelist)
        else:
            self._irc.msg_channel('No people specified!')

    def clear(self):
        self.whitelist = []
        self.save_whitelist(self.whitelist)
        self.list()

    def save_whitelist(self, whitelist):
        fd = open(self._whitelist_file, 'w+')
        for person in self.whitelist:
            fd.write('{0}\n'.format(person.lower()))
        fd.flush()
        fd.close()
        return self.whitelist

    def load_whitelist(self):
        fd = open(self._whitelist_file, 'r')
        self.whitelist = fd.read().split()
        fd.close()
        return self.whitelist

    def list(self):
        self._irc.msg_channel('Whitelist: {}'.format(self.whitelist))

    def execute(self, user, params):
        if params:
            cmd = params[0]
            if cmd == 'add':
                self.add(params[1:])
            elif cmd == 'remove':
                self.remove(params[1:])
            elif cmd == 'list':
                self.list()
            elif cmd == 'clear':
                self.clear()
            else:
                self._irc.msg_channel('Invalid whitelist command!')
        return self
