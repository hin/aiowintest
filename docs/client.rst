.. aiowintest-client:

==========
Client API
==========

The client API uses asyncio and is designed to be easy to use. The API is
far from finished and expect it to be changed without notice!
You have been warned!

Typical use cases are mainly bridging information from and to Win-Test. At
http://sk0ux.se/ we intend to use it to display current scores on a monitor
in the club house, and also bridging gab messages to/from our instant messaging
system.

Currently the functionality is limited to sending/receiving gab messages and
score board summary.

Installation
============

As aiowintest uses asyncio, it requres python 3. Python 3.6 and 3.7 have been
tested but older versions should work, or be easy to get to work.
Pull requests are appreciated!

Install aiowintest using pip:

.. code-block:: bash

    $ pip install aiowintest

Quickstart
==========

A quick example of how to receive gab-messages from Win-Test:

.. code-block:: python3

    import asyncio
    import aiowintest

    # replace the address below with your network broadcast address
    broadcast_addr = ('192.168.11.255', 9000)
    local_addr = ('0.0.0.0', 9871)

    async def on_gab(message):
        print(message)

    async def main(argv):
        loop = asyncio.get_event_loop()
        wt = WintestProtocol(loop, local_addr, broadcast_addr)
        wt.add_handler('gab', on_gab)

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(sys.argv))
        loop.run_forever()

Please note that the machine running the code above *must* be on the
same network as the Win-Test machine(s).


.. toctree::
   :caption: Contents:
   :name: client
