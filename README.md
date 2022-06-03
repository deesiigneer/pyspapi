# pyspapi 
Фреймворк [API](https://github.com/sp-worlds/api-docs) для серверов СП

## Установка
**Требуется *Python 3.7* или выше**

*Windows*
```commandline
pip install pyspapi
```
*Linux*
```commandline
sudo apt pip3 install pyspapi
```

## Примеры
### [Оплата](https://github.com/sp-worlds/api-docs/blob/main/PAYMENTS.md)

```Python
import spapi

api = spapi.Api(card_id='CARD_ID',
                token='TOKEN')

print(api.payment(amount=1,
                  redirecturl='https://www.google.com/',
                  webhookurl='https://www.yourwebhook.com/',
                  data='Какие-то данные'
                  )
      )

```
- `amount` - Стоимость покупки в АРах
- `redirectUrl` - URL страницы, на которую попадет пользователь после оплаты
- `webhookUrl` - URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате
- `data` - Строка до 100 символов, сюда можно пометить любые полезные данных.
#### Получение данных об успешной оплате
После успешной оплаты на URL указанный в `webhookUrl` придет POST запрос.

*Тело запроса будет в формате JSON:*

- `payer` - Ник игрока, который совершил оплату
- `amount` - Стоимость покупки
- `data` - Данные, которые вы отдали при создании запроса на оплату

### [Переводы](https://github.com/sp-worlds/api-docs/blob/main/TRANSACTIONS.md)

```Python
import spapi

api = spapi.Api(card_id='CARD_ID',
                token='TOKEN')

print(api.transaction(receiver='12345',
                      amount=1,
                      comment="test"
                      )
      )

```
- `receiver` - Номер карты получателя
- `amount` - Количество АР для перевода
- `comment` - Комментарий к переводу
- 
### [Проверка наличия проходки](https://github.com/sp-worlds/api-docs/blob/main/USERS.md)

```Python
import spapi

api = spapi.Api(card_id='CARD_ID',
                token='TOKEN')

print(api.check_user(discord_user_id=123456789012345678)
      )

```
- `discord_user_id` - ID пользователя в Discord.

*В ответ вы получите JSON:*

- `username` - Ник пользователя или null, если у пользователя нет входа на сервер.


## Ссылки

- [Discord сервер разработчика](https://discord.gg/sJYtYnhN)
- [Документация API сайтов СП](https://github.com/sp-worlds/api-docs)
