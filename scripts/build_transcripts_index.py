#!/usr/bin/env python3
"""生成转录搜索索引 docs/transcripts-index.json + 复制转录到 docs/transcripts/。

索引条目包含：slug、title、date、author、tags、url、duration、words、file。
转录 txt/srt/vtt/json 会复制到 docs/transcripts/ 供搜索页与阅读页使用。
"""
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
OUT_DIR = DOCS / 'transcripts'
ARTIFACTS = ('.txt', '.srt', '.vtt', '.json')


def slug_of(filename: str) -> str:
    return filename.replace('-总结.svg', '').replace('.svg', '')


def word_count(text: str) -> int:
    """统计正文字数，忽略时间戳行。"""
    lines = []
    for line in text.splitlines():
        if re.match(r'^\[\d{2}:\d{2}', line.strip()):
            continue
        lines.append(line)
    body = '\n'.join(lines)
    return len(re.sub(r'\s+', '', body))


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
    for f in sorted(ROOT.glob('*.txt')):
        if f.name == 'requirements.txt':
            continue
        slug = f.stem
        if slug not in by_slug:
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
        words = word_count(text)
        if words < 100:
            continue

        for ext in ARTIFACTS:
            src = ROOT / f'{slug}{ext}'
            if src.exists():
                dest = OUT_DIR / f'{slug}{ext}'
                if not dest.exists() or dest.stat().st_size != src.stat().st_size:
                    shutil.copy2(src, dest)

        entries.append({
            **meta,
            'words': words,
            'file': f'transcripts/{slug}.txt',
        })

    entries.sort(key=lambda x: x['date'], reverse=True)

    from datetime import date
    out = {
        'generated': date.today().isoformat(),
        'count': len(entries),
        'items': entries,
    }
    (DOCS / 'transcripts-index.json').write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'索引生成完成: {len(entries)} 篇转录')
    print(f'输出: docs/transcripts-index.json ({out["count"]} 条)')


if __name__ == '__main__':
    main()
