#!/usr/bin/env python3
"""从 143 条话术中精选约 42 条，分 7 大板块，输出 SVG 生成用数据。"""
import json

all_items = json.load(open('/tmp/huashu-all.json', encoding='utf-8'))


def find(source, tech, key=None):
    """按 source + technique(+关键词) 查找条目，返回第一条匹配"""
    for x in all_items:
        if x['source'] != source:
            continue
        if tech and not x['technique_norm'].startswith(tech):
            continue
        if key and key not in x['quote']:
            continue
        return x
    return None


def get(source, tech=None, key=None):
    x = find(source, tech, key)
    if not x:
        print(f'!! 未找到: {source} | {tech} | {key}')
    return x


# 板块设计：每板块一个导语 + 卡片列表
sections = [
    {
        "id": "redefine",
        "title": "一、重新定义：先改概念，再改认知",
        "color": "#2563EB",
        "intro": "话术底层是话语主导权。把对方习惯的概念换成你的定义，争论的坐标系就换了。播客里最高频的句式：不是 X，而是 Y。",
        "cards": [
            get('finding-kindred', '定义重构', '这不是理念，这是账单'),
            get('spacex_history_podcast', '定义重构', '火箭只是过程'),
            get('spacex_history_podcast', '定义重构', '人会后悔'),
            get('good-feelings-together', '定义重构', '紧张'),
            get('why-pay-consumer-vol36', '定义重构', '符号'),
            get('bull-market-desire', '定义重构', '焦躁'),
            get('why-pay-consumer-vol36', '定义重构', '纯消费'),
            get('finding-kindred', '定义重构', '社区不是一群人在看'),
        ],
    },
    {
        "id": "analogy",
        "title": "二、类比说服：用一个熟悉的物，讲一个陌生的理",
        "color": "#059669",
        "intro": "抽象概念没人听得进，找到一个对方有体感的'物'做映射，说服力立刻翻倍。最高频句式：这就像……",
        "cards": [
            get('huajing-s-value', '类比/隐喻论证', '蛋炒饭'),
            get('spacex_history_podcast', '设问引导', '可乐罐'),
            get('spacex_history_podcast', '类比/隐喻论证', '洛杉矶开车'),
            get('bull-market-desire', '类比/隐喻论证', '万有引力'),
            get('supermarket-choice', '类比/隐喻论证', '编辑推荐'),
            get('longterm-outdoor-gear', '类比/隐喻论证', '内衣'),
            get('bull-market-desire', '类比/隐喻论证', '周期蝉'),
            get('travel-camera-spring-guide', '类比/隐喻论证', '学区房鸡娃'),
        ],
    },
    {
        "id": "counterintuitive",
        "title": "三、反常识冲击：先让你意外，再让你记住",
        "color": "#D97706",
        "intro": "与直觉相反的结论自带记忆点。先抛结论制造反差，再补证据。最高频句式：这不叫 X，这叫 Y。",
        "cards": [
            get('finding-kindred', '反常识断言', '不叫克制，这叫浪费'),
            get('distant-goal-first-step', '反常识断言', '所有伟大的事'),
            get('moving-12-times-self-discovery', '反常识断言', '完全是因为无知'),
            get('huajing-s-value', '反常识断言', '销量是跟着产能走的'),
            get('summer-skincare', '反常识断言', 'SPF100'),
            get('nyc-year-pessimist', '反常识断言', '投资是反人性'),
            get('kailash-trekking-guide', '反常识断言', '血氧掉到85以下'),
        ],
    },
    {
        "id": "concrete",
        "title": "四、数字与细节：把宏观翻译成切肤",
        "color": "#7C3AED",
        "intro": "空话靠形容词，说服靠数字。把一个抽象损失折算成对方感同身受的具体数字，说服力立刻上升。",
        "cards": [
            get('japan-price-changes', '具体化锚定', '工资就自动变少了30%'),
            get('distant-goal-first-step', '具体化锚定', '25万字'),
            get('china-consumption-confidence', '具体化锚定', '亏了200万'),
            get('supermarket-choice', '具体化锚定', '使用成本只有50块'),
            get('bull-market-desire', '后果推演', '33万本金'),
            get('summer-skincare', '具体化锚定', '专职司机'),
        ],
    },
    {
        "id": "consequence",
        "title": "五、推演未来：把选择快进到后果",
        "color": "#DC2626",
        "intro": "不争论当下，把选择推演到未来看结果。用损失厌恶驱动行动：你今后一定会掐自己的大腿。",
        "cards": [
            get('finding-kindred', '后果推演', '一百次狼狈'),
            get('summer-skincare', '后果推演', '一熬夜，三十就没了'),
            get('huajing-s-value', '后果推演', '掐自己的大腿'),
            get('nyc-year-pessimist', '后果推演', '零下30度'),
            get('moving-12-times-self-discovery', '后果推演', '没有任何一条路会通向意外'),
            get('japan-price-changes', '因果拆解', '降到2000行吗'),
            get('summer-skincare', '因果拆解', '反应性皮脂分泌'),
            get('china-consumption-confidence', '因果拆解', '消费能力是收入'),
        ],
    },
    {
        "id": "dialogue",
        "title": "六、对话技巧：用问题代替结论",
        "color": "#0891B2",
        "intro": "直接把结论塞给对方会被反驳；用设问、反问、让步让答案从对方嘴里说出来，结论就成了他自己的。",
        "cards": [
            get('china-consumption-confidence', '反问逼思', '你不信这个你信谁'),
            get('nvidia-cosmos-interview', '反问逼思', 'crybaby'),
            get('finding-kindred', '反问逼思', '用户跑了吗'),
            get('bull-market-desire', '设问引导', '贝索斯'),
            get('nyc-year-pessimist', '设问引导', '我未来在哪里花钱'),
            get('supermarket-choice', '设问引导', '真的便宜了'),
            get('friends-third-place', '反问逼思', '现在，你开心了吗'),
            get('bull-market-desire', '先让步再转折', '的确，如果每个人都极致理性'),
        ],
    },
    {
        "id": "credibility",
        "title": "七、可信度经营：示弱、背书与归谬",
        "color": "#475569",
        "intro": "说服不只靠进攻，也靠防守。主动承认局限、引用权威、把对方的方案推到极端，都在经营'你这个人可信'。",
        "cards": [
            get('bull-market-desire', '权威背书', '金德尔伯格'),
            get('neo-labs-capital-wave', '权威背书', '善战者无赫赫之功'),
            get('china-consumption-confidence', '归谬/反例', '给马云也发一笔钱'),
            get('nyc-year-pessimist', '承认局限（示弱增信）', '享受了房地产时代的红利'),
            get('nvidia-cosmos-interview', '承认局限（示弱增信）', '我的解释只有10分'),
            get('huajing-s-value', '承认局限（示弱增信）', '没有做交叉验证'),
            get('neo-labs-capital-wave', '定义重构', '遮蔽布'),
            get('supermarket-choice', '反常识断言', '69.99'),
        ],
    },
]

# 去重 + 统计
seen = set()
total = 0
for s in sections:
    uniq = []
    for c in s['cards']:
        if c is None:
            continue
        if id(c) in seen:
            continue
        seen.add(id(c))
        uniq.append(c)
    s['cards'] = uniq
    total += len(uniq)
    print(f"{s['title'][:22]:24} {len(uniq)} 条")

print('\n总计:', total)
json.dump(sections, open('/tmp/huashu-sections.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
