import logging
_log = logging.getLogger(__name__)
import os

class LogFile:
    LS_NONE = ' '
    LS_READ = '>'
    LS_WRITE = '<'

    def __init__(self, logfile):
        _log.debug("LogFile %s", logfile)
        self.lastport = ""
        self.refcount = 0
        self.log_file = None
        self.logfile_name = os.path.abspath(logfile)
        self.last_log = LogFile.LS_NONE

    def write_log(self, log_type, port_name, data):
        if not self.log_file:
            self.log_file = open(self.logfile_name, 'a')
            self.last_log = log_type
            self.log_file.write(self.last_log)
        if log_type != self.last_log or self.lastport != port_name: 
            self.last_log = log_type
            self.lastport = port_name
            # CRLF ?
            self.log_file.write("\r\n")
            self.log_file.write("%s %s", % self.lastport, self.last_log)
        self.log_file.write(data.encode('string_escape'))
        self.log_file.flush()

    def access(self):
        self.refcount = self.refcount + 1

    def deaccess(self):
        self.refcount = self.refcount - 1
        if ( self.refcount == 0 ) and self.log_file:
            self.log_file.close()
            self.log_file = None

