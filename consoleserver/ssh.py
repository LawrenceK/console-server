#
#
#
"""This is from the basic ssh server example, the protocol handler has been pulled out as a separate
source as this is where the logic for the console server sits.
"""
import logging
_log = logging.getLogger(__name__)

from zope.interface import implements

from twisted.cred import portal
from twisted.conch import avatar
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.conch.checkers import SSHPublicKeyDatabase, UNIXPasswordDatabase
from twisted.python import components

from ssh_protocol import TSProtocol

publicKey = 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAGEArzJx8OYOnJmzf4tfBEvLi8DVPrJ3/c9k2I/Az64fxjHf9imyRJbixtQhlH9lfNjUIx+4LmrJH5QNRsFporcHDKOTwTTYLh5KmRpslkYHRivcJSkbh/C+BR3utDS555mV'

privateKey = """-----BEGIN RSA PRIVATE KEY-----
MIIByAIBAAJhAK8ycfDmDpyZs3+LXwRLy4vA1T6yd/3PZNiPwM+uH8Yx3/YpskSW
4sbUIZR/ZXzY1CMfuC5qyR+UDUbBaaK3Bwyjk8E02C4eSpkabJZGB0Yr3CUpG4fw
vgUd7rQ0ueeZlQIBIwJgbh+1VZfr7WftK5lu7MHtqE1S1vPWZQYE3+VUn8yJADyb
Z4fsZaCrzW9lkIqXkE3GIY+ojdhZhkO1gbG0118sIgphwSWKRxK0mvh6ERxKqIt1
xJEJO74EykXZV4oNJ8sjAjEA3J9r2ZghVhGN6V8DnQrTk24Td0E8hU8AcP0FVP+8
PQm/g/aXf2QQkQT+omdHVEJrAjEAy0pL0EBH6EVS98evDCBtQw22OZT52qXlAwZ2
gyTriKFVoqjeEjt3SZKKqXHSApP/AjBLpF99zcJJZRq2abgYlf9lv1chkrWqDHUu
DZttmYJeEfiFBBavVYIF1dOlZT0G8jMCMBc7sOSZodFnAiryP+Qg9otSBjJ3bQML
pSTqy7c3a2AScC/YyOwkDaICHnnD3XyjMwIxALRzl0tQEKMXs6hH8ToUdlLROCrP
EhQ0wahUTCk1gKA4uPD6TMTChavbh4K63OvbKg==
-----END RSA PRIVATE KEY-----"""


class TSAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})

    def is_member_of(self, groupname):
        """Test for membership of a user group and hence for priviledge levels"""
        _log.debug("TSAvatar.is_member_of %s", groupname)
        return True

class TSRealm:
    implements(portal.IRealm)

    def requestAvatar(self, avatarId, mind, *interfaces):
        return interfaces[0], TSAvatar(avatarId), lambda: None


class TSSession:
    implements(session.ISession)

    def __init__(self, avatar):
        self.avatar = avatar

    @property
    def factory(self):
        return self.conn.transport.factory

    def getPty(self, term, windowSize, attrs):
        pass

    def execCommand(self, proto, cmd):
        raise Exception("no executing commands")

    def openShell(self, protocol):
        _log.debug("openShell %s", protocol.getHost().address.port)
        # protocol is an SSHSessionProcessProtocol object
        # protocol.getHost().address.port
        # protocol.factory
        # protocol.transport
        # TODO if port is global sshport create CLI
        ts_protocol = TSProtocol(self.avatar)
        ts_protocol.makeConnection(protocol)
        protocol.makeConnection(session.wrapProtocol(ts_protocol))

    def windowChanged(newWindowSize):
        pass

    def eofReceived(self):
        pass

    def closed(self):
        pass

TS_portal = portal.Portal(TSRealm())
TS_portal.registerChecker(UNIXPasswordDatabase())
TS_portal.registerChecker(SSHPublicKeyDatabase())

components.registerAdapter(TSSession, TSAvatar, session.ISession)


class TSFactory(factory.SSHFactory):
    portal = TS_portal
    publicKeys = {
        'ssh-rsa': keys.Key.fromString(data=publicKey)
    }
    privateKeys = {
        'ssh-rsa': keys.Key.fromString(data=privateKey)
    }
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }

    def __init__(self, consolecollection):
        self.consolecollection = consolecollection
# we then start the listen using TSFactory
