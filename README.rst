=========================
Console Server
=========================
-------------------------
Lawrence Klyne
-------------------------

This is a console server. It can connect to 1 or more serial ports and make these available over SSH.
The data to and from the serial port can be logged to local disk. There is also a cli interface
that can be used to reconfigure the serial ports.

The reason for writing this is the off the self solutions, Cyclades etc., are not cheap, a similar 
solution can be acheived using a raspberry pi and readily available usb to serial adaptors.
e.g. this 16 port one for under £200
http://www.easysync-ltd.com/product/636/usb2-h-1016-m.html

A write up about this can be found on http://www.klyne.org/console-server.html an update is to follow.

Authentication
--------------
Version 0.2 and later uses unix password file and users authorised keys for 
logon.


Priviledges
=============

The consoleserver has to run as root currently to access password file for user authentication
to work at ssh login.

The CLI interface is only allowed by users who are members of the groups root or sudo.

Issues
---------

USB hot plug
=============

On ubuntu modem-manager is run against all serial ports to probe for it being a modem, 
this interferes with the monitored console collection. You may want to add a blacklist udev
rule to prevent this. 99-usb-blacklist.rules is a sample rule file and goes into /etc/udev/rules.d

Group membership
=================

By default serial devices belong to the dialout group so the user running the console server needs to 
be a member of this group or to run as root.

CLI Interface
-------------
There is a CLI interface accessible over SSH that can be used to reconfigure the server and serial ports,
as of version 0.3 this can only be accessed by users belonging to the root or sudo groups - i.e. they
have admin rights on the server. This by default is on port 8022 so ssh -p <username>@<address>.

The configuration of active serial ports is not acted on immediatly issue reload <port name> this is so
you can change multiple parameters. 

Configuration changes are not committed to disk until they are committed using the commit command. This
allows for temporary changes to try and get a port working.

Port names are the full device name, i.e. /dev/ttyUSB0

Commands
==========

help
    Simple help.

list
    List configured ports, these may not all exists on the system.

status
    Show active ports.

exit
    exit and close CLI connection.

create <portname>
    Create a new port configuration in the config file. The default config already lists 32 ports.

reload <portname>
    Close and reopen the named port

show <portname>
    Show current configuration of the port

stop <portname>
    Close the port

start <portname>
    Open the port

enable <portname> <0,1>
    Mark port for auto open as soon as it is seen. Note it may be a USB device that is not yet plugged in but
    will be opened once plugged in.

baud <portname> <baud>
    Change port baud rate.

bytesize <portname> <5,6,7,8>
    Change port number of data bits.

stopbits <portname> <1,2>",
    Change port number of stop bits.

parity <portname> <N,E,O,M,S>",
    Change port parity, None, Even, Odd, Mark, Space.

rtscts <portname> <0,1>",
    Change port to use RTSCTS for flow control - hardware flow control.

xonxoff <portname> <0,1>",
    Change port to use XON XOFF for flow control - software flow control.

sshport <portname> <nnnn>",
    Change ssh port that directly connects to the serial port.

logfile <portname> <logfile>",
    NOTE loggign has been rewored and to chnage logfiles names and locations you will need to edit
    the logfile.ini and then restart the consoleserver, this allows the easier management of logfiles.

portmonitor <location>
    Change the directory to monitor for new serial ports, the port (device) names must already exist in the config for
    the consoleserver to open them as soon as they are plugged in.

Installation
--------------
The package is set up to install on Ubuntu at present dropping relevnt files where required on the
file system. You should be able to install and then enter sudo /etc/init.d/consoleserver start
to get it running as a daemon. sudo consoleserver will run it in a terminal window logging to the screen.

File locations
--------------
The system looks for config files in i) current directory, ~/.consoleserver (Posix) and
/etc/consoleserver. If not found it will use the defaults in the python source directory.


Config File
=============

The system will create a default config file in /etc/consoleserver called config.ini this will be created
to access serial ports ttyUSB0..ttyUSB31. The default management port is 8022 and the 
default serial ports are on 8023..8054. 

If the sshport is not given for a port then no ssh listener is started for that serial port.

LogFiles
===========

A change with V1.0 was to use python logging to handle all logging, there is now a configuration
file (logging.ini) which is passed to fileconfig to setup the logging streams. The logging 
handler names are generated from the the numeric suffix of the port names, i.e. port.11 for ttyUSB11.

Others
===========

    /etc/init.d/consoleserver
    /etc/udev/rules.d/99-usb-blacklist.rules

You will have to make /etc/init.d/consoleserver executable if you wish to run this as a daemon.

Unit Tests
----------

Most of the code is unit tested.

PYTHONPATH=../consoleserver nosetests

Licence
--------------

The code is licenced using the GPL, see included LICENCE file. At present any other licence is subject to negotiation.

\(C\) Copyright L P Klyne 2013-2015

