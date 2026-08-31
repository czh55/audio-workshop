#!/usr/bin/env python3
"""单篇 faster-whisper 转录 worker。

用法: python3 scripts/transcribe_one.py <base> [<cpu_threads>] [--force]
- 读取 <base>.m4a / .mp3
- 流式转录到 <base>.part，完成后原子改名 <base>.txt
- 每个语音片段单独成行；停顿 >1.2s 插入空行分段
- 中断时 .part 保留，不会误判为完成
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 停顿超过该秒数则插入段落空行
PAUSE_BREAK_SEC = 1.2
INITIAL_PROMPT = "以下是普通话的句子。"


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
    part = ROOT / f'{base}.part'

    if not force and txt.exists() and txt.stat().st_size > 100:
        print(f'[skip] {base} 已存在（加 --force 可重跑）', flush=True)
        return

    from faster_whisper import WhisperModel
    model = WhisperModel('small', device='cpu', compute_type='int8', cpu_threads=threads)

    t0 = time.time()
    segments, info = model.transcribe(
        str(audio),
        language='zh',
        beam_size=5,
        vad_filter=True,
        initial_prompt=INITIAL_PROMPT,
    )
    part.write_text('', encoding='utf-8')
    chars = 0
    lines = 0
    paragraphs = 1
    prev_end = None
    with part.open('a', encoding='utf-8') as f:
        for seg in segments:
            text = (seg.text or '').strip()
            if not text:
                continue
            if prev_end is not None:
                gap = seg.start - prev_end
                if gap >= PAUSE_BREAK_SEC:
                    f.write('\n\n')
                    paragraphs += 1
                else:
                    f.write('\n')
            f.write(text)
            f.flush()
            chars += len(text)
            lines += 1
            prev_end = seg.end
        if lines:
            f.write('\n')

    dt = time.time() - t0
    part.replace(txt)
    print(
        f'[done] {base} 耗时{dt/60:.1f}分 字数{chars} 行数{lines} 段数{paragraphs}',
        flush=True,
    )


if __name__ == '__main__':
    main()
