from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class LogEntry:
    """Структура для одной записи лога"""
    url: str
    response_time: float
    status: int
    request_method: str
    timestamp: str
    user_agent: Optional[str] = None
    
   