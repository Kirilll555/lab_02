def build_report(stats):
    return {
        'count': stats['count'],
        'level': stats['lvl'],
        'source': stats['src'],
        'top_5_errors': stats['top_5'],
        'first_time_stamp': stats['first'],
        'last_time_stamp': stats['last'],
        'skipped': stats.get('skipped', 0)
    }
