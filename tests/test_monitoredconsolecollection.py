#
# (C) Copyright L.P.Klyne 2013
#
import os
import os.path
import logging
_log = logging.getLogger(__name__)

from StringIO import StringIO

import unittest
from dingus import patch, Dingus

from twisted.python.filepath import FilePath

from consoleserver import config
from consoleserver.monitoredconsolecollection import MonitoredConsoleCollection

test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'work'))


test_config = """[GLOBAL]
sshport = 8022
portbase = 8023

[/dev/ttyUSB0]
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 0
xonxoff = 0
rtscts = 1
sshport = 8023

[/dev/ttyUSB1]
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 0
xonxoff = 1
rtscts = 0
sshport = 8024
"""

class TestMonitoredConsoleCollection(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('twisted.internet.reactor.callLater', lambda t, f, cf: f(cf))  # so f is called now.
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_create(self):
        # patch so we know the notifier
        config.set_config(StringIO(test_config))
        inotify = Dingus()
        with patch('consoleserver.monitoredconsolecollection.INotify', Dingus(return_value=inotify)):
            collection = MonitoredConsoleCollection()
            name, args, kwargs, result = inotify.calls('watch')[0]
            self.assertEqual(2, len(args))
            self.assertEqual('/dev', args[0].path)
            name, args, kwargs, result = inotify.calls('startReading')[0]
            self.assertEqual(0, len(args))

            collection.created('ignored', FilePath('/dev/ttyUSB0'), 'mask')  # fake the notify
            self.assertEqual(1, len(collection))

            collection.created('ignored', FilePath('/dev/tty0'), 'mask')  # fake the notify
            self.assertEqual(1, len(collection))
