#
# (C) Copyright L.P.Klyne 2013
#
""" This is the protocol handler for the serial port(s) all data sent and received is written to
a per port logfile. The connection may be given a data callback which is used to connect the
port to an active ssh session.
"""
import os
import logging
_log = logging.getLogger(__name__)
import inspect

from twisted.internet import reactor
from twisted.internet import serialport
from twisted.internet.protocol import Protocol


# Protocol handler
class ConsoleHandler(Protocol):
    def __init__(self, port_name, closed_callback=None, data_callback=None, **kwargs):
        _log.debug("Config %s: %s", port_name, kwargs)
        self.sshport = kwargs.pop('sshport', None)
        self.closed_callback = closed_callback
        self._data_callback = data_callback
        knownargs, _, _, _ = inspect.getargspec(serialport.SerialPort.__init__)

        self.serial_port = \
            serialport.SerialPort(self,
                                  port_name,
                                  reactor,
                                  **dict((k, v) for k, v in kwargs.iteritems() if k in knownargs)
                                  )
        self.port_name = os.path.basename(port_name)
#        self.port_name = os.path.basename(self.serial_port.name)
        self.portlog = logging.getLogger("port.%s" % self.port_name)

    @property
    def is_attached(self):
        return self._data_callback is not None

    def attach(self, data_callback):
        self._data_callback = data_callback

    def detach(self):
        self._data_callback = None

    def close(self):
        _log.debug("close")
        if self.serial_port:
            self.serial_port.loseConnection()
            self.serial_port = None
        if self.sshport:
            self.listener.stopListening()

    def do_log(self, inbound, data):
        self.portlog.info(data)

    def write(self, data):
        # from ssh?
        self.do_log(False, data)
        self.transport.write(data)

    def connectionLost(self, reason):
        _log.debug("connectionLost")
        if self.closed_callback:
            self.closed_callback(self)
        self.close()

    def connectionMade(self):
        _log.debug("connectionMade")

    def dataReceived(self, data):
        _log.debug("dataReceived %s", data)
        self.do_log(True, data)
        if self._data_callback:
            # to ssh?
            self._data_callback(data)
