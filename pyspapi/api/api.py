import asyncio
import json
from base64 import b64encode
from logging import NullHandler, getLogger
from typing import Any, Dict, Optional

import aiohttp

from pyspapi.exceptions import (
    BadRequestError,
    ClientError,
    ForbiddenError,
    HTTPError,
    InsufficientBalanceError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    ServerError,
    SPAPIError,
    UnauthorizedError,
    ValidationError,
)
from pyspapi.exceptions import (
    TimeoutError as APITimeoutError,
)

log = getLogger("pyspapi")
log.addHandler(NullHandler())


class APISession(object):
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
        self._validate_credentials(card_id, token)

        self.__url = "https://spworlds.ru/api/public/"
        self.__id = card_id
        self.__token = token
        self.__sleep_timeout = sleep_time
        self.__retries = retries
        self.__timeout = timeout
        self.__raise_exception = raise_exception
        self.__proxy = proxy
        self.session: Optional[aiohttp.ClientSession] = None
        self._session_owner = False

    @staticmethod
    def _validate_credentials(card_id: str, token: str) -> None:
        if not card_id or not isinstance(card_id, str):
            raise ValueError("card_id must be a non-empty string")
        if not token or not isinstance(token, str):
            raise ValueError("token must be a non-empty string")

    async def __aenter__(self):
        try:
            if not self.session:
                self.session = aiohttp.ClientSession(
                    json_serialize=json.dumps,
                    timeout=aiohttp.ClientTimeout(total=self.__timeout),
                    proxy=self.__proxy,
                )
                self._session_owner = True
                log.debug(f"[pyspapi] Session created with timeout={self.__timeout}s")
            else:
                self._session_owner = False
        except Exception as e:
            log.error(f"[pyspapi] Failed to create session: {e}")
            raise
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session_owner and self.session:
            try:
                await self.session.close()
                log.debug("[pyspapi] Session closed")
            except Exception as e:
                log.error(f"[pyspapi] Error closing session: {e}")
            self.session = None

        return False

    def _get_auth_header(self) -> str:
        credentials = f"{self.__id}:{self.__token}"
        encoded = b64encode(credentials.encode("utf-8")).decode("utf-8")
        return f"Bearer {encoded}"

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": self._get_auth_header(),
            "User-Agent": "https://github.com/deesiigneer/pyspapi",
            "Content-Type": "application/json",
        }

    def _parse_error_response(self, content: str) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"raw_response": content}

    def _format_error_message(
        self, error_data: Dict[str, Any], status_code: int
    ) -> str:
        message = (
            error_data.get("message")
            or error_data.get("detail")
            or error_data.get("msg")
            or f"HTTP {status_code}"
        )

        if "error" in error_data:
            message = f"{message} (error: {error_data['error']})"

        return message

    def _log_error_with_details(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        error_data: Dict[str, Any],
        content: str,
    ) -> None:
        message = self._format_error_message(error_data, status_code)

        log.error(
            f"[pyspapi] HTTP {status_code}: {method.upper()} {endpoint} | {message}"
        )

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        if attempt > self.__retries:
            return False
        return status_code in {408, 429, 500, 502, 503, 504}

    async def _handle_http_error(
        self,
        method: str,
        endpoint: str,
        status_code: int,
        content: str,
    ) -> None:
        error_data = self._parse_error_response(content)

        self._log_error_with_details(method, endpoint, status_code, error_data, content)

        if not self.__raise_exception:
            return

        error_message = self._format_error_message(error_data, status_code)

        if status_code == 400:
            error_code = error_data.get("error", "")
            if "notEnoughBalance" in error_code:
                raise InsufficientBalanceError(details=error_data)
            raise BadRequestError(details=error_data)
        elif status_code == 401:
            raise UnauthorizedError(details=error_data)
        elif status_code == 403:
            raise ForbiddenError(details=error_data)
        elif status_code == 404:
            raise NotFoundError(resource=endpoint, details=error_data)
        elif status_code == 422:
            raise ValidationError(error_data)
        elif status_code == 429:
            retry_after = error_data.get("retry_after")
            raise RateLimitError(retry_after=retry_after, details=error_data)
        elif 400 <= status_code < 500:
            raise ClientError(
                status_code=status_code,
                message=error_message,
                response_body=content,
                details=error_data,
            )
        elif 500 <= status_code < 600:
            raise ServerError(
                status_code=status_code,
                message=error_message,
                response_body=content,
                details=error_data,
            )
        else:
            raise HTTPError(
                status_code=status_code,
                message=error_message,
                response_body=content,
                details=error_data,
            )

    async def request(
        self, method: str, endpoint: str, data: Optional[Dict] = None
    ) -> Any:
        url = self.__url + endpoint
        headers = self._get_headers()

        attempt = 0

        while True:
            attempt += 1
            if attempt > 1:
                log.warning(
                    f"[pyspapi] Retry attempt {attempt}/{self.__retries + 1}: {method.upper()} {endpoint}"
                )

            try:
                async with self.session.request(
                    method, url, json=data, headers=headers
                ) as resp:
                    response_text = await resp.text()

                    if resp.status == 422:
                        try:
                            errors = json.loads(response_text)
                        except json.JSONDecodeError:
                            errors = {"raw_response": response_text}

                        error_msg = self._format_error_message(errors, 422)
                        log.error(
                            f"[pyspapi] Validation error (422): {method.upper()} {endpoint} | {error_msg}"
                        )
                        if self.__raise_exception:
                            raise ValidationError(errors)
                        return None

                    if resp.status >= 400:
                        await self._handle_http_error(
                            method, endpoint, resp.status, response_text
                        )

                        if self._should_retry(resp.status, attempt):
                            await asyncio.sleep(self.__sleep_timeout * attempt)
                            continue

                        return None

                    try:
                        return await resp.json()
                    except json.JSONDecodeError as e:
                        log.error(
                            f"[pyspapi] Failed to parse JSON response: {e} | Status: {resp.status}"
                        )
                        if self.__raise_exception:
                            raise SPAPIError(
                                status_code=resp.status,
                                message="Invalid JSON in response",
                                details={
                                    "error": str(e),
                                    "response": response_text[:500],
                                },
                            )
                        return None

            except asyncio.TimeoutError:
                log.warning(
                    f"[pyspapi] Request timeout ({self.__timeout}s): {method.upper()} {endpoint} | Attempt {attempt}/{self.__retries + 1}"
                )

                if self._should_retry(408, attempt):
                    await asyncio.sleep(self.__sleep_timeout * attempt)
                    continue

                log.error("[pyspapi] Max retries reached for timeout")
                if self.__raise_exception:
                    raise APITimeoutError(
                        timeout=self.__timeout,
                        endpoint=endpoint,
                        details={"method": method, "attempt": attempt},
                    )
                return None

            except aiohttp.ClientSSLError as e:
                log.error(f"[pyspapi] SSL error: {e} | {method.upper()} {endpoint}")
                if self.__raise_exception:
                    raise NetworkError(
                        message=f"SSL error: {str(e)}",
                        details={
                            "method": method,
                            "endpoint": endpoint,
                            "error": str(e),
                        },
                    )
                return None

            except (aiohttp.ClientConnectorError, aiohttp.ClientOSError) as e:
                log.warning(
                    f"[pyspapi] Connection error: {e} | {method.upper()} {endpoint} | Attempt {attempt}/{self.__retries + 1}"
                )

                if self._should_retry(0, attempt):
                    await asyncio.sleep(self.__sleep_timeout * attempt)
                    continue

                log.error("[pyspapi] Max retries reached for connection error")
                if self.__raise_exception:
                    raise NetworkError(
                        message=f"Connection error: {str(e)}",
                        details={
                            "method": method,
                            "endpoint": endpoint,
                            "error": str(e),
                            "attempt": attempt,
                        },
                    )
                return None

            except aiohttp.ClientError as e:
                log.error(f"[pyspapi] Client error: {e} | {method.upper()} {endpoint}")
                if self.__raise_exception:
                    raise NetworkError(
                        message=f"HTTP client error: {str(e)}",
                        details={
                            "method": method,
                            "endpoint": endpoint,
                            "error": str(e),
                        },
                    )
                return None

            except SPAPIError:
                raise
            except Exception as e:
                log.exception(
                    f"[pyspapi] Unexpected error: {e} | {method.upper()} {endpoint}"
                )
                if self.__raise_exception:
                    raise SPAPIError(
                        message=f"Unexpected error: {str(e)}",
                        details={
                            "error": str(e),
                            "method": method,
                            "endpoint": endpoint,
                        },
                    )
                return None

    async def get(self, endpoint: str) -> Any:
        async with self:
            return await self.request("GET", endpoint)

    async def post(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        async with self:
            return await self.request("POST", endpoint, data)

    async def put(self, endpoint: str, data: Optional[Dict] = None) -> Any:
        async with self:
            return await self.request("PUT", endpoint, data)
