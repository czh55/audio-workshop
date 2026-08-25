#!/usr/bin/env python3
"""生成转录搜索索引 docs/transcripts-index.json + 复制转录到 docs/transcripts/。

索引条目包含：slug、title、date、author、tags、url、duration、words、file。
转录 txt 会复制到 docs/transcripts/{slug}.txt 供搜索页 fetch。
"""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
OUT_DIR = DOCS / 'transcripts'


def slug_of(filename: str) -> str:
    return filename.replace('-总结.svg', '').replace('.svg', '')


def main() -> None:
    idx = json.load(open(DOCS / 'index.json', encoding='utf-8'))
    by_slug = {}
    for e in idx:
        s = slug_of(e['filename'])
        by_slug[s] = {
            'slug': s,
            'title': e.get('title', ''),
            'date': e.get('date', ''),
            'author': e.get('author', ''),
            'tags': e.get('tags', []),
            'url': e.get('url', ''),
            'duration': e.get('duration', ''),
        }

    OUT_DIR.mkdir(exist_ok=True)
    entries = []
    missing_files = []
    for f in sorted(ROOT.glob('*.txt')):
        if f.name == 'requirements.txt':
            continue
        slug = f.stem
        if slug not in by_slug:
            # 转录但没有 index 条目（如空间站历史），用文件名作为标题
            meta = {
                'slug': slug,
                'title': slug,
                'date': '',
                'author': '',
                'tags': [],
                'url': '',
                'duration': '',
            }
        else:
            meta = by_slug[slug]
        text = f.read_text(encoding='utf-8')
        words = len(text)
        if words < 100:
            continue
        # 复制到 docs/transcripts/
        dest = OUT_DIR / f'{slug}.txt'
        if not dest.exists() or dest.stat().st_size != f.stat().st_size:
            shutil.copy2(f, dest)
        entries.append({
            **meta,
            'words': words,
            'file': f'transcripts/{slug}.txt',
        })
        missing_files.append(slug)

    # 排序：按日期倒序
    entries.sort(key=lambda x: x['date'], reverse=True)

    out = {
        'generated': '2026-08-25',
        'count': len(entries),
        'items': entries,
    }
    (DOCS / 'transcripts-index.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'索引生成完成: {len(entries)} 篇转录')
    print(f'输出: docs/transcripts-index.json ({out["count"]} 条)')


if __name__ == '__main__':
    main()
