"""
Тесты для core.parameter_handlers

Покрываемые функции:
- validate_file_path(file_path)
- validate_date_format(date_str)
- validate_choice(choices) -> validator

Что проверяется:
- корректная проверка существующего файла
- генерация argparse.ArgumentTypeError для несуществующего пути
- проверка формата даты (в текущей реализации validate_date_format использует "%Y-%d-%m")
- validate_choice корректно принимает допустимые значения и бросает ошибку для недопустимых
"""

import argparse
import os
import pytest
from cli import parameter_handlers as ph


def test_validate_file_path_ok(tmp_path):
    p = tmp_path / "file.txt"
    p.write_text("ok")
    res = ph.validate_file_path(str(p))
    assert os.path.isabs(res)
    assert os.path.exists(res)


def test_validate_file_path_missing_raises():
    with pytest.raises(argparse.ArgumentTypeError):
        ph.validate_file_path("/this/path/does/not/exist.xyz")


@pytest.mark.parametrize(
    "date_input, should_pass",
    [
        ("2023-15-08", True),   # соответствует формату "%Y-%d-%m" (год-день-месяц)
        ("2023-08-15", False),  # обычно YYYY-MM-DD — в нашей реализации это невалидно
        ("not-a-date", False),
    ],
)
def test_validate_date_format_parametrized(date_input, should_pass):
    if should_pass:
        assert ph.validate_date_format(date_input) == date_input
    else:
        with pytest.raises(argparse.ArgumentTypeError):
            ph.validate_date_format(date_input)


def test_validate_choice_ok_and_bad():
    validator = ph.validate_choice(["a", "b"])
    assert validator("a") == "a"
    with pytest.raises(argparse.ArgumentTypeError):
        validator("c")
