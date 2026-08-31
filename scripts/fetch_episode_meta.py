#!/usr/bin/env python3
"""批量提取小宇宙播客页面的标题与音频 URL。"""
import re, json, subprocess, time

urls = [
"https://www.xiaoyuzhoufm.com/episode/6a84e4725aeb2a5712e8f1ac",
"https://www.xiaoyuzhoufm.com/episode/6a8aee6e1352af56ff3aadbb",
"https://www.xiaoyuzhoufm.com/episode/674ea3e18b91f86ee4d44a52",
"https://www.xiaoyuzhoufm.com/episode/6a6b4946b581962ce2be0cdd",
"https://www.xiaoyuzhoufm.com/episode/6a5b8f1aa3fec224d59fa176",
"https://www.xiaoyuzhoufm.com/episode/68ea9a78224325ea70c08f20",
"https://www.xiaoyuzhoufm.com/episode/6a7df54436641f136d87ddbf",
"https://www.xiaoyuzhoufm.com/episode/696f7ac3ef1cf272a7797086",
"https://www.xiaoyuzhoufm.com/episode/6a855e9efb87252df2ec5475",
"https://www.xiaoyuzhoufm.com/episode/6a8c2e39ef65145dfcc49bcd",
]

results = []
for i, u in enumerate(urls):
    html = subprocess.run(
        ['curl', '-sL', '--max-time', '30', '-A',
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36', u],
        capture_output=True, text=True).stdout
    audio = re.search(r'"(https://media\.xyzcdn\.net/[^"]+\.(?:m4a|mp3))"', html)
    title_m = re.search(r'<title>([^<]+?) \| 小宇宙', html)
    title = title_m.group(1).strip() if title_m else '(提取失败)'
    print(f'[{i+1}] {u.split("/")[-1]}')
    print(f'    title: {title}')
    print(f'    audio: {audio.group(1) if audio else "未找到"}')
    results.append({'url': u, 'id': u.split('/')[-1], 'title': title,
                    'audio': audio.group(1) if audio else None})
    time.sleep(2)

with open('/tmp/podcast-meta.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print('\n已保存 /tmp/podcast-meta.json')
