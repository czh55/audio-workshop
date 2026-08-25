#!/usr/bin/env python3
"""从 286 条话术中精选约 66 条，归一化到 7 大板块，输出 HTML 生成用数据。

分类映射：
- redefine 重新定义: 定义重构, 概念重构, 概念区分, 概念框架, 认知反转, 视角转换...
- analogy 类比说服: 类比说服, 类比论证, 类比降槛, 归谬类比, 类比重构, 比喻反转...
- counterintuitive 反常识冲击: 反常识论证, 反常识断言, 反常理断言, 认知纠偏, 金句定调, 拆穿心理...
- concrete 数字与细节: 数据冲击, 数据对比, 数据论证, 细节具象...
- consequence 推演未来: 后果推演, 因果推演, 情景推演, 利益诱导...
- dialogue 对话技巧: 设问引导, 设问索取, 反问归谬, 换位思考, 共情示范...
- credibility 可信度经营: 权威引证, 规律引用, 社会认同, 坦诚说服, 示弱...
"""
import json
import sys

items = json.load(open('/tmp/huashu-all.json', encoding='utf-8'))

CATEGORY_KEYWORDS = {
    'redefine': ['定义重构', '概念重构', '概念区分', '概念框架', '重新定义', '认知反转',
                 '视角转换', '观点重构', '命名重构', '概念揭示', '概念辨析', '身份共鸣',
                 '定义', '重构', '金句重构', '规律提炼', '认知'],
    'analogy': ['类比说服', '类比论证', '类比降槛', '归谬类比', '类比重构', '比喻反转',
                '类比戳破', '类比', '隐喻', '比喻', '通感'],
    'counterintuitive': ['反常识论证', '反常识断言', '反常理断言', '反直觉', '认知纠偏',
                         '拆穿心理', '金句定调', '金句断言', '金句', '逆向论证', '反常识',
                         '悖论揭露', '悖论', '证伪论证', '认知颠覆', '反例', '对比论证',
                         '对比', '对照实验', '象征解读'],
    'concrete': ['数据冲击', '数据对比', '数据论证', '数据', '细节', '具象', '算账', '数字'],
    'consequence': ['后果推演', '因果推演', '情景推演', '推演', '利益诱导', '后果', '连锁推演',
                    '前景', '愿景渲染', '格局上升', '拆解归因', '深层归因', '动机揭示',
                    '拆解目标', '拆解', '分层论证', '普遍化论证', '边界论证', '规律排除', '决策框架'],
    'dialogue': ['设问引导', '设问索取', '设问取证', '反问归谬', '反问', '设问', '提问',
                 '换位思考', '共情示范', '共情', '对话', '我懂', '体验', '心理战术',
                 '情景测试', '点破不对等', '先小人后君子', '痛点拆解'],
    'credibility': ['权威引证', '权威背书', '规律引用', '社会认同', '坦诚说服', '示弱',
                    '背书', '卸责示好', '借力打力', '借力', '对等推理', '引用格言', '故事',
                    '历史', '归谬法', '归谬', '机制解释', '经验总结'],
}


def classify(item):
    tech = item.get('technique', '')
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in tech for k in kws):
            return cat
    return 'other'


# 给每条打上分类
for item in items:
    item['_cat'] = classify(item)

from collections import Counter
print('分类分布:', dict(Counter(i['_cat'] for i in items)))


def pick(items, cat, limit):
    """按 quote 长度合理、content 完整度挑选"""
    cand = [i for i in items if i['_cat'] == cat]
    # 排序：quote 在 60-180 字之间优先，技术名简单优先
    def score(i):
        qlen = len(i['quote'])
        if 60 <= qlen <= 180:
            return 0
        return abs(qlen - 120) // 10
    cand.sort(key=score)
    # 去重：同一 source 最多保留 3 条
    from collections import defaultdict
    per_source = defaultdict(list)
    for i in cand:
        per_source[i['source']].append(i)
    picked = []
    for src, lst in per_source.items():
        lst.sort(key=score)
        picked.extend(lst[:3])
    picked.sort(key=score)
    return picked[:limit]


SECTIONS = [
    {"id": "redefine", "title": "一、重新定义：先改概念，再改认知",
     "color": "#2563EB",
     "intro": "话术底层是话语主导权。把对方习惯的概念换成你的定义，争论的坐标系就换了。播客里最高频的句式：不是 X，而是 Y。",
     "limit": 11},
    {"id": "analogy", "title": "二、类比说服：用一个熟悉的物，讲一个陌生的理",
     "color": "#059669",
     "intro": "抽象概念没人听得进，找到一个对方有体感的'物'做映射，说服力立刻翻倍。最高频句式：这就像……",
     "limit": 11},
    {"id": "counterintuitive", "title": "三、反常识冲击：先让你意外，再让你记住",
     "color": "#D97706",
     "intro": "人们记住的不是道理，而是'居然是这样'的瞬间。把常识倒过来，听众才会停下来重新想。",
     "limit": 9},
    {"id": "concrete", "title": "四、数字与细节：把宏观翻译成切肤",
     "color": "#7C3AED",
     "intro": "'很大'没人有感觉，'具体到几'人才会疼。把抽象的规模翻译成可感受的细节，是播客里最强的认知武器。",
     "limit": 9},
    {"id": "consequence", "title": "五、推演未来：把选择快进到后果",
     "color": "#DC2626",
     "intro": "让对方看到现在的选择在三五年后长什么样，说服就不再需要争辩。最高频句式：如果你现在……三年后……",
     "limit": 9},
    {"id": "dialogue", "title": "六、对话技巧：用问题代替结论",
     "color": "#0891B2",
     "intro": "结论是别人塞给你的，问题是自己长出来的。用提问代替论断，让对方自己得出结论，说服效果最持久。",
     "limit": 9},
    {"id": "credibility", "title": "七、可信度经营：示弱、背书与归谬",
     "color": "#475569",
     "intro": "最有说服力的不是最强势的，而是最可信的。适度示弱、借权威背书、用对方逻辑归谬，都是经营可信度的经典路数。",
     "limit": 8},
]

result = []
for sec in SECTIONS:
    picked = pick(items, sec['id'], sec['limit'])
    result.append({'section': sec, 'cards': picked})
    print(f"{sec['title'][:10]}: 选中 {len(picked)} 条")

json.dump({'sections': result}, open('/tmp/huashu-sections.json', 'w'),
          ensure_ascii=False, indent=1)
print('\n已保存 /tmp/huashu-sections.json')
