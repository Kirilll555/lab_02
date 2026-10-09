# streamstats

Консольный анализатор логов

## Установка

pip install -e .

## Использование

python -m streamstats analyze events.csv --format csv --output report.json

python -m streamstats analyze events.jsonl --format jsonl --output report.json

python -m streamstats analyze events.jsonl --format jsonl --output report.json --skip-invalid

## Проверка

python -m pytest

python -m ruff check .