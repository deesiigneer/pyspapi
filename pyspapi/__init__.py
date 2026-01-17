"""pyspapi - API wrapper for SP servers written in Python
TODO: заполнить описание"""

import importlib.metadata
from .spworlds import SPAPI

__all__ = [SPAPI]

__author__: str = "deesiigneer"
__url__: str = "https://github.com/deesiigneer/pyspapi"
__description__: str = "API wrapper for SP servers written in Python."
__license__: str = "MIT"
__version__: str = importlib.metadata.version("pyspapi")
