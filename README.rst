==================================================
Python implementation of the Win-Test UDP protocol
==================================================

Win-Test (http://win-test.com) is a tool used for Ham Radio Contesting.

This is currently a partial implementation of the protocol, mainly
by reverse engineering the protocol by sniffing the UDP traffic.

The author of this package is not affiliated in any way with the Win-Test
developers.

Installation
============

Install using pip:

.. code-block:: bash

    pip install aiowintest

Win-Test Protocol documentation
===============================

There is some partial protocol documentation from the Win-Test developers
here: http://download.win-test.com/utils/SummaryBroadcastingSpecs.txt

Development
===========

To build documentation:

.. code-block:: bash

    pip install sphinx
    sphinx-build docs docs/_build
