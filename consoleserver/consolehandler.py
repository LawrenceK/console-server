#
# (C) Copyright L.P.Klyne 2013
#
""" This is the protocol handler for the serial port(s) all data sent and received is written to
a per port logfile. The connection may be given a data callback which is used to connect the
port to an active ssh session.
"""
import logging
_log = logging.getLogger(__name__)
import inspect

from twisted.internet import reactor
from twisted.internet import serialport
from twisted.internet.protocol import Protocol


# Protocol handler
class ConsoleHandler(Protocol):
    LS_NONE = ' '
    LS_READ = '>'
    LS_WRITE = '<'

    def __init__(self, port_name, closed_callback=None, data_callback=None, **kwargs):
        _log.debug("Config %s: %s", port_name, kwargs)
        self.sshport = kwargs.pop('sshport', None)
        self.closed_callback = closed_callback
        self._data_callback = data_callback
        self.log_file = None
        self.logfile_name = kwargs.pop('logfile', None)
        self.last_log = ConsoleHandler.LS_NONE
        knownargs, _, _, _ = inspect.getargspec(serialport.SerialPort.__init__)

        self.serial_port = \
            serialport.SerialPort(self,
                                  port_name,
                                  reactor,
                                  **dict((k, v) for k, v in kwargs.iteritems() if k in knownargs)
                                  )

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

    def write_log(self, log_type, data):
        if not self.log_file and self.logfile_name:
            self.log_file = open(self.logfile_name, 'a')
            self.last_log = log_type
            self.log_file.write(self.last_log)
        if self.log_file:
            if log_type != self.last_log:
                self.last_log = log_type
                # CRLF ?
                self.log_file.write("\r\n")
                self.log_file.write(self.last_log)
            self.log_file.write(data.encode('string_escape'))

    def write(self, data):
        self.write_log(ConsoleHandler.LS_WRITE, data)
        self.transport.write(data)

    def connectionLost(self, reason):
        _log.debug("connectionLost")
        if self.log_file:
            self.log_file.close()
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
        self.write_log(ConsoleHandler.LS_READ, data)
        if self._data_callback:
            self._data_callback(data)
