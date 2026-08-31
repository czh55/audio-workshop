#!/usr/bin/env python3
"""把 values-all.json 的素材映射到 7 大认知维度板块，输出分类预览。"""
import json

items = json.load(open('/tmp/values-all.json', encoding='utf-8'))

# index -> category 手工映射（基于对全部素材的浏览）
# 7 大板块：work 工作与事业 / money 金钱与消费 / tech 科技与AI
#           growth 自我与成长 / life 消费与生活方式 / travel 旅行与摄影户外
#           society 社会与人性
M = {
    # --- work 工作与事业 ---
    35: 'work', 39: 'work', 90: 'work', 91: 'work', 116: 'work', 123: 'work',
    142: 'work', 143: 'work', 167: 'work', 172: 'work', 173: 'work', 190: 'work',
    193: 'work', 194: 'work', 199: 'work', 200: 'work',
    # --- money 金钱与消费 ---
    0: 'money', 17: 'money', 18: 'money', 20: 'money', 25: 'money', 26: 'money',
    29: 'money', 32: 'money', 33: 'money', 34: 'money', 50: 'money', 81: 'money',
    82: 'money', 110: 'money', 115: 'money', 124: 'money', 127: 'money', 128: 'money',
    139: 'money', 144: 'money', 145: 'money', 157: 'money', 158: 'money', 177: 'money', 178: 'money',
    # --- tech 科技与AI ---
    9: 'tech', 10: 'tech', 41: 'tech', 76: 'tech', 77: 'tech', 105: 'tech', 106: 'tech',
    117: 'tech', 118: 'tech', 121: 'tech', 122: 'tech', 125: 'tech', 133: 'tech', 134: 'tech',
    151: 'tech', 182: 'tech', 187: 'tech', 188: 'tech', 189: 'tech', 195: 'tech', 196: 'tech',
    197: 'tech', 198: 'tech',
    # --- growth 自我与成长 ---
    7: 'growth', 8: 'growth', 15: 'growth', 21: 'growth', 22: 'growth', 23: 'growth',
    36: 'growth', 37: 'growth', 38: 'growth', 40: 'growth', 56: 'growth', 61: 'growth',
    62: 'growth', 65: 'growth', 66: 'growth', 87: 'growth', 88: 'growth', 92: 'growth',
    93: 'growth', 94: 'growth', 95: 'growth', 120: 'growth', 135: 'growth', 136: 'growth',
    137: 'growth', 164: 'growth', 165: 'growth', 166: 'growth', 170: 'growth', 180: 'growth',
    183: 'growth', 184: 'growth', 191: 'growth', 192: 'growth',
    # --- life 消费与生活方式 ---
    1: 'life', 2: 'life', 14: 'life', 24: 'life', 27: 'life', 30: 'life', 31: 'life',
    45: 'life', 48: 'life', 49: 'life', 67: 'life', 78: 'life', 79: 'life', 80: 'life',
    96: 'life', 97: 'life', 98: 'life', 100: 'life', 103: 'life', 104: 'life', 107: 'life',
    108: 'life', 109: 'life', 112: 'life', 119: 'life', 140: 'life', 141: 'life', 146: 'life',
    147: 'life', 148: 'life', 149: 'life', 150: 'life', 154: 'life', 168: 'life', 169: 'life',
    181: 'life', 201: 'life',
    # --- travel 旅行与摄影户外 ---
    3: 'travel', 4: 'travel', 6: 'travel', 42: 'travel', 43: 'travel', 44: 'travel',
    46: 'travel', 47: 'travel', 68: 'travel', 69: 'travel', 70: 'travel', 71: 'travel',
    72: 'travel', 73: 'travel', 101: 'travel', 102: 'travel', 113: 'travel', 114: 'travel',
    131: 'travel', 132: 'travel', 155: 'travel', 156: 'travel', 161: 'travel', 162: 'travel',
    163: 'travel', 174: 'travel',
    # --- society 社会与人性 ---
    5: 'society', 11: 'society', 12: 'society', 13: 'society', 19: 'society', 28: 'society',
    51: 'society', 52: 'society', 53: 'society', 54: 'society', 55: 'society', 58: 'society',
    59: 'society', 60: 'society', 63: 'society', 64: 'society', 83: 'society', 84: 'society',
    85: 'society', 86: 'society', 89: 'society', 99: 'society', 126: 'society', 129: 'society',
    130: 'society', 159: 'society', 160: 'society', 171: 'society', 175: 'society', 176: 'society',
    179: 'society', 185: 'society', 186: 'society',
}

unmapped = [i for i in range(len(items)) if i not in M]
print('未映射:', [(i, items[i]['source']) for i in unmapped])

from collections import Counter, defaultdict
cats = Counter(M.values())
print('分类分布:', dict(cats))

groups = defaultdict(list)
for i, cat in M.items():
    groups[cat].append(i)

for cat, ids in groups.items():
    print(f'\n===== {cat} ({len(ids)}条) =====')
    for i in ids:
        x = items[i]
        print(f"[{i:03d}] {x['source'][:14]:14s} | {x['angle'][:52]}")

# 保存映射供精选使用
json.dump({str(k): v for k, v in M.items()}, open('/tmp/values-map.json', 'w'))
