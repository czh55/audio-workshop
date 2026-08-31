#!/usr/bin/env python3
"""临时调度器：并发 ≤2 转录指定批次。用法: python3 scripts/run_transcribe.py <slug> [<slug>...]"""
import subprocess, time, sys, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONCURRENCY = 2
FILES = sys.argv[1:]


def is_done(base):
    p = ROOT / f'{base}.txt'
    return p.exists() and p.stat().st_size > 100


def start_one(base):
    log = open(ROOT / f'{base}-whisper.log', 'w')
    p = subprocess.Popen(
        ['python3', str(ROOT / 'scripts' / 'transcribe_one.py'), base, '4'],
        stdout=log, stderr=subprocess.STDOUT)
    print(f'[start] {base} {time.strftime("%H:%M:%S")}', flush=True)
    return p, log


queue = [f for f in FILES if not is_done(f)]
print(f'queue size: {len(queue)}', flush=True)
running = {}

while queue or running:
    while len(running) < CONCURRENCY and queue:
        base = queue.pop(0)
        p, log = start_one(base)
        running[base] = (p, log)
    done_bases = [b for b, (p, _) in running.items() if p.poll() is not None]
    for b in done_bases:
        p, log = running.pop(b)
        log.close()
        if is_done(b):
            print(f'[done] {b} {time.strftime("%H:%M:%S")}', flush=True)
        else:
            print(f'[FAIL] {b} rc={p.returncode}', flush=True)
    if not done_bases:
        time.sleep(20)

print('ALL TRANSCRIPTION DONE', time.strftime('%H:%M:%S'), flush=True)
