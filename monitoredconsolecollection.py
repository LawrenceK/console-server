#
# (C) Copyright L.P.Klyne 2013
#
""" This extends the console collection to monitor for serial ports being connected
to this system, USB hot plug.
"""
import logging
_log = logging.getLogger(__name__)

from twisted.python.filepath import FilePath
from twisted.internet.inotify import IN_CREATE, INotify

from consolecollection import ConsoleCollection
import config


class MonitoredConsoleCollection(ConsoleCollection):
    """This monitors for new serial ports being created (USB plugged in) and
    makes the ports available."""
    def __init__(self, location='/dev'):
        notifier = INotify()
        notifier.watch(FilePath(location), IN_CREATE, callbacks=[self.created])
        notifier.startReading()

    def created(self, ignored, path, mask):
        _log.info("New entry created %s", path.path)
        cf = config.get_by_name(path.path)
        if cf:
            self.open_port(cf.name, cf)
