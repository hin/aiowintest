import asyncio
import aiowintest
import sys

# replace the address below with your network broadcast address
broadcast_addr = ('10.1.1.255', 9871)
local_addr = ('0.0.0.0', 9871)

async def on_gab(message):
    print(message)

async def main(argv):
    loop = asyncio.get_event_loop()
    wt = aiowintest.WintestProtocol(loop, local_addr, broadcast_addr)
    await wt.connect()
    #wt.add_handler('gab', on_gab)
    wt.send_gab('TEST', 'Testing gab message')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    #loop.run_forever()
