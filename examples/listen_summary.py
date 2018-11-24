import asyncio
import aiowintest
import sys
import json
import datetime

# replace the address below with your network broadcast address
broadcast_addr = ('10.1.1.255', 9871)
local_addr = ('0.0.0.0', 9871)

def serializer(v):
    if isinstance(v, datetime.datetime):
        return v.astimezone().isoformat()

async def on_summary(message):
    print(json.dumps(message, default=serializer, indent=4, sort_keys=True))

async def main(argv):
    loop = asyncio.get_event_loop()
    wt = aiowintest.WintestProtocol(loop, local_addr, broadcast_addr)
    await wt.connect()
    wt.add_handler('summary', on_summary)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sys.argv))
    loop.run_forever()
