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
=======

`API <https://github.com/sp-worlds/api-docs>`_ обертка для серверов СП, написанная на Python.



Установка
==========
**Требуется Python 3.7 или выше**

*Windows*

.. code:: sh

    pip install pyspapi
      
*Linux*

.. code:: sh

    sudo apt pip3 install pyspapi

Примеры
-----

`Оплата <https://github.com/sp-worlds/api-docs/blob/main/PAYMENTS.md>`_
~~~~

.. code:: python

  from spapi import Api

  api = Api(card_id='CARD_ID',
                  token='TOKEN')

  print(api.payment(amount=1,
                    redirecturl='https://www.google.com/',
                    webhookurl='https://www.yourwebhook.com/',
                    data='some-data'
                    )
        )

* ``amount`` - Стоимость покупки в АРах
* ``redirectUrl`` - URL страницы, на которую попадет пользователь после оплаты
* ``webhookUrl`` - URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате
* ``data`` - Строка до 100 символов, сюда можно поместить любые полезные данных.

`Получение данных об успешной оплате <https://github.com/sp-worlds/api-docs/blob/main/PAYMENTS.md#%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D0%B5-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85-%D0%BE%D0%B1-%D1%83%D1%81%D0%BF%D0%B5%D1%88%D0%BD%D0%BE%D0%B9-%D0%BE%D0%BF%D0%BB%D0%B0%D1%82%D0%B5>`_
~~~~

После успешной оплаты на URL указанный в ``webhookUrl`` придет POST запрос.

*Тело запроса будет в формате JSON:*

* ``payer`` - Ник игрока, который совершил оплату
* ``amount`` - Стоимость покупки
* ``data`` - Данные, которые вы отдали при создании запроса на оплату

**Для проверки достоверности webhook'a используйте:**

.. code:: python

  from spapi import Api

  api = Api(card_id='CARD_ID',
                  token='TOKEN')

  print(api.webhook_verify(data='webhook_data',
                           header='webhook_header'
                           )
        )

*В ответ вы получите:*

* ``True`` - webhook достоверен
* ``False`` - webhook не является достоверным

`Переводы <https://github.com/sp-worlds/api-docs/blob/main/TRANSACTIONS.md>`_
~~~~

.. code:: python

  from spapi import Api

  api = Api(card_id='CARD_ID',
                  token='TOKEN')

  print(api.transaction(receiver='12345',
                        amount=1,
                        comment="test"
                        )
        )
        
* ``receiver`` - Номер карты получателя
* ``amount`` - Количество АР для перевода
* ``comment`` - Комментарий к переводу

`Проверка наличия проходки <https://github.com/sp-worlds/api-docs/blob/main/USERS.md>`_
~~~~

.. code:: python

  from spapi import Api

  api = Api(card_id='CARD_ID',
            token='TOKEN')

  print(api.check_user(discord_user_id=123456789012345678))
  
* ``discord_user_id`` - ID пользователя в Discord

*В ответ вы получите JSON:*

* ``username`` - Ник пользователя или null, если у пользователя нет входа на сервер

Ссылки
=======
* `Discord сервер <https://discord.gg/VbyHaKRAaN>`_
* `Документация pyspapi <https://pyspapi.readthedocs.io/>`_
* `Документация API сайтов СП <https://github.com/sp-worlds/api-docs>`_
