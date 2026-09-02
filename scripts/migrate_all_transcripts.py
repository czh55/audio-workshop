#!/usr/bin/env python3
"""批量迁移全部转录到新格式（时间戳 + 标点 + 段落）。

用法:
  python3 scripts/migrate_all_transcripts.py --reformat     # 仅有 json 的，秒级完成
  python3 scripts/migrate_all_transcripts.py --transcribe   # 无 json 的，需 Whisper
  python3 scripts/migrate_all_transcripts.py                # 先 reformat 再 transcribe
  python3 scripts/migrate_all_transcripts.py --status       # 查看进度
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from transcript_format import Segment, has_timestamp_format, write_transcript_bundle

ARCHIVE = ROOT / 'docs' / 'transcripts'
CONCURRENCY = 2


def list_txt_slugs() -> list[str]:
    return sorted(
        p.stem for p in ROOT.glob('*.txt')
        if p.name != 'requirements.txt' and p.stat().st_size > 100
    )


def needs_migration(slug: str) -> bool:
    txt = ROOT / f'{slug}.txt'
    if not txt.exists():
        return False
    return not has_timestamp_format(txt.read_text(encoding='utf-8'))


def find_json(slug: str) -> Path | None:
    for path in (ROOT / f'{slug}.json', ARCHIVE / f'{slug}.json'):
        if path.exists() and path.stat().st_size > 50:
            return path
    return None


def pending() -> dict[str, list[str]]:
    reform, trans = [], []
    for slug in list_txt_slugs():
        if not needs_migration(slug):
            continue
        if find_json(slug):
            reform.append(slug)
        elif any((ROOT / f'{slug}{ext}').exists() for ext in ('.m4a', '.mp3')):
            trans.append(slug)
    return {'reformat': reform, 'transcribe': trans}


def reformat_one(slug: str) -> bool:
    src = find_json(slug)
    if not src:
        print(f'[skip] {slug} 无 json', flush=True)
        return False
    doc = json.loads(src.read_text(encoding='utf-8'))
    segments = [
        Segment(float(s['start']), float(s['end']), s['text'])
        for s in doc.get('segments', [])
        if (s.get('text') or '').strip()
    ]
    if not segments:
        print(f'[skip] {slug} json 无有效分段', flush=True)
        return False
    stats = write_transcript_bundle(ROOT, slug, segments, doc.get('language', 'zh'))
    print(
        f'[reformat] {slug} 字数{stats["chars"]} 段数{stats["paragraphs"]} 句数{stats["segments"]}',
        flush=True,
    )
    return True


def run_reformat(slugs: list[str]) -> int:
    return sum(reformat_one(s) for s in slugs)


def is_transcribed(slug: str) -> bool:
    txt = ROOT / f'{slug}.txt'
    return txt.exists() and has_timestamp_format(txt.read_text(encoding='utf-8'))


def run_transcribe(slugs: list[str]) -> None:
    if not slugs:
        print('[transcribe] 无需重跑 Whisper', flush=True)
        return
    print(f'[transcribe] 队列 {len(slugs)} 篇，并发 {CONCURRENCY}', flush=True)
    queue = list(slugs)
    running: dict[str, tuple[subprocess.Popen, object]] = {}

    def start_one(base: str):
        log = open(ROOT / f'{base}-whisper.log', 'w')
        p = subprocess.Popen(
            ['python3', str(ROOT / 'scripts' / 'transcribe_one.py'), base, '4', '--force'],
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        print(f'[start] {base} {time.strftime("%H:%M:%S")}', flush=True)
        return p, log

    while queue or running:
        while len(running) < CONCURRENCY and queue:
            base = queue.pop(0)
            p, log = start_one(base)
            running[base] = (p, log)
        done = [b for b, (p, _) in running.items() if p.poll() is not None]
        for b in done:
            p, log = running.pop(b)
            log.close()
            if is_transcribed(b):
                print(f'[done] {b} {time.strftime("%H:%M:%S")}', flush=True)
            else:
                print(f'[FAIL] {b} rc={p.returncode}', flush=True)
        if not done:
            time.sleep(20)

    print('ALL TRANSCRIPTION DONE', time.strftime('%H:%M:%S'), flush=True)


def print_status() -> None:
    slugs = list_txt_slugs()
    done = sum(1 for s in slugs if not needs_migration(s))
    pend = pending()
    print(f'总计 {len(slugs)} 篇 | 已新格式 {done} | 待处理 {len(pend["reformat"]) + len(pend["transcribe"])}')
    print(f'  可 reformat（有 json）: {len(pend["reformat"])}')
    print(f'  需 transcribe（无 json）: {len(pend["transcribe"])}')
    if pend['reformat']:
        print('  reformat 样例:', ', '.join(pend['reformat'][:5]), '...')
    if pend['transcribe']:
        print('  transcribe 样例:', ', '.join(pend['transcribe'][:5]), '...')


def rebuild_index() -> None:
    subprocess.run(['python3', str(ROOT / 'scripts' / 'build_transcripts_index.py')], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description='迁移全部转录到新格式')
    parser.add_argument('--reformat', action='store_true', help='只从 json 重排版')
    parser.add_argument('--transcribe', action='store_true', help='只重跑 Whisper')
    parser.add_argument('--status', action='store_true', help='查看进度')
    parser.add_argument('--no-index', action='store_true', help='跳过重建索引')
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    do_reformat = args.reformat or not args.transcribe
    do_transcribe = args.transcribe or not args.reformat

    pend = pending()
    if do_reformat and pend['reformat']:
        print(f'=== reformat {len(pend["reformat"])} 篇 ===', flush=True)
        run_reformat(pend['reformat'])

    if do_transcribe:
        pend = pending()
        if pend['transcribe']:
            print(f'=== transcribe {len(pend["transcribe"])} 篇 ===', flush=True)
            run_transcribe(pend['transcribe'])

    if not args.no_index:
        rebuild_index()

    print_status()


if __name__ == '__main__':
    main()
