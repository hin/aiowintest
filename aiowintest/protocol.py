import asyncio
import socket
from .packet import WintestPacket
from .wintest_data import *
import sys
import datetime

_packet_parsers = {}

def _on(frame_type):
    def wrap(func):
        _packet_parsers[frame_type] = func
        return func
    return wrap

class WintestProtocol:
    def __init__(self, loop, local_addr, broadcast_addr):
        self._loop = loop
        self._local_addr = local_addr
        self._broadcast_addr = broadcast_addr
        asyncio.ensure_future(self._connect())
        self._summary = {}
        self._handlers = {}

    async def _connect(self):
        await self._loop.create_datagram_endpoint(
            lambda: self, local_addr=self._local_addr
        )

    def add_handler(self, event, handler):
        self._handlers[event] = handler

    def connection_made(self, transport):
        self._transport = transport
        sock = transport.get_extra_info('socket')
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def send_gab(self, text):
        self.send_packet(WintestPacket('GAB', ['', text]))

    def send_packet(self, pkt):
        print('sending:', pkg)
        self.transport.sendto(pkt.encode(), self._broadcast_addr)

    @_on('SUMMARY')
    def _on_summary_packet(self, packet):
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
        print('Unknown:', packet)

    @_on('GAB')
    def _on_gab_packet(self, packet):
        print('GAB:', packet)
        # TODO I believe that the packet.data[1] contains
        # the recipient of the gab in the case of a personal
        # message, but this needs to be confirmed.
        return 'gab', {
            'from': packet.data[0],
            'message': packet.data[2],
        }

    @_on('TIME')
    def _on_time_packet(self, packet):
        # TODO I don't know what packet.data[1] is
        return 'time', {
            'from': packet.data[0],
            'timestamp': datetime.datetime.utcfromtimestamp(int(packet.data[2]))
        }

    @_on('STATUS')
    def _on_status(self, packet):
        return 'status', {
            'station': packet.data[0],
            'operator': packet.data[11],
            'vfo_a': packet.data[6],
            'vfo_b': packet.data[10],
            }

    def _on_packet(self, packet):
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
        pkt = WintestPacket.decode(payload, addr)
        self._on_packet(pkt)
