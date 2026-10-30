"""Small cross-platform entry point for plans, checks, and smoke runs."""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def call(command):
    print(' '.join(map(str, command)), flush=True)
    raise SystemExit(subprocess.call(command, cwd=ROOT))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='action', required=True)
    check = sub.add_parser('check')
    check.add_argument('--family', choices=['dimensional', 'seed'], required=True)
    plan = sub.add_parser('plan')
    plan.add_argument('--family', choices=['dimensional', 'seed'], required=True)
    plan.add_argument('--data-root', type=Path, required=True)
    smoke = sub.add_parser('smoke')
    smoke.add_argument('--family', choices=['dimensional', 'seed'], required=True)
    smoke.add_argument('--data-root', type=Path, required=True)
    args = parser.parse_args()

    folder = ROOT / 'pipelines' / ('dimensional' if args.family == 'dimensional' else 'seed_series')
    if args.action == 'check':
        call([sys.executable, str(folder / 'selftest.py')])
    if args.family == 'dimensional':
        command = [sys.executable, '-u', str(folder / 'suite.py'), '--windows-root', str(args.data_root),
                   '--experiments', '1', '--datasets', 'DREAMER', '--targets', 'valence',
                   '--protocols', 'subject_independent']
    else:
        command = [sys.executable, '-u', str(folder / 'suite.py'), '--data-root', str(args.data_root),
                   '--experiments', '1', '--datasets', 'SEED', '--protocols', 'subject_independent']
    if args.action == 'smoke':
        command += ['--smoke', '--execute']
    call(command)


if __name__ == '__main__':
    main()
