import asyncio
import socket
from .packet import WintestPacket
from .wintest_data import *
import sys
import datetime

_packet_parsers = {}

def _on(frame_type):
    """Decorator function that makes the mapping from UDP frame_types to
    parser function a little smoother.
    """
    def wrap(func):
        _packet_parsers[frame_type] = func
        return func
    return wrap

class WintestProtocol:
    """Implements the Win-Test UDP protocol.
    """
    def __init__(self, loop, local_addr, broadcast_addr):
        """Create a listener for the Win-Test protocol.

        Args:
           loop (asyncio event loop): asyncio event loop to use. Typically
                `asyncio.get_event_loop()` will be the correct loop to pass,
                but in the case of a threaded application there might be reason
                to pass some other loop.
           local_addr (ip, port): Local address and port to listen to. Usually
                ('0.0.0.0', 9871) will be sufficient, but if the network setup
                is non-typical a particular address to listen to can be specified.
            broadcast_addr (ip, port): Broadcast address and port to send packets to.
                This will typically match the address/port specified in Win-Test itself.
                E.g. for a host with the address 192.168.1.25 with netmask 255.255.255.255
                the broadcast address will typically be 192.168.1.255.
                The port will typically be 9871.
        """
        self._loop = loop
        self._local_addr = local_addr
        self._broadcast_addr = broadcast_addr
        asyncio.ensure_future(self._connect())
        self._summary = {}
        self._handlers = {}

    async def _connect(self):
        """Connect the UDP socket"""
        await self._loop.create_datagram_endpoint(
            lambda: self, local_addr=self._local_addr
        )

    def add_handler(self, message_type, handler):
        """Add a message handler function, which is called when a Win-Test message
        is received.

        The handler must have the following signature:
            async def my_message_handler(message)

        The message argument passed to the handler function depends on
        the message_type as described below.

        The message_type is on of the following strings:
            'summary', 'gab', 'time', 'status'
        """
        self._handlers[message_type] = handler

    def connection_made(self, transport):
        """Called by asyncio when the socket is created."""
        self._transport = transport
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_gab(self, from_station, text):
        """Send a gab message to Win-Test.

            Args:
                from_station (str)- name of the station the message was sent from.
                text (str) - the actual text of the message.
        """
        self.send_packet(WintestPacket('GAB', [from_station, '', text]))

    def send_packet(self, pkt):
        """Send a raw WintestPacket to the network.

        Args:
            pkt (WintestPacket): the packet to send
        """
        self.transport.sendto(pkt.encode(), self._broadcast_addr)

    @_on('SUMMARY')
    def _on_summary_packet(self, packet):
        """Handle summary packets.

        Summary information is split into several UDP packets, so in order
        to retrieve all information all the packets need to be gathered before
        a message can be passed to the user of the WintestProtocol class.
        """
        retval = None, None
        if packet.data[3] == 'ID':
            self._summary['id'] = {}
            self._summary['transaction_id'] = packet.data[2]
            self._summary['id']['wintest_version'] = packet.data[4]
            self._summary['id']['wintest_protocol_version'] = packet.data[5]
            self._summary['id']['station_callsign'] = packet.data[6]
            self._summary['id']['gridsquare'] = packet.data[7]
            self._summary['id']['zone'] = packet.data[8]
            self._summary['id']['contest'] = CONTEST_ID[packet.data[9]]
            self._summary['id']['modecategory'] = MODECATEGORY_ID[packet.data[10]]
            self._summary['id']['category'] = CATEGORY_ID[packet.data[11]]
            self._summary['id']['overlay'] = OVERLAY_ID[packet.data[12]]
            self._summary['id']['powerclass'] = POWERCLASS_ID[packet.data[13]]
            self._summary['id']['columns_count'] = int(packet.data[14])
            self._summary['id']['rows_count'] = int(packet.data[15])
            self._summary['rows'] = [None] * self._summary['id']['rows_count']
        elif packet.data[3] == 'HEADERS':
            self._summary['headers'] = []
            for hdr in  packet.data[4:]:
                self._summary['headers'].append(HEADER_ID[hdr])
        elif packet.data[3] == 'ROW':
            row_num = int(packet.data[4])
            self._summary['rows'][row_num] = packet.data[5:]
        elif packet.data[3] == 'SCORE':
            self._summary['score'] = {}
            self._summary['score']['frametime'] = datetime.datetime.utcfromtimestamp(int(packet.data[4]))
            self._summary['score']['operating_time'] = packet.data[5]
            self._summary['score']['final_score'] = packet.data[6]
            retval = 'summary', self._summary
            self._summary = {}
        else:
            print('Unknown or invalid summary packet:', packet)
        return retval

    def _on_unknown_frame_type(self, packet):
        """Deals with any unknown messages encountered from Win-Test.

        TODO: Use logging to log the packet better, or make it a callback
        to the user of the WintestProtocol class.
        """
        print('Unknown:', packet)

    @_on('GAB')
    def _on_gab_packet(self, packet):
        """Parse a gab packet"""
        # TODO I believe that the packet.data[1] contains
        # the recipient of the gab in the case of a personal
        # message, but this needs to be confirmed.
        return 'gab', {
            'from': packet.data[0],
            'message': packet.data[2],
        }

    @_on('TIME')
    def _on_time_packet(self, packet):
        """Parse time packet"""
        # TODO I don't know what packet.data[1] is
        return 'time', {
            'from': packet.data[0],
            'timestamp': datetime.datetime.utcfromtimestamp(int(packet.data[2]))
        }

    @_on('STATUS')
    def _on_status(self, packet):
        """Parse status packet"""
        return 'status', {
            'station': packet.data[0],
            'operator': packet.data[11],
            'vfo_a': packet.data[6],
            'vfo_b': packet.data[10],
            }

    def _on_packet(self, packet):
        """Parse a packet and call the appropriate parser for the packet"""
        packet_parser = _packet_parsers.get(packet.frame_type)
        if packet_parser:
            ret = packet_parser(self, packet)
            if ret:
                event, message = ret
                if self._handlers.get(event):
                    asyncio.ensure_future(self._handlers[event](message))
        else:
            self._on_unknown_frame_type(packet)

    def datagram_received(self, payload, addr):
        """Called by asyncio when a UDP packet is received"""
        pkt = WintestPacket.decode(payload, addr)
        self._on_packet(pkt)
