.. image:: https://i.imgur.com/melhWhU.png
   :alt: pyspapi

.. image:: https://img.shields.io/discord/850091193190973472?color=5865F2&label=discord
   :target: https://discord.gg/VbyHaKRAaN
   :alt: Discord server invite
.. image:: https://img.shields.io/github/v/release/deesiigneer/pyspapi?include_prereleases&label=github%20release
   :target: https://github.com/deesiigneer/pyspapi/
   :alt: GitHub release (latest by date including pre-releases)
.. image:: https://img.shields.io/pypi/v/pyspapi.svg
   :target: https://pypi.org/project/pyspapi/
   :alt: PyPI downloads info
.. image:: https://img.shields.io/pypi/dm/pyspapi?color=informational&label=pypi%20downloads
   :target: https://pypi.org/project/pyspapi/
   :alt: PyPI version info
.. image:: https://img.shields.io/readthedocs/pyspapi
   :target: https://pyspapi.readthedocs.io/
   :alt: pyspapi documentation

pyspapi
========

`API <https://github.com/sp-worlds/api-docs>`_ wrapper for SP servers written in Python.

Installation
-------------
**Requires Python 3.8 or higher**

*Windows*


.. code:: sh

    pip install pyspapi

*Linux/macOS*

.. code:: sh

    sudo apt pip3 install pyspapi

Quick example
--------------

Checking the balance
~~~~~~~~~~~~~~~~~~~~~
.. code:: py

  import pyspapi

  print(pyspapi.SPAPI(card_id='card_id', token='token').balance)

More examples can be found in the `examples <https://github.com/deesiigneer/pyspapi/tree/main/examples>`_

Links
------

- `Discord server <https://discord.gg/VbyHaKRAaN>`_
- `pyspapi documentation <https://pyspapi.readthedocs.io/>`_
- `PyPi <https://pypi.org/project/pyspapi/>`_
- `API documentation for SP sites <https://github.com/sp-worlds/api-docs>`_
