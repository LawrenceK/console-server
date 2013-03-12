import logging
_log = logging.getLogger(__name__)

import unittest
from StringIO import StringIO

from dingus import patch, Dingus

import config
from ssh_protocol import TSProtocol

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


class TestTsProtocol(unittest.TestCase):

    def setUp(self):
        self.tsprotocol = TSProtocol()
        self.tsprotocol.transport = Dingus()

    def tearDown(self):
        pass

    def test_list(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("list")
        self.failUnless(isinstance(result, list))
        self.assertEqual(2, len(result))

    def test_show(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("show /dev/ttyUSB0")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))

    def test_create(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("create /dev/ttyUSB2")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual(3, len(config.get_port_names()))

    def test_baud(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("baud /dev/ttyUSB0 19200")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('baudrate 19200', result[0])

    def test_bytesize(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("bytesize /dev/ttyUSB0 7")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('bytesize 7', result[1])

#    @patch('config.config', ConfigObj(StringIO(test_config)))
    def test_parity(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("parity /dev/ttyUSB0 E")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('parity E', result[2])

    def test_stopbits(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("stopbits /dev/ttyUSB0 2")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('stopbits 2', result[3])

    def test_rtscts(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("rtscts /dev/ttyUSB0 1")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('rtscts 1', result[6])

    def test_xonxoff(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("xonxoff /dev/ttyUSB0 1")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('xonxoff 1', result[5])

    def test_timeout(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("timeout /dev/ttyUSB0 300")
        self.failUnless(isinstance(result, list))
        self.assertEqual(8, len(result))
        self.assertEqual('timeout 300', result[4])

    def test_commit(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("commit")
        self.failUnless(result is None)

    def test_connect(self):
        config.set_config(StringIO(test_config))
        result = self.tsprotocol.process("connect /dev/ttyUSB0")
        self.failUnless(result is None)
        self.failUnless(self.tsprotocol.ch is not None)

        name, args, kwargs, result = self.tsprotocol.consolecollection.calls('find_by_name')[0]
        self.assertEqual('/dev/ttyUSB0', args[0])

#    @patch('ssh_protocol.TSProtocol.sendLine')
    def test_sendlines(self):
        self.tsprotocol.send_lines(['a', 'b'])
        # 2 output entries and two line terms.
        self.assertEqual(4, len(self.tsprotocol.transport.write.calls))

#    @patch('ssh_protocol.TSProtocol.sendLine')
    def test_line_mode(self):
        # test that a new protocol handler started on the global port is in
        # line mode.
        self.tsprotocol.dataReceived('show /dev/ttyUSB0\r\n')
        # 8 lines from show, 8 line terms, and one cli prompt
        self.assertEqual(17, len(self.tsprotocol.transport.write.calls))

#    @patch('ssh_protocol.TSProtocol.sendLine')
    def test_raw_mode(self):
        # test that a protocol handler that has been connected is in raw mode.
        self.test_connect()
        self.tsprotocol.dataReceived('show /dev/ttyUSB0\r\n')
        self.assertEqual(0, len(self.tsprotocol.transport.write.calls))

        name, args, kwargs, result = self.tsprotocol.ch.calls('write')[0]
        self.assertEqual('show /dev/ttyUSB0\r\n', args[0])
