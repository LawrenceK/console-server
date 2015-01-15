#
# (C) Copyright L.P.Klyne 2013
#
""" This is the protocol handler for the serial port(s) all data sent and received is written to
a per port logfile. The connection may be given a data callback which is used to connect the
port to an active ssh session.
"""
import logging
_log = logging.getLogger(__name__)
import os
import inspect

from twisted.internet import reactor
from twisted.internet import serialport
from twisted.internet.protocol import Protocol

from logfile import LogFile

# Protocol handler
class ConsoleHandler(Protocol):
    def __init__(self, port_name, closed_callback=None, data_callback=None, logger=None, **kwargs):
        _log.debug("Config %s: %s", port_name, kwargs)
        self.sshport = kwargs.pop('sshport', None)
        self.closed_callback = closed_callback
        self._data_callback = data_callback
        self.log = logger
        if self.log == None:
            self.log = LogFile(os.path.abspath(kwargs.pop('logfile', os.path.basename(port_name))))
        self.log.access()
        knownargs, _, _, _ = inspect.getargspec(serialport.SerialPort.__init__)

        self.serial_port = \
            serialport.SerialPort(self,
                                  port_name,
                                  reactor,
                                  **dict((k, v) for k, v in kwargs.iteritems() if k in knownargs)
                                  )
        self.port_name = os.path.basename(self.serial_port.name)

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

    def write(self, data):
        self.log.write_log(LogFile.LS_WRITE, self.port_name, data)
        self.transport.write(data)

    def connectionLost(self, reason):
        _log.debug("connectionLost")
        self.log.deaccess()
        if self.closed_callback:
            self.closed_callback(self)
        self.close()

    def connectionMade(self):
        _log.debug("connectionMade")

    def dataReceived(self, data):
        _log.debug("dataReceived %s", data)
        # write to log file
        # are we connected to telnet
        # send data
        self.log.write_log(LogFile.LS_READ, self.port_name, data)
        if self._data_callback:
            self._data_callback(data)
