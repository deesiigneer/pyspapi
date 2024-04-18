.. image:: https://raw.githubusercontent.com/deesiigneer/pyspapi/main/assets/repo-banner.png
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

    pip3 install pyspapi

Quick example
--------------

Checking the balance
~~~~~~~~~~~~~~~~~~~~~
.. code:: py

    from pyspapi import SPAPI
    from asyncio import get_event_loop

    spapi = SPAPI(card_id='CARD_ID', token='TOKEN')


    async def main():
        print(await spapi.balance)

    loop = get_event_loop()
    loop.run_until_complete(main())

More examples can be found in the `examples <https://github.com/deesiigneer/pyspapi/tree/main/examples>`_

Links
------

- `Discord server <https://discord.gg/VbyHaKRAaN>`_
- `pyspapi documentation <https://pyspapi.readthedocs.io/>`_
- `PyPi <https://pypi.org/project/pyspapi/>`_
- `API documentation for SP sites <https://github.com/sp-worlds/api-docs>`_
