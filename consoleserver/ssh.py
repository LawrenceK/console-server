#
# (C) Copyright L.P.Klyne 2013
#
"""This is based on the basic ssh server example, the protocol handler has been pulled out as a separate
source as this is where the logic for the console server sits.
"""
import logging
_log = logging.getLogger(__name__)
import os
import grp

from zope.interface import implements

from twisted.cred import portal
from twisted.conch import avatar
from twisted.conch.ssh import factory, userauth, connection, keys, session
from twisted.conch.checkers import SSHPublicKeyDatabase, UNIXPasswordDatabase
from twisted.python import components
from twisted.python import randbytes

from ssh_protocol import TSProtocol

import config

class TSAvatar(avatar.ConchUser):

    def __init__(self, username):
        avatar.ConchUser.__init__(self)
        self.username = username
        self.channelLookup.update({'session': session.SSHSession})

    def check_priviledged(self):
        """Test for membership of root or sudo groups, hence has admin ability"""
        def is_user_in_group(groupname):
            return self.username in grp.getgrnam(groupname)[3]

        print "TSAvatar.check_priviledged %s" % self.username
        _log.debug("TSAvatar.check_priviledged %s", self.username)
        return is_user_in_group("root") or is_user_in_group("sudo")


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
    services = {
        'ssh-userauth': userauth.SSHUserAuthServer,
        'ssh-connection': connection.SSHConnection
    }
    publickey_file = 'public.key'
    privatekey_file = 'private.key'
    publicKeys = {}
    privateKeys = {}

    def getRSAKeys(self):
        TSFactory.publickey_file = config.find_file( TSFactory.publickey_file, default = True )
        TSFactory.privatekey_file = config.find_file( TSFactory.privatekey_file, default = True )
        if not (os.path.exists(self.publickey_file) and os.path.exists(self.privatekey_file)):
            # generate a RSA keypair
            _log.info("Generating RSA keypair")
            from Crypto.PublicKey import RSA
            KEY_LENGTH = 1024
            rsaKey = RSA.generate(KEY_LENGTH, randbytes.secureRandom)
            # save keys for next time
            file(self.publickey_file, 'w+b').write(keys.Key(rsaKey).public().toString('OPENSSH'))
            file(self.privatekey_file, 'w+b').write(keys.Key(rsaKey).toString('OPENSSH'))

        TSFactory.publicKeys['ssh-rsa'] = keys.Key.fromString(data=file(self.publickey_file).read())
        TSFactory.privateKeys['ssh-rsa'] = keys.Key.fromString(data=file(self.privatekey_file).read())

    def __init__(self, consolecollection):
        self.consolecollection = consolecollection
        self.getRSAKeys()
# we then start the listen using TSFactory
