import argparse
from pathlib import Path
from typing import List
from datetime import datetime
from .exceptions import FileNotFoundError, InvalidDateFormatError, InvalidChoiceError


def _convert_to_argparse_error(func):
    """Декоратор для конвертации наших исключений в argparse.ArgumentTypeError"""

    def wrapper(value):
        try:
            return func(value)
        except (FileNotFoundError, InvalidDateFormatError, InvalidChoiceError) as e:
            raise argparse.ArgumentTypeError(str(e))

    return wrapper


@_convert_to_argparse_error
def validate_file_path(file_path: str) -> str:
    """Проверяет существование файла"""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    return str(path.absolute())


@_convert_to_argparse_error
def validate_date_format(date_str: str) -> str:
    """Проверяет формат даты (YYYY-DD-MM)"""
    try:
        datetime.strptime(date_str, "%Y-%d-%m")
        return date_str
    except ValueError:
        raise InvalidDateFormatError(
            f"Неверный формат даты: {date_str}. Используйте YYYY-DD-MM"
        )


def validate_choice(choices: List[str]):
    """Создает валидатор для выбора из списка значений"""

    @_convert_to_argparse_error
    def validator(value: str) -> str:
        if value not in choices:
            raise InvalidChoiceError(f"Выберите из: {', '.join(choices)}")
        return value

    return validator
