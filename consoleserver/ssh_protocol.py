#
# (C) Copyright L.P.Klyne 2013
#
""" This is the protocol handler for the ssh session(s), this may be connected at startup to a specific
serial port, the listsner was dedicated or it may be for the master port and therefore can be used
to reconfigure the console server and/or connect to a specific serial port.
"""
import logging
_log = logging.getLogger(__name__)
import os
import os.path

from twisted.internet import protocol
import config

cs_help = [
    "help",
    "list [list configuration entries]",
    "status [list open ports]",
    "exit",
    "create <portname>",
    "reload <portname>",
    "connect <portname>",
    "show <portname>",
    "stop <portname>",
    "start <portname>",
    "enable <portname> <0,1>",
    "baud <portname> <baud>",
    "bytesize <portname> <5,6,7,8>",
    "stopbits <portname> <1,2>",
    "parity <portname> <N,E,O,M,S>",
    "rtscts <portname> <0,1>",
    "xonxoff <portname> <0,1>",
    "sshport <portname> <nnnn>",
    "portmonitor <location>",
    "timeout <portname> <seconds>",
]

port_cmds = [
    "connect",
    "create",
    "connect",
    "show",
    "stop",
    "start",
    "enable",
    "baud",
    "bytesize",
    "stopbits",
    "parity",
    "rtscts",
    "xonxoff",
    "sshport",
    "timeout",
    "reload",
]


class TSProtocol(protocol.Protocol):
    """This is the control interface to the terminal server,
    it can be told to connect to a single port.
    """
    def __init__(self, avatar):
        self.avatar = avatar    # who are we
        self.ch = None
        self.buffer = b''

    def data_callback(self, data):
        """Callback from a serial port with data to be sent over ssh"""
        _log.debug("data_callback %s", data)
        self.transport.write(data)

    def do_attach(self, ch):
        if not ch or ch.is_attached:
            return False
        self.ch = ch
        self.ch.attach(self.data_callback)
        return True

    def connectionLost(self, reason):
        _log.debug("connectionLost")
        if self.ch:
            self.ch.detach()
        self.ch = None

    def goodbye(self, message='Good Bye'):
        self.send_lines([message])
        self.transport.loseConnection()

    def connectionMade(self):
        # Is this a ssh session on a port for direct connection
        if not self.do_attach(self.consolecollection.find_by_port(self.transport.getHost().address.port)):
            if self.avatar.check_priviledged():
                _log.debug("Running in CLI mode")
                self.send_cli_prompt()
            else:
                self.goodbye("User %s not allowed to administer the console server" % self.avatar.username)

    def send_lines(self, lines):
        _log.debug("send_lines %s", lines)
        for l in lines:
            self.transport.write(l)
            self.transport.write('\r\n')

    @property
    def consolecollection(self):
        return self.factory.consolecollection

    @property
    def factory(self):
        return self.transport.session.conn.transport.factory

    def process_connect(self, cfg):
        """look for connect request and validate, if we know the port then go into rawmode"""
        ch = self.consolecollection.find_by_name(cfg.name)
        if not ch:
            return["Cannot find console %s" % cfg.name, ]
        elif not self.do_attach(ch):
            return["Console already in use %s" % cfg.name, ]

    def process_baud(self, cfg, baudrate):
        cfg['baudrate'] = baudrate
        return self.process_show(cfg)

    def process_bytesize(self, cfg, bytesize):
        cfg['bytesize'] = bytesize
        return self.process_show(cfg)

    def process_parity(self, cfg, parity):
        cfg['parity'] = parity
        return self.process_show(cfg)

    def process_stopbits(self, cfg, stopbits):
        cfg['stopbits'] = stopbits
        return self.process_show(cfg)

    def process_rtscts(self, cfg, rtscts):
        cfg['rtscts'] = rtscts
        return self.process_show(cfg)

    def process_xonxoff(self, cfg, xonxoff):
        cfg['xonxoff'] = xonxoff
        return self.process_show(cfg)

    def process_enable(self, cfg, enable):
        cfg['enabled'] = enable
        if not enable:
            return self.process_stop(cfg)

    def process_timeout(self, cfg, timeout):
        cfg['timeout'] = timeout
        return self.process_show(cfg)

    def process_sshport(self, cfg, sshport):
        cfg['sshport'] = sshport
        return self.process_show(cfg)

    def process_logfile(self, cfg, logfile=None):
        cfg['logfile'] = logfile
        # path should be absolute or deemed relative to /var/log/consoleserver
        if cfg['logfile']:
            cfg['logfile'] = os.path.join('/var/log/consoleserver', cfg['logfile'])
            if not cfg['logfile'].endswith('.log'):
                cfg['logfile'] = cfg['logfile'] + '.log'
        return self.process_show(cfg)

    def process_status(self, message=None):
        return ["%s" % (k,) for k, v in self.consolecollection.items()]

    def process_list(self, message=None):
        ports = config.get_port_names()
        if message:
            ports.insert(0, message)
        return ports

    def process_help(self, message=None):
        if message:
            helpp = [message]
            helpp.extend(cs_help)
            return helpp
        return cs_help

    def process_show(self, cfg):
        return ["%s %s" % (k, v) for k, v in cfg.items()]

    def process_stop(self, cfg):
        ch = self.consolecollection.find_by_name(cfg.name)
        if not ch:
            return["Cannot find console %s" % cfg.name, ]
        ch.close()

    def process_start(self, cfg):
        if not cfg['enabled']:
            return["Console disabled %s" % cfg.name, ]
        ch = self.consolecollection.find_by_name(cfg.name)
        if ch:
            return["Console allready started %s" % cfg.name, ]
        self.consolecollection.open_port(cfg)

    def process_reload(self, cfg):
        # both commands return error message or None
        return self.process_stop(cfg) or self.process_start(cfg)

    def process_create(self, portname):
        # <portname>
        config.add_port(portname)
        # TODO open this port?
        return self.process_show(config.get_by_name(portname))

    def process_commit(self):
        config.commit()

    def process_exit(self):
        self.goodbye()

    def process_portmonitor(self, location):
        config.server()["monitorpath"] = location

    def process(self, line):
        # parse the line
        _log.info("Command '%s'" % line)
        args = line.split(" ")
        command = args.pop(0)
        f = getattr(self, "process_%s" % command, None)
        if not f:
            return ["Invalid command %s" % command]
        try:
            if command in port_cmds:
                if not args:
                    return self.process_help("Missing port name")
                portname = args.pop(0)
                # the second argument is always a port name
                cfg = config.get_by_name(portname)
                if cfg:
                    if command == 'create':
                        return self.process_list("Port allready exists %s" % portname)
                    return f(cfg, *args)
                elif command != 'create':
                    return self.process_list("No such port %s" % portname)
                return f(portname)
            return f(*args)
        except TypeError, ex:
            _log.exception("Incomplete/invalid command '%s'" % ex)
            return self.process_help("Incomplete/invalid command '%s'" % line)

    def send_cli_prompt(self):
        self.transport.write('>')

    def dataReceived(self, data):
        if self.ch:
            self.ch.write(data)
        else:
            self.transport.write(data)
            self.buffer += data
            self.buffer = self.buffer.replace('\r\n', '\n').replace('\r', '\n')
            parts = self.buffer.split('\n', 1)
            if len(parts) > 1:
                line, self.buffer = parts
                _log.info("command %s", line.encode('string_escape'))
                response = self.process(line)
                if self.ch:
                    # we have entered connected mode, any data still in buffer
                    self.ch.write(self.buffer)
                else:
                    self.send_lines(response or [])
                    self.send_cli_prompt()
