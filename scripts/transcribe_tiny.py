#!/usr/bin/env python3
"""用 tiny 模型转录超长音频（如张爱玲 11h）。

用法: python3 scripts/transcribe_tiny.py <base> [--force]

产出与 transcribe_one.py 相同：txt / srt / vtt / json。
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
    base = args[0] if args else 'zhang_ailing_analysis'

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

    print(f'[start] tiny model {base}', flush=True)
    try:
        model = WhisperModel('tiny', device='cpu', compute_type='int8', cpu_threads=4)
    except Exception as exc:
        print(f'[warn] tiny 不可用（{exc.__class__.__name__}），回退 small', flush=True)
        model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=4)
    t0 = time.time()
    raw_segments, info = model.transcribe(
        str(audio),
        language='zh',
        beam_size=1,
        vad_filter=True,
        initial_prompt=INITIAL_PROMPT,
    )

    segments: list[Segment] = []
    chars = 0
    for i, seg in enumerate(raw_segments):
        text = (seg.text or '').strip()
        if not text:
            continue
        segments.append(Segment(float(seg.start), float(seg.end), text))
        chars += len(text)
        if i % 200 == 0 and i:
            print(f'  progress: {chars} chars, {time.time()-t0:.0f}s', flush=True)

    stats = write_transcript_bundle(ROOT, base, segments, language=getattr(info, 'language', 'zh') or 'zh')
    dt = time.time() - t0
    print(
        f'[done] {base} 耗时{dt/60:.1f}分 '
        f'字数{stats["chars"]} 段数{stats["paragraphs"]} 句数{stats["segments"]}',
        flush=True,
    )


if __name__ == '__main__':
    main()
