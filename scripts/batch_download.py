#!/usr/bin/env python3
"""批量下载缺失转录的播客音频（限流控速版）。

策略：
1. 逐篇 curl 抓取小宇宙 episode 页面（页面请求间隔 3s，防封）
2. 从 HTML 提取 media.xyzcdn.net 音频 URL
3. CDN 音频下载走 rate-limit.mjs 全局节流器（30s 间隔）
4. 断点续传：已下载完成(>50KB)的跳过

用法：python3 scripts/batch_download.py
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MISSING = '/tmp/missing_list.json'
OUT = ROOT  # 音频存根目录

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
PAGE_INTERVAL = 3.0  # 页面抓取间隔（秒）
MIN_SIZE = 50 * 1024  # 最小有效音频大小


def fetch_page(url: str) -> str:
    req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode('utf-8', 'ignore')


def extract_audio(html: str) -> str | None:
    m = re.findall(r'https://media\.xyzcdn\.net/[^"\'\s]+\.(?:m4a|mp3)', html)
    return m[0] if m else None


def rate_limit() -> None:
    """调用 rate-limit.mjs 全局节流器（30s）"""
    subprocess.run(
        ['node', str(ROOT / 'rate-limit.mjs')],
        cwd=str(ROOT), check=True, capture_output=True, text=True,
    )


def main() -> None:
    missing = json.load(open(MISSING, encoding='utf-8'))
    print(f'共 {len(missing)} 篇待下载', flush=True)

    # 提取音频 URL 阶段（页面请求，3s 间隔）
    todo = []
    for i, m in enumerate(missing):
        slug = m['slug']
        out_file = OUT / f'{slug}.m4a'
        if out_file.exists() and out_file.stat().st_size > MIN_SIZE:
            print(f'[skip] {slug} 已存在', flush=True)
            continue

        try:
            html = fetch_page(m['url'])
            audio_url = extract_audio(html)
            if not audio_url:
                print(f'[no-audio] {slug} 页面无音频链接', flush=True)
                continue
            todo.append({'slug': slug, 'audio_url': audio_url})
            print(f'[url] {i + 1}/{len(missing)} {slug}', flush=True)
        except Exception as e:
            print(f'[err] {slug} 页面抓取失败: {e}', flush=True)
        time.sleep(PAGE_INTERVAL)

    print(f'\n提取到 {len(todo)} 个音频 URL，开始下载（30s 限流）...', flush=True)

    # 下载阶段（CDN 请求走 rate-limit.mjs）
    success, failed = 0, []
    for i, t in enumerate(todo):
        slug = t['slug']
        out_file = OUT / f'{slug}.m4a'
        if out_file.exists() and out_file.stat().st_size > MIN_SIZE:
            print(f'[skip] {slug} 已下载', flush=True)
            success += 1
            continue

        # 限流后再下载
        try:
            rate_limit()
            print(f'[dl] {i + 1}/{len(todo)} {slug} ...', flush=True)
            subprocess.run(
                ['curl', '-L', '-s', '-o', str(out_file), t['audio_url'], '--max-time', '600'],
                check=True, timeout=620,
            )
            size = out_file.stat().st_size if out_file.exists() else 0
            if size > MIN_SIZE:
                success += 1
                print(f'[ok] {slug} {size // 1024}KB', flush=True)
            else:
                out_file.unlink(missing_ok=True)
                failed.append((slug, '文件过小'))
                print(f'[fail] {slug} 文件过小', flush=True)
        except Exception as e:
            failed.append((slug, str(e)[:100]))
            print(f'[fail] {slug} {e}', flush=True)

    print(f'\n完成：成功 {success}，失败 {len(failed)}', flush=True)
    for slug, err in failed:
        print(f'  {slug}: {err}', flush=True)


if __name__ == '__main__':
    main()
