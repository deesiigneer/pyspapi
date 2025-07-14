class SPAPIError(Exception):
    """
    Базовая ошибка для всех исключений, связанных с API SPWorlds.
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"[{status_code}] {message}")

    def __str__(self):
        return f"SPAPIError: [{self.status_code}] {self.message}"


class ValidationError(SPAPIError):
    """
    Ошибка валидации.
    """

    def __init__(self, errors):
        self.errors = errors
        super().__init__(422, f"Validation failed: {errors}")

    def __str__(self):
        return f"ValidationError: {self.errors}"
