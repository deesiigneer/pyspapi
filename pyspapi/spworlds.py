from .api import APISession
from .types import User
from .types.me import Account
from .types.payment import Item
from hmac import new, compare_digest
from hashlib import sha256
from base64 import b64encode
import aiohttp

__all__ = ['SPAPI']


class SPAPI(APISession):
    """
    Представляет собой клиент API для взаимодействия с конкретным сервисом.
    """

    def __init__(self, card_id=None, token=None, timeout=5, sleep_time=0.2, retries=0):
        """
        Инициализирует объект SPAPI.

        :param card_id: Идентификатор карты.
        :type card_id: str
        :param token: Токен API.
        :type token: str
        :param timeout: Таймаут для запросов API в секундах. По умолчанию 5.
        :type timeout: int, optional
        :param sleep_time: Время ожидания между повторными запросами в секундах. По умолчанию 0.2.
        :type sleep_time: float, optional
        :param retries: Количество повторных попыток для неудачных запросов. По умолчанию 0.
        :type retries: int, optional
        """
        super().__init__(card_id, token, timeout, sleep_time, retries)
        self.__card_id = card_id
        self.__token = token

    def __repr__(self):
        """
        Возвращает строковое представление объекта SPAPI.
        """
        return "%s(%s)" % (
            self.__class__.__name__,
            self.__dict__
        )

    async def __get(self, method):
        """
        Выполняет GET-запрос к API.

        :param method: Метод API для вызова.
        :type method: str

        :return: JSON-ответ от API.
        :rtype: dict
        """
        async with APISession(self.__card_id, self.__token) as session:
            response = await session.get(method)
            response = await response.json()
            return response

    @property
    async def balance(self):
        """
        Получает текущий баланс карты.

        :return: Текущий баланс карты.
        :rtype: int
        """
        card = await self.__get('card')
        return card['balance']

    @property
    async def webhook(self) -> str:
        """
        Получает URL вебхука, связанного с картой.

        :return: URL вебхука.
        :rtype: str
        """
        card = await self.__get('card')
        return card['webhook']

    @property
    async def me(self):
        """
        Получает информацию об аккаунте текущего пользователя.

        :return: Объект Account, представляющий аккаунт текущего пользователя.
        :rtype: Account
        """
        me = await self.__get('account/me')
        return Account(
                account_id=me['id'],
                username=me['username'],
                status=me['status'],
                roles=me['roles'],
                city=me['city'],
                cards=me['cards'],
                created_at=me['createdAt'])

    async def get_user(self, discord_id: int) -> User:
        """
        Получает информацию о пользователе по его ID в Discord.

        :param discord_id: ID пользователя в Discord.
        :type discord_id: int

        :return: Объект User, представляющий пользователя.
        :rtype: User
        """
        user = await self.__get(f'users/{discord_id}')
        cards = await self.__get(f"accounts/{user['username']}/cards")
        return User(user['username'], user['uuid'], cards)

    async def create_transaction(self, receiver: str, amount: int, comment: str):
        """
        Создает транзакцию.

        :param receiver: Получатель транзакции.
        :type receiver: str
        :param amount: Сумма транзакции.
        :type amount: int
        :param comment: Комментарий к транзакции.
        :type comment: str

        :return: Баланс после транзакции.
        :rtype: int
        """
        async with APISession(self.__card_id, self.__token) as session:
            data = {
                'receiver': receiver,
                'amount': amount,
                'comment': comment
            }
            res = await session.post('transactions', data)
            res = await res.json()
        return res['balance']

    async def create_payment(self, webhook_url: str, redirect_url: str, data: str, items) -> str:
        """
        Создает платеж.

        :param webhook_url: URL вебхука для платежа.
        :type webhook_url: str
        :param redirect_url: URL для перенаправления после платежа.
        :type redirect_url: str
        :param data: Дополнительные данные для платежа.
        :type data: str
        :param items: Элементы, включаемые в платеж.

        :return: URL для платежа.
        :rtype: str
        """
        async with APISession(self.__card_id, self.__token) as session:
            data = {
                'items': items,
                'redirectUrl': redirect_url,
                'webhookUrl': webhook_url,
                'data': data
            }
            res = await session.post('payments',data)
            res = await res.json()
        return res['url']

    async def update_webhook(self, url: str):
        """
        Обновляет URL вебхука, связанного с картой.

        :param url: Новый URL вебхука.
        :type url: str

        :return: JSON-ответ от API.
        :rtype: dict
        """
        async with APISession(self.__card_id, self.__token) as session:
            data = {
                'url': url
            }
            res = await session.put(endpoint='card/webhook', data=data)
            if res:
                res = await res.json()
        return res

    def webhook_verify(self, data: str, header) -> bool:
        """
        Проверяет достоверность вебхука.

        :param data: Данные из вебхука.
        :type data: str
        :param header: Заголовок X-Body-Hash из вебхука.

        :return: True, если заголовок из вебхука достоверен, иначе False.
        :rtype: bool
        """
        hmac_data = b64encode(new(self.__token.encode('utf-8'), data, sha256).digest())
        return compare_digest(hmac_data, header.encode('utf-8'))

    def to_dict(self) -> dict:
        """
        Преобразует объект SPAPI в словарь.

        :return: Словарное представление объекта SPAPI.
        :rtype: dict
        """
        return self.__dict__.copy()
