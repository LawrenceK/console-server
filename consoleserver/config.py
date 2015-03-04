#
# (C) Copyright L.P.Klyne 2013
#
""" This handles the console server configuration. It uses a configuration spec file.
"""
import logging
_log = logging.getLogger(__name__)
import os
import os.path

from configobj import ConfigObj
from validate import Validator

# these are the valid values
dict(bytesize="5,6,7,8",
     stopbits="1,1.5,2",
     parity="N,E,O,M,S",
     timeout="float",
     xonxoff="0,1",  # true, false
     rtscts="0,1")  # true, false

default = dict(enabled=1,
               baudrate=9600,
               bytesize=8,
               parity='N',
               stopbits=1,
               timeout=0,
               xonxoff=0,
               rtscts=0,
               sshport=0)


config = None
configspec = """[GLOBAL]
sshport = integer(default=8022)
portbase = integer(default=8023)
opendelay = integer(default=2)

[__many__]
baudrate = integer()
bytesize = integer(min=5, max=8, default=8)
parity = option('N', 'E', 'O', 'M', 'S')
stopbits = integer(min=1, max=2, default=1)
timeout = float()
interChartimeout = float()
xonxoff = boolean(default=False)
rtscts = boolean(default=False)
enabled = boolean(default=True)
sshport = integer()
logtype = integer()
""".split('\n')

default_config = """[GLOBAL]
sshport = 8022
""".split('\n')


def set_config(infile):
    global config
    config = ConfigObj(infile, configspec=configspec)
    result = config.validate(Validator())
    if not result:
        _log.error("config.ini invalid %s", config)
    _log.info("ports %s", config.keys())

set_config(default_config)


def commit():
    config.write()


def server():
    return config.get('GLOBAL', {})


def add_port(port_name, commit_new=False):
    if port_name not in config:
        config[port_name] = dict(default)
        result = config.validate(Validator())
        if not result:
            _log.error("config.ini invalid %s", config)
        if commit_new:
            config.write()
    return config[port_name]


def get_by_name(port_name):
    if port_name in config:
        _log.info("get_by_name %s", port_name)
        return config[port_name]
    _log.error("get_by_name not found %s", port_name)
    return None


def get_names_from_port(port_nr):
    return [k for k, v in config.iteritems() if k != "GLOBAL" and "sshport"in v and v['sshport'] == port_nr]


def get_port_names():
    """return a list of all port names in the configuration file"""
    return [k for k in config.keys() if k != "GLOBAL"]

def find_file( basename, default = False ):
    fname = os.path.abspath(basename)   # current directory
    _log.info("look for %s in %s", basename, fname)
    if os.path.exists(fname):
        return fname
    if os.name == "posix":
        fname = os.path.abspath(os.path.expanduser(os.path.join("~", ".consoleserver", basename)))   # users home directory
        _log.info("look for %s in %s", basename, fname)
        if os.path.exists(fname):
            return fname
        _log.info("look for %s in %s", basename, fname)
        fname = os.path.join("/etc", "consoleserver", basename)   # system directory
        if os.path.exists(fname):
            return fname
    _log.info("look for %s in %s", basename, fname)
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), basename)   # python directory
    if os.path.exists(fname):
        return fname
    if default:
        return os.path.abspath(basename)
    return None

