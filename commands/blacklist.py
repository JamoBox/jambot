from lib.command import Command


class BlacklistCommand(Command):

    def __init__(self, bot):
        self._bot = bot
        self._irc = bot.irc
        self._blacklist_file = self._bot.config['blacklist']
        self.blacklist = []
        self.load_blacklist()

    def add(self, people):
        if people:
            for person in people:
                if person not in self.blacklist:
                    self.blacklist.append(person.lower())
                else:
                    self._irc.msg_channel('{0} is already in blacklist'
                                          .format(person.lower()))
            self.save_blacklist(self.blacklist)
        else:
            self._irc.msg_channel('No people specified!')

    def remove(self, people):
        if people:
            for person in people:
                if person in self.blacklist:
                    self.blacklist.remove(person.lower())
                else:
                    self._irc.msg_channel('{0} is not in blacklist'
                                          .format(person.lower()))
            self.save_blacklist(self.blacklist)
        else:
            self._irc.msg_channel('No people specified!')

    def clear(self):
        self.blacklist = []
        self.save_blacklist(self.blacklist)
        self.list()

    def save_blacklist(self, blacklist):
        fd = open(self._blacklist_file, 'w+')
        for person in self.blacklist:
            fd.write('{0}\n'.format(person.lower()))
        fd.flush()
        fd.close()
        self.load_blacklist()
        return self.blacklist

    def load_blacklist(self):
        fd = open(self._blacklist_file, 'r')
        self.blacklist = fd.read().split()
        fd.close()
        return self.blacklist

    def list(self):
        self._irc.msg_channel('Blacklist: {}'.format(self.blacklist))

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
                self._irc.msg_channel('Invalid blacklist command!')
        return self
