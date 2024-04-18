:orphan:

.. _quickstart:

.. currentmodule:: pyspapi

Quickstart
==========

This page gives a brief introduction to the library.

Checking balance
----------------

Let's output the amount of money remaining in the card account to the console.

It looks something like this:

.. code-block:: python

    from pyspapi import SPAPI
    from asyncio import get_event_loop

    spapi = SPAPI(card_id='CARD_ID', token='TOKEN')


    async def main():
        print(await spapi.balance)

    loop = get_event_loop()
    loop.run_until_complete(main())

Make sure not to name it ``pyspapi`` as that'll conflict with the library.


You can find more examples in the `examples directory <https://github.com/deesiigneer/pyspapi/tree/main/examples/>`_ on GitHub.