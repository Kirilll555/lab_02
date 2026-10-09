from streamstats.analysis import analyze
from streamstats.models import Event
from streamstats.report import build_report


def test_analyze_empty_line():
    stats = analyze([])
    assert stats['count'] == 0
    assert stats['lvl'] == {}
    assert stats['src'] == {}
    assert stats['top_5'] == []
    assert stats['first'] is None
    assert stats['last'] is None

def test_analyze_one_line():
    events = [
        Event('2026-01-01T12:00:00', 'INFO', 'source', 'message')
    ]
    stats = analyze(events)
    assert stats['count'] == 1
    assert stats['lvl'] == {'INFO': 1}
    assert stats['src'] == {'source': 1}

def test_analyze_two_lines():
    events = [
        Event('2026-01-01T12:00:00', 'INFO', 'source_1', 'message'),
        Event('2026-01-01T12:00:00', 'CRITICAL', 'source_2', 'message')
    ]
    stats = analyze(events)
    assert stats['count'] == 2
    assert stats['lvl'] == {'INFO': 1, 'CRITICAL': 1}
    assert stats['src'] == {'source_1': 1, 'source_2': 1}
    assert stats['first'] == '2026-01-01T12:00:00'
    assert stats['last'] == '2026-01-01T12:00:00'

def test_analyze_several_lines():
    events = [
        Event('2026-01-01T12:00:00', 'INFO', 'source_1', 'message'),
        Event('2026-01-01T12:00:00', 'INFO', 'source_2', 'message'),
        Event('2026-01-01T12:00:00', 'INFO', 'source_3', 'message'),
    ]
    stats = analyze(events)
    assert stats['count'] == 3
    assert stats['src'] == {'source_1': 1, 'source_2': 1, 'source_3': 1}

def test_analyze_top5():
    events = [
        Event('2026-01-01T12:00:00', 'ERROR', 'source_1', 'message'),
        Event('2026-01-01T12:00:00', 'ERROR', 'source_1', 'message'),
        Event('2026-01-01T12:00:00', 'CRITICAL', 'source_2', 'new_message'),
    ]
    stats = analyze(events)
    assert stats['top_5'] == [('source_1', 2), ('source_2', 1)]

def test_build_report():
    stats = {
        'count': 1,
        'lvl': {'INFO': 1},
        'src': {'source': 1},
        'top_5': [],
        'first': '2026-01-01T12:00:00',
        'last': '2026-01-01T12:00:00',
    }
    report = build_report(stats)
    assert report['count'] == 1
    assert report['skipped'] == 0
