"""
Тесты для core.reports

Покрываемые классы/функции:
- BaseReport (абстрактно)
- ReportEngine.register / ReportEngine.run
- register_report decorator
- AverageReport.generate

Что проверяется:
- корректное поведение AverageReport (агрегация и вычисление среднего)
- ReportEngine.run бросает ValueError для неизвестного имени
- регистрация нового отчёта работает, повторная регистрация с тем же именем бросает ValueError
"""

import pytest
from core.reports import ReportEngine, register_report, BaseReport
from core.log_models import LogEntry


@pytest.fixture
def reset_report_registry():
    ReportEngine._registry.clear()
    yield
    ReportEngine._registry.clear()


@pytest.fixture
def entries_for_reports():
    return [
        LogEntry(url="/a", response_time=100.0, status=200, request_method="GET", timestamp="2023-10-01T10:00:00Z"),
        LogEntry(url="/a", response_time=300.0, status=200, request_method="GET", timestamp="2023-10-01T11:00:00Z"),
        LogEntry(url="/b", response_time=50.0, status=404, request_method="GET", timestamp="2023-10-01T12:00:00Z"),
    ]


def test_average_report_computes_table(entries_for_reports):
    result = ReportEngine.run("average", entries_for_reports)
    assert isinstance(result, dict) and "table_data" in result
    rows = result["table_data"]
    assert ["/a", 2, 200.0] in rows
    assert ["/b", 1, 50.0] in rows


def test_report_engine_unknown_report(entries_for_reports):
    with pytest.raises(ValueError):
        ReportEngine.run("unknown", entries_for_reports)


def test_register_report_and_duplicate(reset_report_registry):
    class DummyReport(BaseReport):
        def generate(self, entries, **params):
            return {"ok": True}

    # регистрация отчёта
    register_report("dummy")(DummyReport)
    assert ReportEngine.run("dummy", []) == {"ok": True}

    # повторная регистрация должна вызывать ValueError
    with pytest.raises(ValueError, match="Отчёт 'dummy' уже зарегистрирован"):
        register_report("dummy")(DummyReport)