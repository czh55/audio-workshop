#!/usr/bin/env python3
"""单篇 faster-whisper 转录 worker。

用法: python3 scripts/transcribe_one.py <base> [<cpu_threads>]
- 读取 <base>.m4a
- 流式转录到 <base>.part，完成后原子改名 <base>.txt
- 中断时 .part 保留，不会误判为完成
"""
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    base = sys.argv[1]
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 4
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
    part = ROOT / f'{base}.part'

    if txt.exists() and txt.stat().st_size > 100:
        print(f'[skip] {base} 已存在', flush=True)
        return

    from faster_whisper import WhisperModel
    model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=threads)

    t0 = time.time()
    segments, info = model.transcribe(str(audio), language='zh', beam_size=5)
    part.write_text('', encoding='utf-8')
    chars = 0
    with part.open('a', encoding='utf-8') as f:
        for seg in segments:
            f.write(seg.text)
            f.flush()
            chars += len(seg.text)

    dt = time.time() - t0
    part.replace(txt)
    print(f'[done] {base} 耗时{dt/60:.1f}分 字数{chars}', flush=True)


if __name__ == '__main__':
    main()
