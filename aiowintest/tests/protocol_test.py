import asynctest
from asynctest.mock import Mock
import pytest

from ..protocol import *

# Reuse test data from packet_test.py
from aiowintest.tests.packet_test import summary

class TestWintestProtocol(asynctest.TestCase):
    def make_wintest(self):
        loop = asyncio.get_event_loop()
        wt = WintestProtocol(loop, ('0.0.0.0', 9871), ('192.168.1.255', 9871))
        wt._transport = Mock()
        return wt

    def test_gab(self):
        wt = self.make_wintest()
        wt.send_gab('test', 'CQ')
        wt._transport.sendto.assert_called_with(b'GAB: "test" "" "CQ"\x84\x00', ('192.168.1.255', 9871))

    def test_summary(self):
        wt = self.make_wintest()
        on_summary = asynctest.CoroutineMock()
        wt.add_handler('summary', on_summary)
        for p in summary:
            wt.datagram_received(p, ('192.168.1.100', 9871))
        on_summary.assert_called_with({
            'id': {
                'wintest_version': '4.23.0',
                'wintest_protocol_version': 129,
                'station_callsign': 'SJ0X',
                'gridsquare': 'JO99BM',
                'zone': '14',
                'contest': 'CQWW_DX',
                'modecategory': 'PHONE',
                'category': 'MULTI_SINGLE',
                'overlay': 'NONE',
                'powerclass': 'HIGH',
                'columns_count': 7,
                'rows_count': 7
                },
            'transaction_id': 8220,
            'rows': [
                ['TOTAL', 1355, 91, 330, 30, 2070, 1.53],
                ['160', 28,  4, 25,  1,   28, pytest.approx(1.00, 0.001)],
                ['80',  75, 12, 59,  0,  110, pytest.approx(1.47, 0.001)],
                ['40', 533, 27, 93, 20,  702, pytest.approx(1.32, 0.001)],
                ['20', 629, 19, 68,  9, 1021, pytest.approx(1.62, 0.001)],
                ['15',  89, 28, 84,  0,  206, pytest.approx(2.31, 0.001)],
                ['10',   1,  1,  1,  0,    3, pytest.approx(3.00, 0.001)]],
            'headers': ['BAND', 'QSO', 'CQ', 'DXCC', 'DUPE', 'POINTS', 'AVG'],
            'score': {
                'frametime': datetime.datetime(2018, 10, 27, 15, 37, 16),
                'operating_time': 930,
                'final_score': 871470
                }
            })
