import logging
_log = logging.getLogger(__name__)

from StringIO import StringIO

import unittest
import config

#from dingus import patch

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


class TestConFig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load(self):
        config.set_config(StringIO(test_config))
        cfg = config.get_by_name("/dev/ttyUSB0")
        _log.debug("config ttyUSB0 %s", cfg)
        self.assertEqual(9600, cfg['baudrate'])
        self.assertEqual(8, cfg['bytesize'])
        self.assertEqual('N', cfg['parity'])
        self.assertEqual(1, cfg['stopbits'])
        self.assertEqual(0, cfg['timeout'])
        self.assertEqual(False, cfg['xonxoff'])
        self.assertEqual(True, cfg['rtscts'])
