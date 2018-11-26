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

def split_data(input):
    def get_token(input):
        result = None
        divisor = 10.0
        i = 0
        while i < len(input):
            if type(result) == type(None):
                if input[i] == '"':
                    result = ''
                elif input[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    result = int(input[i])
                elif input[i] == ' ':
                    pass
                else:
                    raise ValueError('Cannot parse char %c', input[i])
            elif type(result) == str:
                if input[i] == '"':
                    break
                else:
                    if input[i] == '\\':
                        num = ''
                        while input[i+1] in ['0', '1', '2', '3', '4', '5', '6', '7']:
                            i += 1
                            num += input[i]
                        if len(num) > 0:
                            result += chr(int(num, 8))
                        else:
                            i += 1
                            result += input[i]
                    else:
                        result += input[i]
            elif type(result) == int:
                if input[i] == ' ':
                    break
                elif input[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    result = 10*result + int(input[i])
                elif input[i] == '.':
                    result = float(result)
                else:
                    raise ValueError('Parsing %s failed: illegal character %c'%(type(result).__name__, input[i]))
            elif type(result) == float:
                if input[i] == ' ':
                    break
                elif input[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    result += int(input[i])/divisor
                    divisor *= 10.0
                else:
                    raise ValueError('Parsing %s failed: illegal character %c'%(type(result).__name__, input[i]))
            else:
                raise ValueError('Parsing %s failed'%(type(result).__name__))
            i += 1
        return result, input[i+1:]
    result = []
    while len(input) > 0:
        token, input = get_token(input)
        result.append(token)
    return result

class WintestPacket:
    def __init__(self, frame_type, data):
        self.frame_type = frame_type
        self.data = data

    def decode(packet):
        # Win-test adds a null character at the end of all packets except
        # for the RCVDPKT (DX cluster spots). I don't know why - it shouldn't
        # according their documentation. This may a simple bug in their implementation
        # or it could be some feature I haven't figured out.
        # For now, we simple check if the last byte is zero, and discard it
        # if it is. This works since the 7th bit is always set in the checksum.
        if packet[-1] == 0:
            packet = packet[:-1]
        ch = packet[-1]
        if ch != WintestPacket.checksum(packet[:-1]):
            raise ValueError('Incorrect checksum (%x)'%(ch))
        i = packet.find(b':')
        frame_type = packet[:i].decode('ascii')
        raw_data = packet[i+1:-1].decode('ascii')
        msg_data = split_data(raw_data)
        #msg_data = [unescape(a) for a in shlex.split(packet[i+1:-1].decode('ascii'))]
        return WintestPacket(frame_type, msg_data)

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
        # Add the strange extra null character at the end to (hopefully) mimic
        # the actual observed behaviour of Win-Test.
        # To mimic Win-Test more closely, we should not add this for for at
        # least the RCVDPKT packets, but there is currently no support for
        # sending such packets so we skip this for now.
        data += bytes([0])
        return data

    # Calculate checksum according to the Wintest protocol
    def checksum(data):
        return (sum(data)|128)%256
