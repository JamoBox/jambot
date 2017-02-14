from lib.base import JamBase


class IrcAccount(JamBase):

    def __init__(self,
                 server,
                 nickname,
                 username,
                 password,
                 hostname='-',
                 servername='-',
                 realname='JamBot'):

        JamBase.__init__(self)

        self.server = server
        self.nickname = nickname
        self.username = username
        self.password = password
        self.hostname = hostname
        self.servername = servername
        self.realname = realname


    def _authenticate_to_server(self):
        # Must be sent in order of PASS, NICK, USER
        self.server.send('PASS {password}'
                         .format(password=self.password))
        self.server.send('NICK {nickname}'
                         .format(nickname=self.nickname))
        self.server.send('USER {username} {hostname} {servername} :{realname}'
                         .format(username=self.username,
                                 hostname=self.hostname,
                                 servername=self.servername,
                                 realname=self.realname))
