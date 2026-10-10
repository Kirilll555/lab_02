import argparse
import json
import os
import sys

from .analysis import analyze
from .errors import ConfigurationOfCLIError, StreamStatsError, UnsupportedFormatError
from .parsers import csv_parser, jsonl_parser
from .report import build_report


def events(files, fmt, skip_invalid, counter):
    if fmt not in ('csv', 'jsonl'):
        raise UnsupportedFormatError(f'Формат {fmt} не поддерживается')
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
    p_anlz.add_argument('--format', required=True)
    p_anlz.add_argument('--output', required=True)
    p_anlz.add_argument('--skip-invalid', action='store_true')
    args = par.parse_args()
    counter = {'skipped': 0}
    try:
        output_dir = os.path.dirname(args.output)
        if output_dir and not os.path.isdir(output_dir):
            raise ConfigurationOfCLIError(f'Директория не существует: {output_dir}')
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
