#!/usr/bin/env python3
"""用 tiny 模型转录超长音频（张爱玲 11h）。"""
import sys, time
from pathlib import Path
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
base = sys.argv[1] if len(sys.argv) > 1 else 'zhang_ailing_analysis'
audio = ROOT / f'{base}.m4a'
txt = ROOT / f'{base}.txt'
part = ROOT / f'{base}.part'

if txt.exists() and txt.stat().st_size > 100:
    print(f'[skip] {base} 已存在', flush=True)
    sys.exit(0)

print(f'[start] tiny model {base}', flush=True)
model = WhisperModel('tiny', device='cpu', compute_type='int8', cpu_threads=4)
t0 = time.time()
segments, info = model.transcribe(str(audio), language='zh', beam_size=1)
part.write_text('', encoding='utf-8')
chars = 0
with part.open('a', encoding='utf-8') as f:
    for i, seg in enumerate(segments):
        f.write(seg.text)
        f.flush()
        chars += len(seg.text)
        if i % 200 == 0:
            print(f'  progress: {chars} chars, {time.time()-t0:.0f}s', flush=True)

dt = time.time() - t0
part.replace(txt)
print(f'[done] {base} 耗时{dt/60:.1f}分 字数{chars}', flush=True)
