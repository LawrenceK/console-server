#
# (C) Copyright L.P.Klyne 2013
#
import logging
_log = logging.getLogger(__name__)

import unittest
from dingus import patch, Dingus
from StringIO import StringIO

from consolehandler import ConsoleHandler
from consolecollection import ConsoleCollection
import config

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
rtscts = 0
sshport = 8022

[/dev/ttyUSB1]
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 0
xonxoff = 0
rtscts = 0
sshport = 8023
"""


class TestConsoleCollection(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_create(self):
        collection = ConsoleCollection()
        self.assertEqual(0, len(collection))

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_open_port(self):
        config.set_config(StringIO(test_config))
        collection = ConsoleCollection()
        collection.open_port('/dev/ttyUSB0', config.get_by_name('/dev/ttyUSB0'))

        self.assertEqual(1, len(collection))
        ch = collection.find_by_name('/dev/ttyUSB0')
        self.assertIsInstance(ch, ConsoleHandler)

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_find_by_name(self):
        config.set_config(StringIO(test_config))
        collection = ConsoleCollection()
        collection.open_port('/dev/ttyUSB0', config.get_by_name('/dev/ttyUSB0'))

        self.assertEqual(1, len(collection))
        ch = collection.find_by_name('/dev/ttyUSB0')
        self.assertIsInstance(ch, ConsoleHandler)
        ch = collection.find_by_name('/dev/ttyUSB1')
        self.assertEqual(None, ch)

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_find_by_port(self):
        config.set_config(StringIO(test_config))
        _log.debug("config %s", config.config)
        collection = ConsoleCollection()
        collection.open_port('/dev/ttyUSB0', config.get_by_name('/dev/ttyUSB0'))

        self.assertEqual(1, len(collection))
        ch = collection.find_by_port(8022)
        self.assertIsInstance(ch, ConsoleHandler)
        ch = collection.find_by_port(8023)
        self.assertEqual(None, ch)

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_close_port(self):
        config.set_config(StringIO(test_config))
        collection = ConsoleCollection()
        collection.open_port('/dev/ttyUSB0', config.get_by_name('/dev/ttyUSB0'))

        self.assertEqual(1, len(collection))
        collection.close_port('/dev/ttyUSB0')
        #TODO test invalid key

    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_closed(self):
        config.set_config(StringIO(test_config))
        collection = ConsoleCollection()
        collection.open_port('/dev/ttyUSB0', config.get_by_name('/dev/ttyUSB0'))

        ch = collection.find_by_name('/dev/ttyUSB0')
        self.assertIsInstance(ch, ConsoleHandler)

        self.assertEqual(1, len(collection))
        collection.closed(ch)
        self.assertEqual(0, len(collection))

#    def closed(self, closed_port):
