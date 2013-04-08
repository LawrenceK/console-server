import logging
_log = logging.getLogger(__name__)

from twisted.internet import reactor

import config
from monitoredconsolecollection import MonitoredConsoleCollection
from consolecollection import ConsoleCollection
from ssh import TSFactory


def console_server(consoles=None):
    if not consoles:
        location = config.server().get("monitorpath", None)
        if location:
            consoles = MonitoredConsoleCollection(location=location)
        else:
            consoles = ConsoleCollection()
        consoles.open_all()

    # create listening ssh session with cli
    reactor.listenTCP(config.server().get("sshport", 8022), TSFactory(consoles))
