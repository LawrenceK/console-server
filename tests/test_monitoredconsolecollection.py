#
# (C) Copyright L.P.Klyne 2013
#
import os
import os.path
import logging
_log = logging.getLogger(__name__)

import unittest
from dingus import patch, Dingus

from twisted.python.filepath import FilePath

from monitoredconsolecollection import MonitoredConsoleCollection

test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'work'))


class TestMonitoredConsoleCollection(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create(self):
        new_ports = []

        def callback(port_name):
            new_ports.append(port_name)

# need to mock/patch this
# reactor.callLater(config.server().get("opendelay", 2), self.open_port, cf)

        # patch so we know the notifier
        inotify = Dingus()
        with patch('monitoredconsolecollection.INotify', Dingus(return_value=inotify)):
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
