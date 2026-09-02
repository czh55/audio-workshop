#!/usr/bin/env python3
"""单篇 faster-whisper 转录 worker。

用法: python3 scripts/transcribe_one.py <base> [<cpu_threads>] [--force]

产出（仓库根目录）：
- {base}.txt   带 [MM:SS - MM:SS] 段落头 + 中文标点
- {base}.srt   字幕
- {base}.vtt   WebVTT
- {base}.json  分段 JSON（含 start/end/text）
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))

from transcript_format import Segment, has_timestamp_format, write_transcript_bundle

INITIAL_PROMPT = '以下是普通话的句子。请使用正确的中文标点符号。'


def main() -> None:
    args = [a for a in sys.argv[1:] if a]
    force = '--force' in args
    args = [a for a in args if a != '--force']
    if not args:
        print('用法: python3 scripts/transcribe_one.py <base> [<cpu_threads>] [--force]', flush=True)
        sys.exit(2)

    base = args[0]
    threads = int(args[1]) if len(args) > 1 else 4

    audio = None
    for ext in ('.m4a', '.mp3'):
        p = ROOT / f'{base}{ext}'
        if p.exists():
            audio = p
            break
    if audio is None:
        print(f'[FAIL] {base} 无音频文件', flush=True)
        sys.exit(1)

    txt = ROOT / f'{base}.txt'
    if not force and txt.exists() and txt.stat().st_size > 100:
        existing = txt.read_text(encoding='utf-8')
        if has_timestamp_format(existing):
            print(f'[skip] {base} 已是带时间戳格式（加 --force 可重跑）', flush=True)
            return

    from faster_whisper import WhisperModel
    model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=threads)

    t0 = time.time()
    raw_segments, info = model.transcribe(
        str(audio),
        language='zh',
        beam_size=5,
        vad_filter=True,
        initial_prompt=INITIAL_PROMPT,
    )
    segments = [
        Segment(float(seg.start), float(seg.end), (seg.text or '').strip())
        for seg in raw_segments
        if (seg.text or '').strip()
    ]

    stats = write_transcript_bundle(ROOT, base, segments, language=getattr(info, 'language', 'zh') or 'zh')
    dt = time.time() - t0
    print(
        f'[done] {base} 耗时{dt/60:.1f}分 '
        f'字数{stats["chars"]} 段数{stats["paragraphs"]} 句数{stats["segments"]}',
        flush=True,
    )


if __name__ == '__main__':
    main()
