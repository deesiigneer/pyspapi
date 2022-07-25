.. py:currentmodule:: pyspapi

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
~~~~~
.. autoclass:: SPAPI
    :members:

    .. automethod:: SPAPI.event()
        :decorator:

    .. automethod:: SPAPI.check_user_access
        :decorator:

    .. automethod:: SPAPI.get_user
        :decorator:

    .. automethod:: SPAPI.get_users
        :decorator:

    .. automethod:: SPAPI.payment
        :decorator:

    .. automethod:: SPAPI.transaction
        :decorator:

    .. automethod:: SPAPI.webhook_verify
        :decorator:

MojangAPI
~~~~~
.. autoclass:: MojangAPI
    :members:

    .. automethod:: SPAPI.event()
        :decorator:

    .. automethod:: SPAPI.get_name_history
        :decorator:

    .. automethod:: SPAPI.get_profile
        :decorator:

    .. automethod:: SPAPI.get_username
        :decorator:

    .. automethod:: SPAPI.get_uuid
        :decorator:

    .. automethod:: SPAPI.get_uuids
        :decorator:
