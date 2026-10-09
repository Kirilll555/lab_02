import csv
import json
import logging

from .errors import StreamStatsError
from .models import Event, validate

logger = logging.getLogger(__name__)

def csv_parser(file, skip_invalid=False, counter=None):
    csv_reader = csv.DictReader(file)
    for num, line in enumerate(csv_reader, start=2):
        try:
            event = Event(
                timestamp=line['timestamp'],
                level=line['level'],
                source=line['source'],
                message=line['message'],
            )
            validate(event)
            yield event
        except (StreamStatsError, KeyError):
            if skip_invalid:
                logger.warning(f'Пропущена строка {num}')
                if counter is not None:
                    counter['skipped'] += 1
                continue
            raise
def jsonl_parser(file, skip_invalid=False, counter=None):
    for num, line in enumerate(file, start=1):
        try:
            data = json.loads(line)
            event = Event(
                timestamp=data['timestamp'],
                level=data['level'],
                source=data['source'],
                message=data['message'],
            )
            validate(event)
            yield event
        except (StreamStatsError, KeyError, json.JSONDecodeError):
            if skip_invalid:
                logger.warning(f'Пропущена строка {num}')
                if counter is not None:
                    counter['skipped'] += 1
                continue
            raise
