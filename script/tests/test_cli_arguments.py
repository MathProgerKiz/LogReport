"""
Тесты для cli.arguments.get_arguments

Покрываемые функции:
- get_arguments() (проверяем разбор аргументов через argparse)

Что проверяется:
- разбор одного файла и валидной даты
- разбор нескольких файлов (nargs="+")
- отсутствие обязательных аргументов вызывает SystemExit
- если валидатор даты бросает ошибку, argparse завершает программу (SystemExit)
"""

import sys
import os
import pytest
from cli.arguments import get_arguments


def test_get_arguments_parses_single_file_and_date(monkeypatch, tmp_path):
    f = tmp_path / "logs.ndjson"
    f.write_text('{"@timestamp":"2023-10-01T00:00:00Z","url":"/x","response_time":1,"status":200,"request_method":"GET","http_user_agent":"ua"}\n')

    # Для текущей реализации validate_date_format ожидается формат "%Y-%d-%m"
    argv = [
        "prog",
        "--file",
        str(f),
        "--report",
        "average",
        "--date",
        "2023-01-10",  # год=2023, день=01, месяц=10 -> соответствует "%Y-%d-%m"
    ]
    monkeypatch.setattr(sys, "argv", argv)
    args = get_arguments()
    assert isinstance(args.file, list)
    assert os.path.exists(args.file[0])
    assert args.report == "average"
    assert hasattr(args, "date")
    assert args.date == "2023-01-10"


def test_get_arguments_parsing_multiple_files(monkeypatch, tmp_path):
    f1 = tmp_path / "a.ndjson"
    f2 = tmp_path / "b.ndjson"
    f1.write_text("\n")
    f2.write_text("\n")
    argv = ["prog", "--file", str(f1), str(f2), "--report", "average"]
    monkeypatch.setattr(sys, "argv", argv)
    args = get_arguments()
    assert isinstance(args.file, list)
    assert len(args.file) == 2


def test_get_arguments_missing_required_args_causes_systemexit(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prog"])
    with pytest.raises(SystemExit):
        get_arguments()


def test_get_arguments_invalid_date_causes_systemexit(monkeypatch, tmp_path):
    f = tmp_path / "logs.ndjson"
    f.write_text("")
    argv = ["prog", "--file", str(f), "--report", "average", "--date", "bad-date"]
    monkeypatch.setattr(sys, "argv", argv)
    with pytest.raises(SystemExit):
        get_arguments()
