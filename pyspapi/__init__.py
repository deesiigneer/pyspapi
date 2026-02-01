"""
SPWorlds API Wrapper
~~~~~~~~~~~~~~~~~~~

High-level client for interacting with the SPWorlds API.

:copyright: (c) 2022-present deesiigneer
:license: MIT, see LICENSE for more details.
"""

import importlib.metadata

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
    TimeoutError,
    UnauthorizedError,
    ValidationError,
)
from pyspapi.spworlds import SPAPI

__all__ = [
    "SPAPI",
    "BadRequestError",
    "ClientError",
    "ForbiddenError",
    "HTTPError",
    "InsufficientBalanceError",
    "NetworkError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    "SPAPIError",
    "TimeoutError",
    "UnauthorizedError",
    "ValidationError",
]

__title__: str = "pyspapi"
__author__: str = "deesiigneer"
__description__: str = "API wrapper for SP servers written in Python."
__license__: str = "MIT"
__url__: str = "https://github.com/deesiigneer/pyspapi"
__copyright__: str = "2022-present deesiigneer"
__version__: str = importlib.metadata.version("pyspapi")
