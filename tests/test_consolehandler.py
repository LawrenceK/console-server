import sys, os, os.path
import logging

import unittest
import consolehandler

from dingus import patch

#
class TestConsoleHandler(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('twisted.internet.serialport.SerialPort')
    def test_create(self):
        logfile_name = 'test_port.log'
        config = dict(port='test_port',
                logfile=logfile_name,
                baudrate=9600, 
    #            bytesize=serialport.EIGHTBITS, 
    #            parity=serialport.PARITY_NONE, 
    #            stopbits=serialport.STOPBITS_ONE, 
    #            timeout=0, 
    #            xonxoff=0, 
    #            rtscts=0
        )
        if os.path.exists(logfile_name):
            os.remove(logfile_name)

        c = consolehandler.ConsoleHandler(config['port'], **config)
        print c.serial_port

        c.connectionMade()

        for i in range(10):
            c.dataReceived('test %s\n' % i)

        c.connectionLost('shutdown')

        self.failUnless(os.path.exists(logfile_name))
        self.failUnless(os.path.getsize(logfile_name) > 0)
