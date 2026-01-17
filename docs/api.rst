.. currentmodule:: pyspapi

Справочник API
===============

В следующем разделе описывается API pyspapi.

Информация о версии
---------------------

Существует два основных способа запроса информации о версии.

.. data:: version_info

    Именованный кортеж, аналогичный :obj:`py:sys.version_info`.

    Как и в :obj:`py:sys.version_info`, допустимые значения для ``releaselevel`` это
    'alpha', 'beta', 'candidate' и 'final'.

.. data:: __version__

    Строковое представление версии.

``pyspapi``
-----------

``SPAPI``
~~~~~~~~~
.. autoclass:: SPAPI
    :members:
