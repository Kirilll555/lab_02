import argparse
import json
import sys

from .analysis import analyze
from .errors import StreamStatsError
from .parsers import csv_parser, jsonl_parser
from .report import build_report


def events(files, fmt, skip_invalid, counter):
    for file in files:
        with open(file) as f:
            if fmt == 'csv':
                yield from csv_parser(f, skip_invalid, counter)
            else:
                yield from jsonl_parser(f, skip_invalid, counter)
def main():
    par = argparse.ArgumentParser(prog='streamstats')
    sub = par.add_subparsers(dest='command', required=True)
    p_anlz = sub.add_parser('analyze', help='Проанализировать входные данные')
    p_anlz.add_argument('input', nargs='+', help='Входные данные')
    p_anlz.add_argument('--format', choices=['csv', 'jsonl'], required=True)
    p_anlz.add_argument('--output', required=True)
    p_anlz.add_argument('--skip-invalid', action='store_true')
    args = par.parse_args()
    counter = {'skipped': 0}
    try:
        stats = analyze(events(args.input, args.format, args.skip_invalid, counter))
        stats['skipped'] = counter['skipped']
        report = build_report(stats)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False)
    except StreamStatsError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
if __name__ == '__main__':
    main()
