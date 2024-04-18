from base64 import b64encode
from logging import getLogger
import aiohttp
import json


log = getLogger('pyspapi')


class APISession(object):
    """ Holds aiohttp session for its lifetime and wraps different types of request """

    def __init__(self, card_id: str, token: str, timeout=5, sleep_time=0.2, retries=0):
        self.__url = "https://spworlds.ru/"
        self.__id = card_id
        self.__token = token
        self.__sleep_timeout = sleep_time
        self.__retries = retries
        self.__timeout = timeout
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            json_serialize=json.dumps,
            timeout=aiohttp.ClientTimeout(total=self.__timeout))
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    def __get_url(self, endpoint: str) -> str:
        """ Get URL for requests """
        url = self.__url
        api = "api/public"
        return f"{url}{api}/{endpoint}"

    async def __request(self, method: str, endpoint: str, data=None):
        url = self.__get_url(endpoint)
        response = await self.session.request(
            method=method,
            url=url,
            json=data,
            headers={'Authorization': f"Bearer {str(b64encode(str(f'{self.__id}:{self.__token}').encode('utf-8')), 'utf-8')}",
                     'User-Agent': 'https://github.com/deesiigneer/pyspapi'},
            ssl=True
        )
        if response.status not in [200, 201]:
            message = await response.json()
            raise aiohttp.ClientResponseError(
                code=response.status,
                message=message['message'],
                headers=response.headers,
                history=response.history,
                request_info=response.request_info
            )
        return response

    async def get(self, endpoint, **kwargs):
        """ GET requests """
        try:
            return await self.__request("GET", endpoint, None, **kwargs)
        except aiohttp.ClientResponseError as e:
            log.error(f"GET request to {endpoint} failed with status {e.status}: {e.message}")
        except aiohttp.ClientError as e:
            log.error(f"GET request to {endpoint} failed: {e}")
        except Exception as e:
            log.error(f"GET request to {endpoint} failed: {e}")

    async def post(self, endpoint, data, **kwargs):
        """ POST requests """
        try:
            return await self.__request("POST", endpoint, data, **kwargs)
        except aiohttp.ClientResponseError as e:
            log.error(f"POST request to {endpoint} failed with status {e.status}: {e.message}")
        except aiohttp.ClientError as e:
            log.error(f"POST request to {endpoint} failed: {e}")
        except Exception as e:
            log.error(f"POST request to {endpoint} failed: {e}")

    async def put(self, endpoint, data, **kwargs):
        """ PUT requests """
        try:
            return await self.__request("PUT", endpoint, data, **kwargs)
        except aiohttp.ClientResponseError as e:
            log.error(f"PUT request to {endpoint} failed with status {e.status}: {e.message}")
        except aiohttp.ClientError as e:
            log.error(f"PUT request to {endpoint} failed: {e}")
        except Exception as e:
            log.error(f"PUT request to {endpoint} failed: {e}")