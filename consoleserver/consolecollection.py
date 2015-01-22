#
# (C) Copyright L.P.Klyne 2013
#
""" This manages a set of active console handlers.
"""
import logging
_log = logging.getLogger(__name__)
import os.path

from twisted.internet import reactor

import config
from consolehandler import ConsoleHandler
from ssh import TSFactory


class ConsoleCollection(dict):
    def open_port(self, config):
        if config.name in self:
            raise ValueError('port %s already open' % config.name)
        try:
            self[config.name] = ConsoleHandler(config.name, closed_callback=self.closed, **config)
            # start an ssh listener for this port
            if self[config.name].sshport:
                self[config.name].listener = reactor.listenTCP(self[config.name].sshport, TSFactory(self))
        except Exception:
            _log.exception("open_port %s failed", config.name)

    def closed(self, closed_port):
        for port_name, port in self.items():
            if port == closed_port:
                del self[port_name]
                return

    def close_port(self, port_name):
        self.pop(port_name).close()

    def find_by_name(self, port_name):
        return self.get(port_name, None)

    def find_by_port(self, port_nr):
        handlers = [v for v in self.itervalues() if v and v.sshport == port_nr]
        if handlers:
            return handlers[0]
        return None

    def open_all(self):
        for port_name in config.get_port_names():
            cfg = config.get_by_name(port_name)
            if cfg['enabled']:
                if os.path.exists(port_name):
                    self.open_port(cfg)
                else:
                    _log.debug("Port %s does not yet exist", port_name)
            else:
                _log.debug("Port %s disabled", port_name)
