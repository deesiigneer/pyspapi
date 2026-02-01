from typing import Any, Dict, Optional


class SPAPIError(Exception):
    """
    Базовая ошибка для всех исключений, связанных с API SPWorlds.
    """

    def __init__(
        self,
        status_code: Optional[int] = None,
        message: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        error_msg = f"[{status_code}] {message}" if status_code else message
        super().__init__(error_msg)

    def __str__(self):
        if self.status_code:
            return f"{self.__class__.__name__}: [{self.status_code}] {self.message}"
        return f"{self.__class__.__name__}: {self.message}"

    def __repr__(self):
        return f"{self.__class__.__name__}(status_code={self.status_code}, message={self.message!r}, details={self.details!r})"


class ValidationError(SPAPIError):
    """
    Ошибка валидации (HTTP 422).
    """

    def __init__(self, errors: Dict[str, Any]):
        self.errors = errors
        super().__init__(
            status_code=422,
            message="Validation failed",
            details={"validation_errors": errors},
        )

    def __str__(self):
        return f"{self.__class__.__name__}: {self.errors}"


class NetworkError(SPAPIError):
    """
    Ошибка сетевого соединения.
    """

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message=message, details=details)


class TimeoutError(SPAPIError):
    """
    Ошибка истечения времени ожидания.
    """

    def __init__(
        self,
        timeout: float,
        endpoint: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        msg = f"Request timeout after {timeout}s"
        if endpoint:
            msg += f" for endpoint: {endpoint}"
        super().__init__(
            message=msg, details=details or {"timeout": timeout, "endpoint": endpoint}
        )


class HTTPError(SPAPIError):
    """
    Ошибка HTTP (4xx, 5xx).
    """

    def __init__(
        self,
        status_code: int,
        message: str = "",
        response_body: str = "",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.response_body = response_body
        super().__init__(
            status_code=status_code,
            message=message or f"HTTP {status_code}",
            details=details or {"response_body": response_body},
        )


class ClientError(HTTPError):
    """
    Ошибка клиента (4xx).
    """

    pass


class ServerError(HTTPError):
    """
    Ошибка сервера (5xx).
    """

    pass


class RateLimitError(ClientError):
    """
    Превышен лимит запросов (HTTP 429).
    """

    def __init__(
        self,
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.retry_after = retry_after
        msg = "Rate limit exceeded"
        if retry_after:
            msg += f". Retry after {retry_after}s"
        super().__init__(
            status_code=429,
            message=msg,
            details=details or {"retry_after": retry_after},
        )


class UnauthorizedError(ClientError):
    """
    Ошибка аутентификации (HTTP 401).
    """

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=401,
            message="Unauthorized. Invalid or missing credentials.",
            details=details,
        )


class ForbiddenError(ClientError):
    """
    Ошибка доступа (HTTP 403).
    """

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=403,
            message="Forbidden. Access denied.",
            details=details,
        )


class NotFoundError(ClientError):
    """
    Ресурс не найден (HTTP 404).
    """

    def __init__(self, resource: str = "", details: Optional[Dict[str, Any]] = None):
        msg = "Resource not found"
        if resource:
            msg += f": {resource}"
        super().__init__(
            status_code=404,
            message=msg,
            details=details or {"resource": resource},
        )


class BadRequestError(ClientError):
    """
    Некорректный запрос (HTTP 400).
    """

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            message="Bad request. Invalid request parameters.",
            details=details,
        )


class InsufficientBalanceError(ClientError):
    """
    Недостаточно средств на счете.
    """

    def __init__(self, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            status_code=400,
            message="Insufficient balance. Not enough funds to complete the transaction.",
            details=details or {"error": "error.public.transactions.notEnoughBalance"},
        )
