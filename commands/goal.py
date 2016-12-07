from lib.command import Command
from config.config import config

class GoalCommand(Command):

    def __init__(self, bot):
        self._irc = bot.irc
        self._invoker = bot.invoker
        self.goal = ''
        self._goal_file = config['goal']
        self.load_goal()
        self._ops = config['ops']

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

    def execute(self, user, params):
        if params:
            if user in self._ops:
                self.goal = ''
                for word in params:
                    self.goal += '{} '.format(word)
                self.save_goal()
        self._irc.msg_channel('Current goal: {}'.format(self.goal))