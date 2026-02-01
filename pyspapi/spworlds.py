from base64 import b64encode
from hashlib import sha256
from hmac import compare_digest, new
from typing import Optional

from pyspapi.api import APISession
from pyspapi.exceptions import InsufficientBalanceError
from pyspapi.types import User
from pyspapi.types.me import Account
from pyspapi.types.payment import Item

__all__ = ["SPAPI"]


class SPAPI(APISession):
    """
    pyspapi — высокоуровневый клиент для взаимодействия с SPWorlds API.

    Предоставляет удобные методы для работы с балансом карты, вебхуками,
    информацией о пользователе, транзакциями и платежами, а также верификацией вебхуков.
    """

    def __init__(
        self,
        card_id: str,
        token: str,
        timeout: int = 5,
        sleep_time: float = 0.2,
        retries: int = 0,
        raise_exception: bool = False,
        proxy: str = None,
    ):
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
        :param proxy: Прокси для подключения к API. По умолчанию None.
        :type proxy: str
        """
        super().__init__(
            card_id, token, timeout, sleep_time, retries, raise_exception, proxy
        )
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
        try:
            response = await super().get("card")
            if response is None:
                return None
            return int(response.get("balance", 0))
        except (KeyError, ValueError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to parse balance response: {e}")
            return None

    @property
    async def webhook(self) -> Optional[str]:
        """
        Получает URL вебхука, связанного с картой.

        :return: URL вебхука.
        :rtype: str
        """
        try:
            response = await super().get("card")
            if response is None:
                return None
            return str(response.get("webhook", ""))
        except (KeyError, ValueError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to parse webhook response: {e}")
            return None

    @property
    async def me(self) -> Optional[Account]:
        """
        Получает информацию об аккаунте текущего пользователя.

        :return: Объект Account, представляющий аккаунт текущего пользователя.
        :rtype: :class:`Account`
        """
        try:
            me = await super().get("accounts/me")
            if me is None:
                return None

            return Account(
                account_id=me.get("id"),
                username=me.get("username"),
                minecraftuuid=me.get("minecraftUUID"),
                status=me.get("status"),
                roles=me.get("roles", []),
                cities=me.get("cities", []),
                cards=me.get("cards", []),
                created_at=me.get("createdAt"),
            )
        except (KeyError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to parse account response: {e}")
            return None

    async def get_user(self, discord_id: int) -> Optional[User]:
        """
        Получает информацию о пользователе по его ID в Discord.

        :param discord_id: ID пользователя в Discord.
        :type discord_id: int

        :return: Объект User, представляющий пользователя.
        :rtype: :class:`User`
        """
        if not discord_id:
            raise ValueError("discord_id must be a non-empty integer")

        try:
            user = await super().get(f"users/{discord_id}")
            if user is None:
                return None

            cards = await super().get(f"accounts/{user['username']}/cards")
            if cards is None:
                cards = []

            return User(user["username"], user["uuid"], cards)
        except (KeyError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to parse user response: {e}")
            return None

    async def create_transaction(
        self, receiver: str, amount: int, comment: str
    ) -> Optional[int]:
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
        if not receiver:
            raise ValueError("receiver must be a non-empty string")
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("amount must be a positive integer")

        try:
            data = {"receiver": receiver, "amount": amount, "comment": comment}
            response = await super().post("transactions", data)

            if response is None:
                return None

            return int(response.get("balance", 0))
        except (KeyError, ValueError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to create transaction: {e}")
            return None
        except InsufficientBalanceError as ibe:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Insufficient balance for transaction: {ibe}")
            return None

    async def create_payment(
        self, webhook_url: str, redirect_url: str, data: str, items: list[Item]
    ) -> Optional[str]:
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
        if not webhook_url or not redirect_url:
            raise ValueError("webhook_url and redirect_url must be non-empty strings")
        if not items or len(items) == 0:
            raise ValueError("items must contain at least one item")

        try:
            payload = {
                "items": items,
                "redirectUrl": redirect_url,
                "webhookUrl": webhook_url,
                "data": data,
            }

            response = await super().post("payments", payload)

            if response is None:
                return None

            return str(response.get("url", ""))
        except (KeyError, ValueError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to create payment: {e}")
            return None

    async def update_webhook(self, url: str) -> Optional[dict]:
        """
        Обновляет URL вебхука, связанного с картой.

        :param url: Новый URL вебхука.
        :return: Ответ API в виде словаря или None при ошибке.
        """
        if not url:
            raise ValueError("url must be a non-empty string")

        try:
            data = {"url": url}
            response = await super().put("card/webhook", data)

            if response is None:
                return None

            return response
        except (KeyError, TypeError) as e:
            log = __import__("logging").getLogger("pyspapi")
            log.error(f"Failed to update webhook: {e}")
            return None

    def webhook_verify(self, data: str, header: str) -> bool:
        """
        Проверяет достоверность вебхука.

        :param data: Данные из вебхука.
        :type data: str
        :param header: Заголовок X-Body-Hash из вебхука.

        :return: True, если заголовок из вебхука достоверен, иначе False.
        :rtype: bool
        """
        hmac_data = b64encode(new(self.__token.encode("utf-8"), data, sha256).digest())
        return compare_digest(hmac_data, header.encode("utf-8"))

    def to_dict(self) -> dict:
        """
        Преобразует объект SPAPI в словарь.

        :return: Словарное представление объекта SPAPI.
        :rtype: dict
        """
        return self.__dict__.copy()
