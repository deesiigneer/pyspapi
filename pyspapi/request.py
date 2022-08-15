import aiohttp
from .errors import handle
from typing import Coroutine, Any, TypeVar

T = TypeVar("T")
Response = Coroutine[Any, Any, T]

class Request:
    async def get(url: str, headers=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as session_response:
                try:
                    response = await session_response.json()
                except:
                    response = await session_response.text()
                if session_response.status == 404:
                    return None
                if not session_response.ok:
                    handle(response)
                return response

    async def post(url: str, payload, headers=None):
        async with aiohttp.ClientSession() as session:
            session_response = await session.post(url, json=payload, headers=headers)
            try:
                response = await session_response.json()
            except:
                response = await session_response.text()
            if not session_response.ok:
                handle(response)
            return response
