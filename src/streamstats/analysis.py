def analyze(events):
    count = 0
    lvl = {}
    src = {}
    err = {}
    first = None
    last = None
    for event in events:
        count += 1
        lvl[event.level] = lvl.get(event.level, 0) + 1
        src[event.source] = src.get(event.source, 0) + 1
        if event.level in ('ERROR', 'CRITICAL'):
            err[event.source] = err.get(event.source, 0) + 1
        if first is None or event.timestamp < first:
            first = event.timestamp
        if last is None or event.timestamp > last:
            last = event.timestamp
    top_5 = sorted(err.items(), key=lambda x: (-x[1], x[0]))[:5]
    return {
        'count': count,
        'lvl': lvl,
        'src': src,
        'top_5': top_5,
        'first': first,
        'last': last
    }
