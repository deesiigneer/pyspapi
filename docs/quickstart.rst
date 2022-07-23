:orphan:

.. _quickstart:

.. currentmodule:: pyspapi

Quickstart
==========

This page gives a brief introduction to the library.

Checking balance
-------------

Let's output the amount of money remaining in the card account to the console.

It looks something like this:

.. code-block:: python

  import pyspapi

  print(pyspapi.SPAPI(card_id='card_id', token='token').balance)

Make sure not to name it ``pyspapi`` as that'll conflict with the library.


You can find more examples in the `examples directory <https://github.com/deesiigneer/pyspapi/tree/main/examples/>`_ on GitHub.