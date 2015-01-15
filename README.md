(C) Copyright L P Klyne 2013

This is a console server. It can connect to 1 or more serial ports and make these available over SSH.
The data to and from the serial port will be logged to local disk. There is also a cli interface
that can be used to reconfigure the serial ports.

The reason for writing this is the off the self solutions, Cyclades etc., are not cheap, a similar 
solution can be acheived using a raspberry pi and readily available usb to serial adaptors.
e.g. this 16 port one for under £200
http://www.easysync-ltd.com/product/636/usb2-h-1016-m.html

Authentication
--------------
Version 0.2 uses unix password file and users authorised keys for logon therefore the console server
has to run as root to get access to the relevant files.

Issues with USB hot plug
------------------------
On ubuntu modem-manager is run against all serial ports to probe for it being a modem, 
this interferes with the monitored console collection. You may want to add a blacklist udev
rule to prevent this. 99-usb-blacklist.rules is a sample rule file and goes into /etc/udev/rules.d

Group membership
----------------
By default serial devices belong to the dialout group so the user running the console server needs to 
be a member of this group or to run as root.

Unit Tests
----------
Most of the code is unit tested.

To run them 
cd tests
PYTHONPATH=../consoleserver python testAll.py
