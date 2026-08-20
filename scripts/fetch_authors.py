#!/usr/bin/env python3
"""从 小宇宙 SSR 页面批量抓取每集的播客名，输出 slug -> author 映射。"""
import json
import re
import time
import urllib.request

INDEX = 'docs/index.json'
OUT = 'docs/author-map.json'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'


def fetch_title(url: str) -> str | None:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as r:
        html = r.read().decode('utf-8', 'ignore')
    m = re.search(r'<title[^>]*>(.*?)</title>', html, re.S)
    return m.group(1).strip() if m else None


def parse_author(raw_title: str) -> tuple[str, str]:
    main = raw_title.split(' | ')[0] if ' | ' in raw_title else raw_title
    parts = main.rsplit(' - ', 1)
    ep_title = parts[0].strip()
    pod_name = parts[-1].strip() if len(parts) > 1 else ''
    return ep_title, pod_name


def slug_of(entry) -> str:
    return entry['filename'].replace('-总结.svg', '').replace('.svg', '')


def main() -> None:
    idx = json.load(open(INDEX, encoding='utf-8'))
    try:
        existing = json.load(open(OUT, encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        existing = {}

    todo = [e for e in idx if slug_of(e) not in existing]
    print(f'共 {len(idx)} 篇，已有 {len(existing)} 篇，需抓取 {len(todo)} 篇')

    failures = []
    for i, entry in enumerate(todo):
        slug = slug_of(entry)
        try:
            raw = fetch_title(entry['url'])
            if not raw:
                raise ValueError('no <title>')
            ep_title, author = parse_author(raw)
            if not author:
                raise ValueError(f'no author in: {raw[:80]}')
            existing[slug] = {'author': author, 'title': ep_title, 'url': entry['url']}
            print(f"[{i + 1}/{len(todo)}] {slug} => {author}")
        except Exception as ex:
            failures.append((slug, str(ex)))
            print(f"[{i + 1}/{len(todo)}] {slug} FAILED: {ex}")
        time.sleep(0.5)

    json.dump(existing, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(f'\n完成，成功 {len(existing)} 篇，失败 {len(failures)} 篇')
    for slug, err in failures:
        print(f'  {slug}: {err}')


if __name__ == '__main__':
    main()
