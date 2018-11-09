from dataclasses import dataclass, field
import shlex

# Some documentation here:
# http://download.win-test.com/utils/SummaryBroadcastingSpecs.txt

def encode_string(s):
    result = ''
    for c in s:
        if c == '"':
            result += '\\"'
        elif ord(c) in range(32, 127):
            result += c
        else:
            result += '\\%03o'%(ord(c))
    return result

@dataclass
class WintestPacket:
    frame_type: str
    data: list

    def __init__(self, frame_type, data, sender):
        self.frame_type = frame_type
        self.sender = sender
        self.data = data

    def decode(packet, sender):
        def unescape(s):
            i = 0
            result = ''
            while i < len(s):
                if s[i] == '\\':
                    ns = ''
                    while s[i+1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        ns += s[i+1]
                        i += 1
                    result += chr(int(ns, 8))
                else:
                    result += s[i]
                i += 1
            return result
        # Win-test adds a null character at the end of all packets except
        # for the RCVDPKT (DX cluster spots). I don't know why - it shouldn't
        # according the summary docs. This may a simple bug in their implementation
        # or it could be some feature I haven't figured out.
        # For now, we simple check if the last byte is zero, and discard it
        # if it is. Ugly but works...
        if packet[-1] == 0:
            packet = packet[:-1]
        ch = packet[-1]
        if ch != WintestPacket.checksum(packet[:-1]):
            raise ValueError('Incorrect checksum (%x)'%(ch))
        i = packet.find(b':')
        frame_type = packet[:i].decode('ascii')
        msg_data = [unescape(a) for a in shlex.split(packet[i+1:-1].decode('ascii'))]
        return WintestPacket(frame_type, msg_data, sender)

    def encode(self):
        def encode_arg(arg):
            if type(arg) == int:
                return '%d'%arg
            elif type(arg) == str:
                return '"%s"'%encode_string(arg)
            raise ValueError('Cannot encode %s'%type(arg))
        msg = self.frame_type + ': ' + ' '.join([encode_arg(arg) for arg in self.data])
        data = msg.encode('ascii')
        ch = WintestPacket.checksum(data)
        data += bytes([ch])
        # Add the strange extra null character at the end to (mosty) mimic Win-tests
        # actual behaviour. To mimic Win-test fully, we should not add this for
        # for at least the RCVDPKT packets, but I do not currently have a need
        # for sending such packets so we skip this for now. Ugly but good enough...
        data += bytes([0])
        return data

    # Calculate checksum according to the Wintest protocol
    def checksum(data):
        return (sum(data)|128)%256
