class CLIValidationError(Exception):
    """Базовое исключение для ошибок валидации CLI"""

    pass


class FileNotFoundError(CLIValidationError):
    """Файл не найден"""

    pass


class InvalidDateFormatError(CLIValidationError):
    """Неверный формат даты"""

    pass


class InvalidChoiceError(CLIValidationError):
    """Неверный выбор из списка"""

    pass
