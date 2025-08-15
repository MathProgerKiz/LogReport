from datetime import datetime
import json
from pathlib import Path
from typing import List, Dict, Union, Optional
from core.log_models import LogEntry


def get_json_data(
    file_name: Union[str, List[str]],
    date: Optional[str] = None,
    as_dataclass: bool = False
) -> Union[List[LogEntry], List[Dict[str, any]]]:
    """
    Загружает JSON-логи из файла или списка файлов.

    Args:
        file_name: путь к файлу или список путей
        date: фильтр по дате в формате "YYYY-MM-DD"
        as_dataclass: если True, возвращает LogEntry, иначе dict

    Returns:
        Список LogEntry или dict
    """
    files = [file_name] if isinstance(file_name, str) else file_name
    result: List[Union[LogEntry, Dict[str, any]]] = []

    input_date: Optional[datetime.date] = None
    if date:
        try:
            input_date = datetime.strptime(date, "%Y-%d-%m").date()
        except ValueError:
            raise ValueError(f"Неверный формат даты: {date}, ожидается YYYY-dd-mm")

    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            continue  

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue  

                # фильтрация по дате
                if input_date:
                    ts = obj.get("@timestamp", "")
                    try:
                        ts_date = datetime.strptime(ts[:10], "%Y-%m-%d").date()
                        if ts_date != input_date:
                            continue
                    except ValueError:
                        continue  

                if as_dataclass:
                    try:
                        entry = LogEntry(
                            url=obj.get("url", ""),
                            response_time=float(obj.get("response_time") or 0.0),
                            status=int(obj.get("status") or 0),
                            request_method=obj.get("request_method", ""),
                            timestamp=obj.get("@timestamp", ""),
                            user_agent=obj.get("http_user_agent", "")
                        )
                        result.append(entry)
                    except (ValueError, TypeError):
                        continue  # некорректные поля
                else:
                    result.append(obj)

    return result
