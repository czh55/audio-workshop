#!/usr/bin/env python3
"""从已有 {base}.json 重新生成 txt/srt/vtt（不重新跑 Whisper）。

用法: python3 scripts/reformat_transcript.py <base> [<base>...]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from transcript_format import Segment, write_transcript_bundle


def reformat_one(base: str) -> bool:
    for candidate in (ROOT / f'{base}.json', ROOT / 'docs' / 'transcripts' / f'{base}.json'):
        if candidate.exists():
            src = candidate
            break
    else:
        print(f'[skip] {base} 无 json', flush=True)
        return False
    doc = json.loads(src.read_text(encoding='utf-8'))
    segments = [
        Segment(float(s['start']), float(s['end']), s['text'])
        for s in doc.get('segments', [])
        if (s.get('text') or '').strip()
    ]
    if not segments:
        print(f'[skip] {base} json 无有效分段', flush=True)
        return False
    stats = write_transcript_bundle(ROOT, base, segments, doc.get('language', 'zh'))
    print(
        f'[done] {base} 字数{stats["chars"]} 段数{stats["paragraphs"]} 句数{stats["segments"]}',
        flush=True,
    )
    return True


def main() -> None:
    bases = sys.argv[1:]
    if not bases:
        print('用法: python3 scripts/reformat_transcript.py <base> [<base>...]', flush=True)
        sys.exit(2)
    ok = sum(reformat_one(b) for b in bases)
    if not ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
