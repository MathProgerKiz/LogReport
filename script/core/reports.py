from abc import ABC, abstractmethod
from collections import defaultdict
from typing import List, Dict, Any, Iterable, Type

from core.log_models import LogEntry


class BaseReport(ABC):
    @abstractmethod
    def generate(self, entries: Iterable[LogEntry], **params: Any) -> Dict[str, Any]:
        pass


class ReportEngine:
    _registry: Dict[str, Type[BaseReport]] = {}

    @classmethod
    def register(cls, name: str, report_cls: Type[BaseReport]):
        if name in cls._registry:
            raise ValueError(f"Отчёт '{name}' уже зарегистрирован")
        cls._registry[name] = report_cls

    @classmethod
    def run(cls, name: str, entries: Iterable[LogEntry], **params) -> Dict[str, Any]:
        report_cls = cls._registry.get(name)
        if not report_cls:
            raise ValueError(f"Неизвестный отчёт: {name}. Доступные: {list(cls._registry.keys())}")
        report = report_cls()
        return report.generate(entries, **params)


def register_report(name: str):
    def wrapper(cls: Type[BaseReport]):
        ReportEngine.register(name, cls)
        return cls
    return wrapper


@register_report("average")
class AverageReport(BaseReport):
    def generate(self, entries: Iterable[LogEntry], **params: Any) -> Dict[str, Any]:
        stats: Dict[str, List[float]] = defaultdict(lambda: [0, 0.0])
        for e in entries:
            stats[e.url][0] += 1
            stats[e.url][1] += e.response_time

        rows = [[url, cnt, round(total / cnt, 3)] for url, (cnt, total) in stats.items()]
        rows.sort(key=lambda x: x[1], reverse=True)
        return {"table_data": rows}


