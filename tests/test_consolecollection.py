#
# (C) Copyright L.P.Klyne 2013
#
import logging
_log = logging.getLogger(__name__)
import os

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
sshport = 8023

[/dev/ttyUSB1]
baudrate = 9600
bytesize = 8
parity = N
stopbits = 1
timeout = 0
xonxoff = 0
rtscts = 0
sshport = 8024
"""

TEST_PUBLICKEYFILE = './public.key'
TEST_PRIVATEKEYFILE = './private.key'


class TestConsoleCollection(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_PUBLICKEYFILE):
            os.remove(TEST_PUBLICKEYFILE)
        if os.path.exists(TEST_PRIVATEKEYFILE):
            os.remove(TEST_PRIVATEKEYFILE)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_create(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', Dingus(return_value=listenTCP)):
            collection = ConsoleCollection()
            self.assertEqual(0, len(collection))

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_open_port(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', listenTCP):
            config.set_config(StringIO(test_config))
            collection = ConsoleCollection()
            collection.open_port(config.get_by_name('/dev/ttyUSB0'))
            self.assertEqual(1, len(listenTCP.calls))

            self.assertEqual(1, len(collection))
            ch = collection.find_by_name('/dev/ttyUSB0')
            self.assertIsInstance(ch, ConsoleHandler)

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_find_by_name(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', listenTCP):
            config.set_config(StringIO(test_config))
            collection = ConsoleCollection()
            collection.open_port(config.get_by_name('/dev/ttyUSB0'))
            self.assertEqual(1, len(listenTCP.calls))

            self.assertEqual(1, len(collection))
            ch = collection.find_by_name('/dev/ttyUSB0')
            self.assertIsInstance(ch, ConsoleHandler)
            ch = collection.find_by_name('/dev/ttyUSB1')
            self.assertEqual(None, ch)

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_find_by_port(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', listenTCP):
            config.set_config(StringIO(test_config))
            _log.debug("config %s", config.config)
            collection = ConsoleCollection()
            collection.open_port(config.get_by_name('/dev/ttyUSB0'))
            self.assertEqual(1, len(listenTCP.calls))

            self.assertEqual(1, len(collection))
            ch = collection.find_by_port(8023)
            self.assertIsInstance(ch, ConsoleHandler)
            ch = collection.find_by_port(8024)
            self.assertEqual(None, ch)

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_close_port(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', listenTCP):
            config.set_config(StringIO(test_config))
            collection = ConsoleCollection()
            collection.open_port(config.get_by_name('/dev/ttyUSB0'))
            self.assertEqual(1, len(listenTCP.calls))

            self.assertEqual(1, len(collection))
            collection.close_port('/dev/ttyUSB0')
            #TODO test invalid key

    @patch('ssh.TSFactory.publickey_file', TEST_PUBLICKEYFILE)
    @patch('ssh.TSFactory.privatekey_file', TEST_PRIVATEKEYFILE)
    @patch('twisted.internet.serialport.SerialPort', Dingus(return_value=Dingus()))
    def test_closed(self):
        listenTCP = Dingus()
        with patch('twisted.internet.reactor.listenTCP', listenTCP):
            config.set_config(StringIO(test_config))
            collection = ConsoleCollection()
            collection.open_port(config.get_by_name('/dev/ttyUSB0'))
            self.assertEqual(1, len(listenTCP.calls))

            ch = collection.find_by_name('/dev/ttyUSB0')
            self.assertIsInstance(ch, ConsoleHandler)

            self.assertEqual(1, len(collection))
            collection.closed(ch)
            self.assertEqual(0, len(collection))

#    def closed(self, closed_port):
