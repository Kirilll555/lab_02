from dataclasses import dataclass
from datetime import datetime

from .errors import IncorrectEventError, IncorrectTimeStampError

levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
@dataclass
class Event:
    timestamp: str
    level: str
    source: str
    message: str

def validate(event):
    if event.level not in levels:
        raise IncorrectEventError(f'Неверно указан level {event.level}')
    if not event.source:
        raise IncorrectEventError('Введен пустой source')
    try:
        datetime.fromisoformat(event.timestamp)
    except ValueError:
        raise IncorrectTimeStampError(f'Неверная временная метка {event.timestamp}')
