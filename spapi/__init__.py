# pyspapi by deesiigneer
#

import hmac
import hashlib
import base64

from requests import post, get


class Error(Exception):
    pass


class ApiError(Error):
    pass


class Api:

    def __init__(self, card_id: str, token: str):
        self.id = card_id
        self.token = token
        self.header = {
            'Authorization': f"Bearer {str(base64.b64encode(str(f'{self.id}:{self.token}').encode('utf-8')), 'utf-8')}",
        }

    def _fetch(self, path, data):
        if path is None:
            result = get(url=f'https://spworlds.ru/api/public/users/{data}',
                         headers=self.header)
        else:
            result = post(
                url=f'https://spworlds.ru/api/public/{path}',
                headers=self.header,
                json=data
            )
        if result.status_code == [200, 400]:
            ApiError(f'Ошибка при запросе к API {result.status_code}')

        return result.json()

    def payment(self, amount, redirecturl, webhookurl, data):
        """
        Создание запроса на оплату.

        :param amount: Стоимость покупки в АРах.
        :param redirecturl: URL страницы, на которую попадет пользователь после оплаты.
        :param webhookurl: URL, куда наш сервер направит запрос, чтобы оповестить ваш сервер об успешной оплате.
        :param data: Строка до 100 символов, сюда можно поместить любые полезные данных.

        :return: url - Ссылка на страницу оплаты, на которую стоит перенаправить пользователя.
        """
        return self._fetch('payment', data={'amount': amount,
                                            'redirectUrl': redirecturl,
                                            'webhookUrl': webhookurl,
                                            'data': data})

    def webhook_verify(self, data, header):
        """
        Проверяет достоверность webhook'а.

        :param data : data из webhook.
        :param  header : headers из webhook.

        :return: Если header из webhook'а достоверен возвращает True, иначе False
        """
        hmac_data = base64.b64encode(hmac.new(self.token.encode('utf-8'), data, hashlib.sha256).digest())
        return hmac.compare_digest(hmac_data, header.encode('utf-8'))

    def transaction(self, receiver, amount, comment):
        """
        Перевод АР на карту.

        :param receiver : Номер карты получателя.

        :param amount: Количество АР для перевода.

        :param comment: Комментарий для перевода.
        """
        return self._fetch('transactions', data={'receiver': receiver,
                                                 'amount': amount,
                                                 'comment': comment})

    def check_user(self, discord_user_id):
        """
        Проверка на наличие проходки
        :param discord_user_id: ID пользователя в Discord.

        :return: username - Ник пользователя или null, если у пользователя нет проходки на сервер.
        """
        return self._fetch(None, data=discord_user_id)
