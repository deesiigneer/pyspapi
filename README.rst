.. image:: https://raw.githubusercontent.com/kvertisp/asyncpyspapi/main/assets/repo-banner.png
   :alt: pyspapi

.. image:: https://img.shields.io/discord/850091193190973472?color=5865F2&label=discord
   :target: https://discord.gg/VbyHaKRAaN
   :alt: Discord server invite
.. image:: https://img.shields.io/github/v/release/deesiigneer/pyspapi?include_prereleases&label=github%20release
   :target: https://github.com/kvertisp/asyncpyspapi/
   :alt: GitHub release (latest by date including pre-releases)
.. image:: https://img.shields.io/pypi/v/asyncpyspapi.svg
   :target: https://pypi.org/project/asyncpyspapi/
   :alt: PyPI downloads info
.. image:: https://img.shields.io/pypi/dm/asyncpyspapi?color=informational&label=pypi%20downloads
   :target: https://pypi.org/project/asyncpyspapi/
   :alt: PyPI version info
.. image:: https://img.shields.io/readthedocs/pyspapi
   :target: https://pyspapi.readthedocs.io/
   :alt: pyspapi documentation

asyncpyspapi
========

`API <https://github.com/sp-worlds/api-docs>`_ wrapper for SP servers written in Python.

Installation
-------------
**Requires Python 3.8 or higher**

*Windows*


.. code:: sh

    pip install asyncpyspapi

*Linux/macOS*

.. code:: sh

    pip3 install asyncpyspapi

Quick example
--------------

Checking the balance
~~~~~~~~~~~~~~~~~~~~~
.. code:: py

  import asyncpyspapi

  client = asyncpyspapi.SPAPI(card_id='card_id', token='token')
  balance = await client.get_balance()
  print("Balance:", balance)

Links
------

- `pyspapi discord server <https://discord.gg/VbyHaKRAaN>`_
- `pyspapi documentation <https://pyspapi.readthedocs.io/>`_
- `PyPi <https://pypi.org/project/asyncpyspapi/>`_
- `API documentation for SP sites <https://github.com/sp-worlds/api-docs>`_
