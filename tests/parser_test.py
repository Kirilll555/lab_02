import io
import json

import pytest

from streamstats.errors import IncorrectEventError, IncorrectTimeStampError
from streamstats.models import Event, validate
from streamstats.parsers import csv_parser, jsonl_parser


def test_csv_parser():
    data = (
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source,message\n'
    )
    events = list(csv_parser(io.StringIO(data)))
    assert len(events) == 1
    assert events[0].level == 'INFO'

def test_jsonl_parser():
    data = (
        '{"timestamp": "2026-01-01T12:00:00", "level": "INFO", '
        '"source": "source", "message": "message"}\n'
    )
    events = list(jsonl_parser(io.StringIO(data)))
    assert len(events) == 1
    assert events[0].level == 'INFO'

def test_jsonl_parser_incorrect_line():
    data = 'incorrect'
    with pytest.raises(json.JSONDecodeError):
        list(jsonl_parser(io.StringIO(data)))

def test_validation():
    event = Event(
        timestamp='2026-01-01T12:00:00',
        level='INFO',
        source='source',
        message='message'
    )
    validate(event)

def test_validation_empty_timestamp():
    event = Event(
        timestamp='',
        level='INFO',
        source='source',
        message='message'
    )
    with pytest.raises(IncorrectTimeStampError):
        validate(event)

def test_validation_empty_level():
    event = Event(
        timestamp='2026-01-01T12:00:00',
        level='',
        source='source',
        message='message'
    )
    with pytest.raises(IncorrectEventError):
        validate(event)

def test_validation_empty_source():
    event = Event(
        timestamp='2026-01-01T12:00:00',
        level='INFO',
        source='',
        message='message'
    )
    with pytest.raises(IncorrectEventError):
        validate(event)

def test_validation_incorrect_timestamp():
    event = Event(
        timestamp='incorrect',
        level='INFO',
        source='source',
        message='message'
    )
    with pytest.raises(IncorrectTimeStampError):
        validate(event)

def test_validation_incorrect_level():
    event = Event(
        timestamp='2026-01-01T12:00:00',
        level='incorrect',
        source='source',
        message='message'
    )
    with pytest.raises(IncorrectEventError):
        validate(event)

def test_unicode():
    data = (
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,приложение,сообщение\n'
    )
    events = list(csv_parser(io.StringIO(data)))
    assert len(events) == 1
    assert events[0].source == 'приложение'
    assert events[0].message == 'сообщение'

def test_csv_parser_incorrect_line():
    data = (
        'timestamp,level,source,message\n'
        'неправильная,строка,без,полей\n'
    )
    with pytest.raises(IncorrectEventError):
        list(csv_parser(io.StringIO(data)))

def test_csv_parser_skip_invalid():
    data = (
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source,message\n'
        'неправильная,строка,без,полей\n'
    )
    counter = {'skipped': 0}
    events = list(csv_parser(io.StringIO(data), skip_invalid=True, counter=counter))
    assert len(events) == 1
    assert counter['skipped'] == 1

def test_csv_parser_empty():
    data = 'timestamp,level,source,message\n'
    events = list(csv_parser(io.StringIO(data)))
    assert events == []
