#!/usr/bin/env python3
"""验证转录完整性：检查 90 篇待转录是否都生成了有效 txt。"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MIN_SIZE = 100  # 有效转录至少 100 字节


def main() -> None:
    need = json.load(open('/tmp/transcribe_list.json', encoding='utf-8'))
    done, missing, small = [], [], []
    for slug in need:
        p = ROOT / f'{slug}.txt'
        if not p.exists():
            missing.append(slug)
        elif p.stat().st_size < MIN_SIZE:
            small.append((slug, p.stat().st_size))
        else:
            done.append(slug)

    print(f'共 {len(need)} 篇')
    print(f'已完成: {len(done)}')
    print(f'缺失: {len(missing)}')
    print(f'过小: {len(small)}')
    if missing:
        print('缺失清单:', ' '.join(missing))
    if small:
        print('过小清单:', small)


if __name__ == '__main__':
    main()
