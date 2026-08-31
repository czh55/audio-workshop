#!/usr/bin/env python3
"""为 10 篇播客分配 slug 并写入 /tmp/podcast-meta.json。"""
import json

meta = json.load(open('/tmp/podcast-meta.json', encoding='utf-8'))

# id -> slug（≤30 字符，英文/拼音，无空格特殊字符）
SLUGS = {
    '6a84e4725aeb2a5712e8f1ac': 'italian_food_ordering',
    '6a8aee6e1352af56ff3aadbb': 'learning_in_the_cracks',
    '674ea3e18b91f86ee4d44a52': 'japan_travel_food_chain',
    '6a6b4946b581962ce2be0cdd': 'yiwu_small_goods',
    '6a5b8f1aa3fec224d59fa176': 'five_sounds_end_of_world',
    '68ea9a78224325ea70c08f20': 'japan_chinese_restaurants',
    '6a7df54436641f136d87ddbf': 'extreme_weather_future',
    '696f7ac3ef1cf272a7797086': 'zhang_ailing_analysis',
    '6a855e9efb87252df2ec5475': 'europe_filter_cracked',
    '6a8c2e39ef65145dfcc49bcd': 'brand_premium_decline',
}

for m in meta:
    m['slug'] = SLUGS[m['id']]
    print(f"{m['id'][:8]} -> {m['slug']}")

with open('/tmp/podcast-meta.json', 'w', encoding='utf-8') as f:
    json.dump(meta, f, ensure_ascii=False, indent=1)
print('已保存 slug')
