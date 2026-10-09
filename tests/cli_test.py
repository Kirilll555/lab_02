import subprocess
import sys


def test_help_in_cli():
    result = subprocess.run(
        [sys.executable, '-m', 'streamstats', '--help'],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode == 0
def test_empty_command_in_cli():
    result = subprocess.run(
        [sys.executable, '-m', 'streamstats'],
        capture_output=True,
        text=True,
        check=False
    )
    assert result.returncode != 0

def test_analyze_csv_cli(tmp_path):
    file = tmp_path / 'test.csv'
    file.write_text(
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source,message\n'
    )
    out = tmp_path / 'report.json'
    result = subprocess.run(
        [
            sys.executable, '-m', 'streamstats', 'analyze',
            str(file), '--format', 'csv', '--output', str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert out.exists()

def test_cli_multiple_files(tmp_path):
    file1 = tmp_path / 'a.csv'
    file1.write_text(
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source1,message\n'
    )
    file2 = tmp_path / 'b.csv'
    file2.write_text(
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source2,message\n'
    )
    out = tmp_path / 'report.json'
    result = subprocess.run(
        [
            sys.executable, '-m', 'streamstats', 'analyze',
            str(file1), str(file2), '--format', 'csv', '--output', str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert out.exists()
def test_cli_skip_invalid(tmp_path):
    incorrect = tmp_path / 'incorrect.csv'
    incorrect.write_text(
        'timestamp,level,source,message\n'
        '2026-01-01T12:00:00,INFO,source,message\n'
        'неправильная,строка,без,полей\n'
    )
    out = tmp_path / 'report.json'
    result = subprocess.run(
        [
            sys.executable, '-m', 'streamstats', 'analyze',
            str(incorrect), '--format', 'csv', '--output', str(out),
            '--skip-invalid',
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert out.exists()
