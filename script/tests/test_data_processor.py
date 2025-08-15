"""
Тесты для core.data_processor.get_json_data

Покрываемые функции:
- get_json_data(file_name, date=None, as_dataclass=False)

Что проверяется:
- чтение валидных ndjson-строк (включая пропуск пустых/битых строк)
- фильтрация по дате (YYYY-MM-DD)
- возврат dataclass LogEntry при as_dataclass=True
- поведение при несуществующем файле (возвращает пустой список)
- пропуск строк с некорректными полями при as_dataclass=True
"""

import json
import pytest
from pathlib import Path
from core.data_processor import get_json_data
from core.log_models import LogEntry


# ------------------- фикстуры -------------------
@pytest.fixture
def ndjson_file(tmp_path):
    p = tmp_path / "test1.ndjson"
    lines = [
        json.dumps({"@timestamp": "2023-10-01T12:00:00Z", "url": "/a", "response_time": 100, "status": 200, "request_method": "GET"}),
        json.dumps({"@timestamp": "2023-10-01T13:00:00Z", "url": "/b", "response_time": 150, "status": 200, "request_method": "POST"}),
        json.dumps({"@timestamp": "2023-10-02T14:00:00Z", "url": "/c", "response_time": 200, "status": 404, "request_method": "GET"}),
    ]
    p.write_text("\n".join(lines))
    return str(p)


@pytest.fixture
def another_ndjson_file(tmp_path):
    p = tmp_path / "test2.ndjson"
    lines = [
        json.dumps({"@timestamp": "2023-10-01T15:00:00Z", "url": "/d", "response_time": 300, "status": 500, "request_method": "PUT"}),
    ]
    p.write_text("\n".join(lines))
    return str(p)


# ------------------- тесты -------------------
def test_get_json_data_reads_valid_lines(ndjson_file):
    entries = get_json_data(ndjson_file)
    assert isinstance(entries, list)
    assert len(entries) == 3
    assert all(isinstance(e, dict) for e in entries)


@pytest.mark.parametrize(
    "date_str, expected_count",
    [
        ("2023-10-01", 2),
        ("2023-10-02", 1),
    ],
)
def test_get_json_data_date_filter(ndjson_file, date_str, expected_count):
    entries = get_json_data(ndjson_file, date=date_str)
    assert len(entries) == expected_count


def test_get_json_data_as_dataclass_and_multi_files(ndjson_file, another_ndjson_file):
    entries = get_json_data([ndjson_file, another_ndjson_file], as_dataclass=True)
    assert len(entries) == 4
    assert all(isinstance(e, LogEntry) for e in entries)


def test_get_json_data_nonexistent_file_returns_empty(tmp_path):
    p = tmp_path / "noexists.ndjson"
    entries = get_json_data(str(p))
    assert entries == []


def test_get_json_data_invalid_date_format_raises(ndjson_file):
    with pytest.raises(ValueError):
        get_json_data(ndjson_file, date="invalid-date")


def test_get_json_data_skip_invalid_fields(tmp_path):
    p = tmp_path / "bad_fields.ndjson"
    bad = {
        "@timestamp": "2023-10-01T00:00:00Z",
        "url": "/x",
        "response_time": "not-a-number",  # некорректное поле
        "status": 200,
        "request_method": "GET",
    }
    p.write_text(json.dumps(bad) + "\n")
    entries = get_json_data(str(p), as_dataclass=True)
    assert entries == []
