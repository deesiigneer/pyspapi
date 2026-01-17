:orphan:

.. _quickstart:

.. currentmodule:: pyspapi

Быстрый старт
==============

На этой странице дается краткое введение в библиотеку.

Проверка баланса
-----------------

Выведем количество денег, оставшихся на счету карты, на консоль.

Это выглядит примерно так:

.. code-block:: python

    from pyspapi import SPAPI
    from asyncio import get_event_loop

    spapi = SPAPI(card_id='CARD_ID', token='TOKEN')


    async def main():
        print(await spapi.balance)

    loop = get_event_loop()
    loop.run_until_complete(main())

Убедитесь, что вы не называете его ``pyspapi``, так как это вызовет конфликт с библиотекой.

Вы можете найти больше примеров в `папке примеров <https://github.com/deesiigneer/pyspapi/tree/main/examples/>`_ на GitHub.