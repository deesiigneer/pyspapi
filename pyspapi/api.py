import json.decoder
from sys import version_info
import ast
from base64 import b64encode, b64decode
from hmac import new, compare_digest
from hashlib import sha256
from logging import getLogger
from requests import get, post, Response
from typing import Any, Dict, List, Optional
from .models import MojangUserProfile, SPUserProfile
import warnings

log = getLogger('pyspapi')


class _Error(Exception):
    """

    """
    def __init__(self, message: Optional[str] = None):
        self.message = message if message else self.__class__.__doc__
        super().__init__(self.message)


class SPAPI:
    """
    class SPAPI
    """
    _SPWORLDS_DOMAIN_ = "https://spworlds.ru/api/public"

    def __init__(self, card_id: str, token: str):
        self.__id = card_id
        self.__token = token
        self.__header = {
            'Authorization': f"Bearer {str(b64encode(str(f'{self.__id}:{self.__token}').encode('utf-8')), 'utf-8')}",
            'User-Agent': f'pyspapi (https://github.com/deesiigneer/pyspapi) '
                          f'Python {version_info.major}.{version_info.minor}.{version_info.micro}'
        }
        self.balance = self.__check_balance()

    def __make_request(self, method: str, path: str, data: Optional[dict]) -> Optional[Response]:
        if method == 'GET':
            response = get(self._SPWORLDS_DOMAIN_ + path, headers=self.__header)
            return response
        elif method == 'POST':
            response = post(self._SPWORLDS_DOMAIN_ + path, headers=self.__header, json=data)
            return response

    def get_user(self, user_id: int) -> Optional[SPUserProfile]:
        """
        Получение информации об игроке SP \n
        :param user_id: ID пользователя в Discord.
        :return: Class SPUserProfile.
       """
        response = self.__make_request('GET', f'/users/{str(user_id)}', data=None)
        if not response.ok:
            return None
        try:
            username = response.json()['username']
            return SPUserProfile(access=True if username is not None else False, username=username)
        except json.decoder.JSONDecodeError:
            return

    def get_users(self, user_ids: List[int]) -> List[str]:
        """
        Получение никнеймов игроков в майнкрафте. **Не более 10**\n
        :param user_ids: List[int] ID пользователей в Discord.
        :return: List[str] который содержит майнкрафт никнеймы игроков в том же порядке, который был задан,
         None если пользователь не найден или нет проходки.
       """
        if len(user_ids) > 10:
            user_ids = user_ids[:10]
            warnings.warn('user_ids more than 10. Reduced to 10')
        nicknames_list = []
        for user_id in user_ids:
            nicknames_list.append(self.get_user(user_id).username
                                  if self.get_user(user_id) is not None else None)
        return nicknames_list

    def check_users_access(self, user_ids: List[int]) -> List[bool]:
        """
        Проверка наличия проходки у списка пользователей Discord. **Не более 10**\n
        :param user_ids: Список(List[int]) содержащий ID пользователей в Discord.
        :return: Список(List[bool]) в том же порядке, который был задан.True - проходка имеется, иначе False.
        """
        if len(user_ids) > 10:
            user_ids = user_ids[:10]
            warnings.warn('user_ids more than 10. Reduced to 10')
        ids_list = []
        for user_id in user_ids:
            ids_list.append(self.get_user(user_id).access
                            if self.get_user(user_id) is not None else None)
        return ids_list

    def payment(self, amount: int, redirect_url: str, webhook_url: str, data: str) -> Optional[str]:
        """
        Создание ссылки для оплаты.\n
        :param amount: Стоимость покупки в АРах.
        :param redirect_url: URL страницы, на которую попадет пользователь после оплаты.
        :param webhook_url: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
        :param data: Строка до 100 символов, сюда можно поместить любые полезные данных.
        :return: Ссылку на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        if len(data) > 100:
            raise _Error('В data больше 100 символов')
        body = {
            'amount': amount,
            'redirectUrl': redirect_url,
            'webhookUrl': webhook_url,
            'data': data
        }
        response = self.__make_request('POST', '/payment', data=body)
        if not response.ok:
            return None
        try:
            return response.json()['url']
        except json.decoder.JSONDecodeError:
            return None

    def webhook_verify(self, data: str, header) -> bool:
        """
        Проверяет достоверность webhook'а. \n
        :param data: data из webhook.
        :param  header: header X-Body-Hash из webhook.
        :return: True если header из webhook'а достоверен, иначе False
        """
        hmac_data = b64encode(new(self.__token.encode('utf-8'), data, sha256).digest())
        return compare_digest(hmac_data, header.encode('utf-8'))

    def transaction(self, receiver: int, amount: int, comment: str) -> Optional[str]:
        """
        Перевод АР на карту. \n
        :param receiver: Номер карты получателя.
        :param amount: Количество АР для перевода.
        :param comment: Комментарий для перевода.
        :return: True если перевод успешен, иначе False.
        """
        body = {
            'receiver': receiver,
            'amount': amount,
            'comment': comment
        }
        response = self.__make_request('POST', 'transactions', data=body)
        if not response.ok:
            return None
        try:
            return 'Success' if response.status_code == 200 else 'Fail'
        except json.decoder.JSONDecodeError:
            return None

    def __check_balance(self) -> Optional[int]:
        """
        Проверка баланса карты \n
        :return: Количество АР на карте.
        """
        response = self.__make_request('GET', '/card', None)
        if not response.ok:
            return None
        try:
            return response.json()['balance']
        except json.decoder.JSONDecodeError:
            return None


class MojangAPI:
    """
    class MojangAPI
    """

    _API_DOMAIN_ = "https://api.mojang.com"
    _SESSIONSERVER_DOMAIN_ = "https://sessionserver.mojang.com"

    @classmethod
    def __make_request(cls, server: str, method: str, path: str, data=Optional[dict]) -> Optional[Response]:
        if server == 'API':
            if method == 'GET':
                return get(cls._API_DOMAIN_ + path)
            elif method == 'POST':
                return post(cls._API_DOMAIN_ + path, json=data)
        elif server == 'SESSION':
            if method == 'GET':
                return get(cls._SESSIONSERVER_DOMAIN_ + path)

    @classmethod
    def get_uuid(cls, username: str) -> Optional[str]:
        """
        Получить UUID игрока Minecraft.\n
        :param username: str никнейм игрока Minecraft.
        :return: Optional[str] UUID игрока Minecraft.
        """
        response = cls.__make_request('API', 'GET', f'/users/profiles/minecraft/{username}')
        if not response.ok:
            return None

        try:
            return response.json()['id']
        except json.decoder.JSONDecodeError:
            return None

    @classmethod
    def get_uuids(cls, names: List[str]) -> Dict[str, str]:
        """
        Получить UUID's игроков Minecraft.\n
        :param names: List[str] Список с никнеймами игроков Minecraft.
        :return: Dict[str, str] UUID игрока Minecraft.

        """
        if len(names) > 10:
            names = names[:10]
        response = cls.__make_request('API', 'POST', '/profiles/minecraft', data=names).json()
        if not isinstance(response, list):
            if response.get('error'):
                raise ValueError(response['errorMessage'])
            else:
                raise _Error(response)
        return {uuids['name']: uuids['id'] for uuids in response}

    @classmethod
    def get_username(cls, uuid: str) -> Optional[str]:
        """
        Получить никнейм игрока.\n
        :param uuid: UUID игрока Minecraft.
        :return: Optional[str] в виде никнейма игрока Minecraft.
        """
        response = cls.__make_request('SESSION', 'GET', f'/session/minecraft/profile/{uuid}', None)
        if not response.ok:
            return None
        try:
            return response.json()["name"]
        except json.decoder.JSONDecodeError:
            return None

    @classmethod
    def get_profile(cls, uuid: str) -> Optional[MojangUserProfile]:
        """
        Профиль игрока Minecraft.\n
        :param uuid: UUID игрока Minecraft.
        :return: Class MojangUserProfile
        """
        response = cls.__make_request('SESSION', 'GET', f'/session/minecraft/profile/{uuid}')
        if not response.ok:
            return None
        try:
            value = response.json()["properties"][0]["value"]
        except (KeyError, json.decoder.JSONDecodeError):
            return None
        user_profile = ast.literal_eval(b64decode(value).decode())
        return MojangUserProfile(user_profile)

    @classmethod
    def get_name_history(cls, uuid: str) -> List[Dict[str, Any]]:
        """
        История никнеймов в Minecraft.\n
        :param uuid: UUID игрока Minecraft.
        :return: List[Dict[str, Any]] который содержит name и changed_to_at
        """
        requests = cls.__make_request('API', 'GET', f"/user/profiles/{uuid}/names")
        name_history = requests.json()

        name_data = []
        for data in name_history:
            name_data_dict = {"name": data["name"]}
            if data.get("changedToAt"):
                name_data_dict["changed_to_at"] = data["changedToAt"]
            else:
                name_data_dict["changed_to_at"] = 0
            name_data.append(name_data_dict)
        return name_data
