import asyncio
import json
from base64 import b64encode
from logging import getLogger
from typing import Optional, Any, Dict

import aiohttp

from ..exceptions import ValidationError, SPAPIError

log = getLogger('pyspapi')


class APISession(object):

    def __init__(self, card_id: str,
                 token: str,
                 timeout: int = 5,
                 sleep_time: float = 0.2,
                 retries: int = 0,
                 raise_exception: bool = False):
        self.__url = "https://spworlds.ru/api/public/"
        self.__id = card_id
        self.__token = token
        self.__sleep_timeout = sleep_time
        self.__retries = retries
        self.__timeout = timeout
        self.__raise_exception = raise_exception
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            json_serialize=json.dumps,
            timeout=aiohttp.ClientTimeout(total=self.__timeout))
        return self

    async def __aexit__(self, *err):
        await self.session.close()
        self.session = None

    async def request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Any:
        url = self.__url + endpoint
        headers = {
            'Authorization': f"Bearer {str(b64encode(str(f'{self.__id}:{self.__token}').encode('utf-8')), 'utf-8')}",
            'User-Agent': 'https://github.com/deesiigneer/pyspapi',
            "Content-Type": "application/json",
        }

        attempt = 0
        while True:
            attempt += 1
            if attempt > 1:
                log.warning(f'[pyspapi] Repeat attempt {attempt}: {method.upper()} {url}')
            try:
                async with self.session.request(method, url, json=data, headers=headers) as resp:
                    if resp.status == 422:
                        errors = await resp.json()
                        log.error(f"[pyspapi] Validation error: {errors}")
                        if self.__raise_exception:
                            raise ValidationError(errors)
                        return None

                    if resp.status >= 400:
                        content = await resp.text()
                        log.error(f"[pyspapi] API error {resp.status}: {content}")
                        if self.__raise_exception:
                            raise SPAPIError(resp.status, content)
                        return None

                    return await resp.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                log.exception(f"[pyspapi] Connection error: {e}")
                if attempt > self.__retries:
                    return None
                await asyncio.sleep(self.__sleep_timeout)

    async def get(self, endpoint: str) -> Any:
        async with self:
            return await self.request("GET", endpoint)

    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        async with self:
            return await self.request("POST", endpoint, data)

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        async with self:
            return await self.request("PUT", endpoint, data)
