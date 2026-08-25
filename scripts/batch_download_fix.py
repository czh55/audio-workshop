#!/usr/bin/env python3
"""补下载脚本：只处理无音频链接或下载失败的篇目（兼容 m4a/mp3）。"""
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
MIN_SIZE = 50 * 1024


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'ignore')


def extract_audio(html: str):
    m = re.findall(r'https://media\.xyzcdn\.net/[^"\'\s]+\.(?:m4a|mp3)', html)
    return m[0] if m else None


def rate_limit() -> None:
    subprocess.run(['node', str(ROOT / 'rate-limit.mjs')], cwd=str(ROOT),
                   check=True, capture_output=True, text=True)


def main() -> None:
    missing = json.load(open('/tmp/missing_list.json', encoding='utf-8'))
    todo = []
    for m in missing:
        slug = m['slug']
        out_file = ROOT / f'{slug}.m4a'
        if out_file.exists() and out_file.stat().st_size > MIN_SIZE:
            continue
        try:
            html = fetch_page(m['url'])
            audio_url = extract_audio(html)
            if audio_url:
                ext = '.mp3' if audio_url.endswith('.mp3') else '.m4a'
                todo.append({'slug': slug, 'audio_url': audio_url, 'out': ROOT / f'{slug}{ext}'})
                print(f'[url] {slug} -> {ext}', flush=True)
            else:
                print(f'[no-audio] {slug}', flush=True)
        except Exception as e:
            print(f'[err] {slug}: {e}', flush=True)
        time.sleep(3)

    print(f'\n待补下载 {len(todo)} 篇', flush=True)
    for i, t in enumerate(todo):
        if t['out'].exists() and t['out'].stat().st_size > MIN_SIZE:
            print(f'[skip] {t["slug"]} 已存在', flush=True)
            continue
        try:
            rate_limit()
            print(f'[dl] {i + 1}/{len(todo)} {t["slug"]} ...', flush=True)
            subprocess.run(['curl', '-L', '-s', '-o', str(t['out']), t['audio_url'], '--max-time', '600'],
                           check=True, timeout=620)
            size = t['out'].stat().st_size if t['out'].exists() else 0
            print(f'[ok] {t["slug"]} {size // 1024}KB' if size > MIN_SIZE else f'[fail] {t["slug"]} 文件过小', flush=True)
        except Exception as e:
            print(f'[fail] {t["slug"]}: {e}', flush=True)

    print('补下载完成', flush=True)


if __name__ == '__main__':
    main()
