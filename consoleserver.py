import logging
_log = logging.getLogger(__name__)

from twisted.internet import reactor

import config
from monitoredconsolecollection import MonitoredConsoleCollection
from ssh import TSFactory


def console_server(consoles=None):
    if not consoles:
        consoles = MonitoredConsoleCollection(location=config.server().get("monitorpath", None))
        consoles.open_all()

    # create listening ssh session with cli
    ts_factory = TSFactory(consoles)
    reactor.listenTCP(config.server().get("sshport", 8022), ts_factory)
