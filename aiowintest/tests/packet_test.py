import unittest

import wtmsg
from wtmsg import WintestPacket

# Some packegs as captured on the network, each string is the payload
# of one UDP packet.
summary = [
    b'SUMMARY: "MULT" "" 8220 "ID" "4.23.0" 129 "SJ0X" "JO99BM" "14" 200 1 3 1 0 7 7\x89\x00',
    b'SUMMARY: "MULT" "" 8220 "HEADERS" 1 5 8 10 6 14 15\x9e\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 1 "160" 28 4 25 1 28 1.00\xa5\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 2 "80" 75 12 59 0 110 1.47\xe1\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 3 "40" 533 27 93 20 702 1.32\xc4\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 4 "20" 629 19 68 9 1021 1.62\xd1\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 5 "15" 89 28 84 0 206 2.31\xec\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 6 "10" 1 1 1 0 3 3.00\xcc\x00',
    b'SUMMARY: "MULT" "" 8220 "ROW" 0 "TOTAL" 1355 91 330 30 2070 1.53\xf3\x00',
    b'SUMMARY: "MULT" "" 8220 "SCORE" 1540654636 930 871470\xfd\x00',
]

gab = [
    b'GAB: "RUN" "" "Seeeeeeegt"\x96\x00',
    b'GAB: "MULT" "" "\\345\\344\\366 \\"test\\""\xb8\x00',
]

gab_parsed = [
    WintestPacket('GAB', 'RUN', '', 'Seeeeeeegt'),
    WintestPacket('GAB', 'MULT', '', 'åäö "test"'),
]

spot = [
    b'RCVDPKT: "TELNET" "" "DX de 9A1CIG-#: 10122.80  EA1FL/P        CW    15 dB  21 WPM  CQ      1724Z\n"\xf4',
]

class TestWintestPacket(unittest.TestCase):
    def test_checksum(self):
        for msg in summary:
            data = msg[:-2]
            ch = WintestPacket.checksum(data)
            self.assertEqual(ch, msg[-2])

    def test_encode_gab(self):
        for i, msg in enumerate(gab_parsed):
            data = msg.encode()
            self.assertEqual(data, gab[i])

    def test_decode_gab(self):
        for i, packet in enumerate(gab):
            msg = WintestPacket.decode(packet)
            self.assertEqual(msg.frame_type, 'GAB')
            self.assertSequenceEqual(msg.data, gab_parsed[i].data)

    def test_encode_string(self):
        s = 'åäö"'
        self.assertEqual(wtmsg.encode_string(s), '\\345\\344\\366\\"')

    def test_decode_spot(self):
        msg = WintestPacket.decode(spot[0])

if __name__ == '__main__':
    unittest.main()
