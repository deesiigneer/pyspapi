.. currentmodule:: pyspapi

API Reference
===============

The following section outlines the API of pyspapi.

Version  Info
---------------------

There are two main ways to query version information.

.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'alpha', 'beta', 'candidate' and 'final'.

.. data:: __version__

    A string representation of the version.

``pyspapi``
-----------

``SPAPI``
~~~~~~~~~
.. autoclass:: SPAPI
    :members:
