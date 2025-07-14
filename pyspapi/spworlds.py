from base64 import b64encode
from hashlib import sha256
from hmac import new, compare_digest
from typing import Optional

from .api import APISession
from .types import User
from .types.me import Account
from .types.payment import Item

__all__ = ['SPAPI']


class SPAPI(APISession):
    """
    pyspapi — высокоуровневый клиент для взаимодействия с SPWorldsAPI.

    Предоставляет удобные методы для работы с балансом карты, вебхуками,
    информацией о пользователе, транзакциями и платежами, а также верификацией вебхуков.
    """

    def __init__(self, card_id: str,
                 token: str,
                 timeout: int = 5,
                 sleep_time: float = 0.2,
                 retries: int = 0,
                 raise_exception: bool = False):
        """
        Инициализирует объект SPAPI.

        :param card_id: Идентификатор карты.
        :type card_id: str
        :param token: Токен API.
        :type token: str
        :param timeout: Таймаут для запросов API в секундах. По умолчанию 5.
        :type timeout: int
        :param sleep_time: Время ожидания между повторными запросами в секундах. По умолчанию 0.2.
        :type sleep_time: float
        :param retries: Количество повторных попыток для неудачных запросов. По умолчанию 0.
        :type retries: int
        :param raise_exception: Поднимать исключения при ошибке, если True.
        :type raise_exception: bool
        """
        super().__init__(card_id, token, timeout, sleep_time, retries, raise_exception)
        self.__card_id = card_id
        self.__token = token

    def __repr__(self):
        """
        Возвращает строковое представление объекта SPAPI.
        """
        return f"{self.__class__.__name__}({vars(self)})"

    @property
    async def balance(self) -> Optional[int]:
        """
        Получает текущий баланс карты.

        :return: Текущий баланс карты.
        :rtype: int
        """
        return int((await super().get('card'))['balance'])

    @property
    async def webhook(self) -> Optional[str]:
        """
        Получает URL вебхука, связанного с картой.

        :return: URL вебхука.
        :rtype: str
        """
        return str((await super().get('card'))['webhook'])

    @property
    async def me(self) -> Optional[Account]:
        """
        Получает информацию об аккаунте текущего пользователя.

        :return: Объект Account, представляющий аккаунт текущего пользователя.
        :rtype: :class:`Account`
        """
        me = await super().get('accounts/me')
        return Account(
                account_id=me['id'],
                username=me['username'],
            minecraftuuid=me['minecraftUUID'],
                status=me['status'],
                roles=me['roles'],
            cities=me['cities'],
                cards=me['cards'],
                created_at=me['createdAt'])

    async def get_user(self, discord_id: int) -> Optional[User]:
        """
        Получает информацию о пользователе по его ID в Discord.

        :param discord_id: ID пользователя в Discord.
        :type discord_id: int

        :return: Объект User, представляющий пользователя.
        :rtype: :class:`User`
        """
        user = await super().get(f'users/{discord_id}')
        cards = await super().get(f"accounts/{user['username']}/cards")
        return User(user['username'], user['uuid'], cards)

    async def create_transaction(self, receiver: str, amount: int, comment: str) -> Optional[int]:
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
        data = {
            'receiver': receiver,
            'amount': amount,
            'comment': comment
        }

        return int((await super().post('transactions', data))['balance'])

    async def create_payment(self, webhook_url: str, redirect_url: str, data: str, items: list[Item]) -> Optional[str]:
        """
        Создает платеж.

        :param webhook_url: URL вебхука для платежа.
        :type webhook_url: str
        :param redirect_url: URL для перенаправления после платежа.
        :type redirect_url: str
        :param data: Дополнительные данные для платежа.
        :type data: str
        :param items: Элементы, включаемые в платеж.

        :return: URL для платежа или None при ошибке.
        :rtype: str
        """
        data = {
            'items': items,
            'redirectUrl': redirect_url,
            'webhookUrl': webhook_url,
            'data': data
        }

        return str((await super().post('payments', data))['url'])

    async def update_webhook(self, url: str) -> Optional[dict]:
        """
        Обновляет URL вебхука, связанного с картой.

        :param url: Новый URL вебхука.
        :return: Ответ API в виде словаря или None при ошибке.
        """
        data = {'url': url}

        return await super().put('card/webhook', data)

    def webhook_verify(self, data: str, header: str) -> bool:
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
