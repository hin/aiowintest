===========
Development
===========

Building the documentation
==========================

The documentation is written using Sphinx which is installed by:

.. code-block:: bash

    $ pip install sphinx

To build the documentation:

.. code-block:: bash

    $ make docs

Open the file "``docs/_build/index.html``" in your web browser.

Running unit tests
==================

Run the unit test by:

.. code-block:: bash

    $ python setup.py test

Uploading a new release
=======================

Prerequisites:

.. code-block:: bash

    pip install twine
    pip install setuptools
    pip install wheel

Update the version in aiowintest/__init__.py

Set a git tag to the version number, e.g.

.. code-block:: bash

    $ git tag $(python3 setup.py --version)
    $ git push --tags

Next, build the distribution files:

.. code-block:: bash

    $ make dist

Upload distribution files to pypi.org:

.. code-block:: bash

    $ make upload

The documentation at https://aiowintest.readthedocs.io/ is updated
automatically by Read the Docs when the tag is pushed, but check that it
worked and take necessary actions to correct any issue.
