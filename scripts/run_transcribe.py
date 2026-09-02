#!/usr/bin/env python3
"""临时调度器：并发 ≤2 转录指定批次。用法: python3 scripts/run_transcribe.py <slug> [<slug>...]"""
import subprocess, time, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from transcript_format import has_timestamp_format

CONCURRENCY = 2
FILES = sys.argv[1:]


def is_done(base):
    p = ROOT / f'{base}.txt'
    if not p.exists() or p.stat().st_size <= 100:
        return False
    return has_timestamp_format(p.read_text(encoding='utf-8'))


def start_one(base):
    log = open(ROOT / f'{base}-whisper.log', 'w')
    p = subprocess.Popen(
        ['python3', str(ROOT / 'scripts' / 'transcribe_one.py'), base, '4', '--force'],
        stdout=log, stderr=subprocess.STDOUT)
    print(f'[start] {base} {time.strftime("%H:%M:%S")}', flush=True)
    return p, log


queue = list(FILES)
print(f'queue size: {len(queue)} (force re-transcribe)', flush=True)
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
