#!/usr/bin/env python3
"""批量下载小宇宙音频：每次 curl 前执行 rate-limit.mjs（30s 限流），失败重试 ≤3 次。"""
import json, subprocess, time, sys, os

ROOT = '/Users/chenzhiheng/Projects/audio-workshop'
meta = json.load(open('/tmp/podcast-meta.json', encoding='utf-8'))

def rate_limit():
    subprocess.run(['node', 'rate-limit.mjs'], cwd=ROOT, check=True)

def download(m):
    slug = m['slug']
    out = os.path.join(ROOT, f'{slug}.m4a')
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        print(f'[skip] {slug} 已存在')
        return True
    for attempt in range(1, 4):
        rate_limit()
        print(f'[dl {attempt}/3] {slug} ...', flush=True)
        r = subprocess.run(
            ['curl', '-sL', '-o', out, '--max-time', '600',
             '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
             '--progress-bar', m['audio']],
            capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out) and os.path.getsize(out) > 100000:
            print(f'[ok] {slug} {os.path.getsize(out)/1e6:.1f}MB', flush=True)
            return True
        print(f'[fail] {slug} 尝试{attempt}失败', flush=True)
        if os.path.exists(out):
            os.remove(out)
    return False

failed = []
for m in meta:
    if not download(m):
        failed.append(m['slug'])

print('\n完成。失败:', failed if failed else '无')
sys.exit(1 if failed else 0)
