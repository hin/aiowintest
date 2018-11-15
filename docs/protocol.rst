=====================
The Win-Test Protocol
=====================

The Win-Test protocol is based on UDP broadcast packets, by default sent to the
local broadcast address at port 9871.

There is some partial documentation of the Win-Test protocol here:
http://download.win-test.com/utils/SummaryBroadcastingSpecs.txt

This protocol documentation was made by reading the documentation above,
and by reverse engineering the protocol using Wireshark and python code.

The resulting documentation, python code and everything else related to this
project  has no affiliation with the Win-Test developers.
It has been created out of personal curiosity and is presented in the hope that
it may be useful or at least amusing to others.

Any further insights and/or corrections to this project is greatly appreciated.
Please get in touch via https://github.com/hin/aiowintest

Payload structure
=================

The payload structure is mostly an ASCII-encoded string followed by a checksum
and an optional null-character.

The structure of the payload is as follows:

============ ======
field        type
============ ======
frame_type   string
:            colon delimiter (ascii 58)
space        space delimiter (ascii 32)
from_station string
space        space delimiter (ascii 32)
to_station   string
space        space delimiter (ascii 32)
data[0]      data field
space        space delimiter (ascii 32)
data[1]      data field
space        space delimiter (ascii 32)
...
data[n]      data field
checksum     byte
null         null character with unknown purpose (optional)
============ ======

For some packets, the payload also contains a null (0x00) character at the
end. According to the limited protocol documentation I've
found, it should not be there, and I've not been able to find any purpose
of it. It may simply be a bug in the Win-Test software.

For now, I check for the extra null character and ignore it if it exists.

Checksum calculation
====================

When sending a packet, the checksum is calculated as:
    (sum of all bytes) | 128 % 256

In python, this can be calculated as:

.. code-block:: python3

    def checksum(data):
        return (sum(data)|128)%256

Data field format and encoding
==============================

The data fields in the payload are either strings enclosed in quotes
(ascii 34) or integers encoded as decimal strings without quotes.

If a string contains the quote character, it is escaped with a backslash (ascii 92).

Win-Test seems to accept iso8859-1 and any character code above 127 is
encoded as a backslash followed by the character code in octal.

For example, the string åäö" is encoded as:

================== ================== ==========
original character encoded characters ascii code
================== ================== ==========
å                  backslash,3,4,5    92,51,52,53
ä                  backslash,3,4,4    92,51,52,52
ö                  backslash,3,6,6    92,51,54,54
"                  backslash,"        92,34
================== ================== ==========

Frame types
===========

The frame_type field in the packets specifies what kind of information
the packet contains. I have not found a list of *all* the frame types so this
document contains what can be found in the official docs, as well as the packets
I've encountered while reverse engineering the protocol.

Frame Type GAB
--------------

Gab messages are the chat messages that can be sent between stations.
Apart from the from_station and to_station, it only contains one data field,
which contains the actual text of the gab message.

The to_station is a zero length string in the case of a gab message that
is sent to all stations.

Frame Type SUMMARY
------------------

This packet contains information about the score status of the contest.
It is described in detail in the official document linked to above.

Frame Type RCVDPKT
------------------

RCVDPKT is used to broadcast DX cluster spots coming from the telnet
connection. The from_station is 'TELNET' and the to_station is an zero length
string. There is one data field which is formatted as it arrives over telnet
from the DX cluster.

Frame Type STATUS
-----------------

Sent regularly, and contains the following data fields:

====== ===========
type   information
====== ===========
int    unknown
int    unknown
int    unknown
int    unknown
int    VFO A frequency in 100s of Hertz
string unknown
int    unknown
string unknown
int    VFO B frequency in 100s of Hertz
string operator callsign
====== ===========

Frame Type TIME
---------------

Used for time syncronization. The to_station field is empty, and the only data
field is a number representing seconds since the `Unix Epoch`_.

Frame Type IHAVE
----------------

The purpose of this message, which is sent quite frequently, is unknown.

It seems to contain some numbers that could possibly be used to synchronize
Win-Test instances in the case where UDP packets are lost, but this is just
a guess. More investigation is needed.

Frame Type ADDQSO
-----------------

This message is sent when a QSO is entered by the operator.

The data fields are as follows:

====== ===========
type   information
====== ===========
int    timestamp in unix time
int    frequency in 100s of Hertz
int    unknown
int    unknown
int    unknown
int    unknown
int    unknown
int    unknown
int    unknown
string callsign of worked station
string sent report (e.g. "59")
string received contest exchange (e.g. "5904")
string unknown
string unknown
string unknown
int    unknown
string unknown
string unknown
string operator callsign
int    unknown
====== ===========

.. _Unix Epoch: https://en.wikipedia.org/wiki/Unix_time


.. toctree::
   :name: protocol
