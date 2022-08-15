import ast
import warnings
import asyncio
from aiohttp import web
from sys import version_info
from base64 import b64encode, b64decode
from hmac import new, compare_digest
from hashlib import sha256
from logging import getLogger
from typing import Any, Dict, List, Optional, Union
from .types import SPUser, MojangProfile, UsernameToUUID
from .request import Request
from .errors import Error

log = getLogger('pyspapi')


class _BaseAPI:

    _SPWORLDS = "https://spworlds.ru/api/public"
    _API_MOJANG = "https://api.mojang.com"
    _SESSIONSERVER_MOJANG = "https://sessionserver.mojang.com"

    def __init__(self, card_id: str, token: str):
        """
        :param card_id:
        :param token:
        """
        self._id = card_id
        self._token = token

        self._HEADER = {
            'Authorization': f"Bearer {str(b64encode(str(f'{self._id}:{self._token}').encode('utf-8')), 'utf-8')}",
            'User-Agent': f'pyspapi (https://github.com/deesiigneer/pyspapi) '
                          f'Python {version_info.major}.{version_info.minor}.{version_info.micro}'
        }

    async def webhook_verify(self, data: str, header) -> bool:
        """
        Проверяет достоверность webhook'а. \n
        :param data: data из webhook.
        :param  header: header X-Body-Hash из webhook.
        :return: True если header из webhook'а достоверен, иначе False
        """
        print()
        hmac_data = b64encode(new(self._token.encode('utf-8'), data, sha256).digest())
        return compare_digest(hmac_data, header.encode('utf-8'))

    def listener(self, host: str = '127.0.0.1', port: int = 80, webhook_path: str = '/webhook/'):
        app = web.Application()
        async def handle(request):
            request_data = await request.read()
            header = request.headers.get('X-Body-Hash')
            if header is not None:
                if await self.webhook_verify(data=request_data, header=header) is True:
                    web.json_response(status=202)
                    return True
                else:
                    web.json_response(status=400)
            else:
                return web.json_response(status=404)
        app.add_routes([web.get(webhook_path, handle)])
        web.run_app(app, port=port, host=host)


class API(_BaseAPI):
    """
    class API
    """

    async def get_user(self, user_id: int) -> Optional[SPUser]:
        """
        Получение информации об игроке SP \n
        :param user_id: ID пользователя в Discord.
        :return: Class User.
        """
        sp_user = await Request.get(f'{self._SPWORLDS}/users/{str(user_id)}', self._HEADER)
        if sp_user is not None:
            return SPUser(await Request.get(f'{self._SPWORLDS}/users/{str(user_id)}', self._HEADER))
        else:
            return None

    async def get_users(self, user_ids: List[int]) -> Union[SPUser, Any]:
        """
        Получение никнеймов игроков в майнкрафте. **Максимально можно указать 60 user_ids, не используйте эту функцию
        чаще 1 раза в минуту если указали больше 60 user_ids**\n
        https://spworlds.readthedocs.io/ru/latest/index.html#id3\n
        :param user_ids: List[int] ID пользователей в Discord.
        :return: List[str] который содержит майнкрафт никнеймы игроков в том же порядке, который был задан, None если
            пользователь не найден или нет проходки.
        """
        if len(user_ids) > 60:
            user_ids = user_ids[:60]
            warnings.warn('user_ids больше чем 60. Уменьшено до 60.')
        tasks = []
        for user_id in user_ids:
            tasks.append(self.get_user(user_id))
        return await asyncio.gather(*tasks, return_exceptions=True)

    async def get_uuid(self, username: str) -> Optional[UsernameToUUID]:
        """
        Получить UUID игрока Minecraft.\n
        :param username: str никнейм игрока Minecraft.
        :return: Optional[str] UUID игрока Minecraft.
        """
        response = await Request.get(f'{self._API_MOJANG}/users/profiles/minecraft/{username}')
        return UsernameToUUID(await Request.get(f'{self._API_MOJANG}/users/profiles/minecraft/{username}'))

    async def get_uuids(self, usernames: list[str]) -> Dict[str, str]:
        """
        Получить UUID's игроков Minecraft. **Не больше 10**\n
        :param usernames: List[str] Список с никнеймами игроков Minecraft.
        :return: Dict[str, str] UUID игроков Minecraft.
        """
        if len(usernames) > 10:
            usernames = usernames[:10]
            warnings.warn('usernames больше чем 10. Уменьшено до 10.')
        return await Request.post(f'{self._API_MOJANG}/profiles/minecraft', payload=usernames)

    async def get_name_history(self, uuid: str) -> List[Dict[str, Any]]:
        """
        История никнеймов в Minecraft.\n
        :param uuid: UUID игрока Minecraft.
        :return: List[Dict[str, Any]] который содержит name и changed_to_at
        """
        requests = await Request.get(f"{self._API_MOJANG}/user/profiles/{uuid}/names")

        name_data = []
        for data in requests:
            name_data_dict = {"name": data["name"]}
            if data.get("changedToAt"):
                name_data_dict["changed_to_at"] = data["changedToAt"]
            else:
                name_data_dict["changed_to_at"] = 0
            name_data.append(name_data_dict)
        return name_data

    async def get_profile(self, uuid: str) -> MojangProfile:
        response = await Request.get(f'{self._SESSIONSERVER_MOJANG}/session/minecraft/profile/{uuid}')
        return MojangProfile(ast.literal_eval(b64decode(response["properties"][0]["value"]).decode()))

    async def payment(self, amount: int, redirect_url: str, webhook_url: str, data: str) -> Optional[str]:
        """
        Создание ссылки для оплаты.\n
        :param amount: Стоимость покупки в АРах.
        :param redirect_url: URL страницы, на которую попадет пользователь после оплаты.
        :param webhook_url: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
        :param data: Строка до 100 символов, сюда можно поместить любые полезные данных.
        :return: Ссылку на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        if len(data) > 100:
            raise Error('В data больше 100 символов')
        return await Request.post(f'{self._SPWORLDS}/payment',
                                  payload={
                                      'amount': amount,
                                      'redirectUrl': redirect_url,
                                      'webhookUrl': webhook_url,
                                      'data': data},
                                  headers=self._HEADER)

    async def transaction(self, receiver: int, amount: int, comment: str) -> Optional[str]:
        """
        Перевод АР на карту. \n
        :param receiver: Номер карты получателя.
        :param amount: Количество АР для перевода.
        :param comment: Комментарий для перевода.
        :return: True если перевод успешен, иначе False.
        """
        return 'Удачно' if await Request.post(f'{self._SPWORLDS}/transactions',
                                                 payload={'receiver': receiver,
                                                          'amount': amount,
                                                          'comment': comment},
                                                 headers=self._HEADER) else 'Что-то пошло не так...'

    @property
    async def balance(self) -> Optional[int]:
        """
        Проверка баланса карты \n
        :return: Количество АР на карте.
        """
        balance = await Request.get(f'{self._SPWORLDS}/card', headers=self._HEADER)
        return balance['balance']
