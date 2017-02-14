from lib.command import Command
from config.irc_config import IrcConfig

class GoalCommand(Command):

    def __init__(self, bot):
        self._irc = bot.irc
        self._invoker = bot.invoker
        self.goal = ''
        self._goal_file = config.goal
        self.load_goal()
        self._ops = config.ops

    def save_goal(self):
        fd = open(self._goal_file, 'w+')
        fd.write(self.goal)
        fd.flush()
        fd.close()
        return self.goal

    def load_goal(self):
        fd = open(self._goal_file, 'r')
        self.goal = fd.readline()
        fd.close()
        return self.goal

    def execute(self, user, args):
        if args:
            if user in self._ops:
                self.goal = ''
                for word in args:
                    self.goal += '{} '.format(word)
                self.save_goal()
        self._irc.msg_channel('Current goal: {}'.format(self.goal))
