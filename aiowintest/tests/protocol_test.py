import unittest
from unittest.mock import Mock

from ..protocol import *



class TestWintestProtocol(unittest.TestCase):
    def make_wintest(self):
        loop = asyncio.get_event_loop()
        wt = WintestProtocol(loop, ('0.0.0.0', 9871), ('192.168.1.255', 9871))
        wt._transport = Mock()
        return wt

    def test_gab(self):
        wt = self.make_wintest()
        wt.send_gab('test', 'CQ')
        wt._transport.sendto.assert_called_with(b'GAB: "test" "" "CQ"\x84\x00', ('192.168.1.255', 9871))
