#!/usr/bin/env python3
"""从 158 条氛围控制素材中精选约 60 条，归一化到 7 大板块，输出 HTML 生成用数据。

分类映射（谈话氛围控制专题）：
- self-mock 自嘲救场: 自嘲*, 接受批评, 主动认错, 坦诚道歉, 道歉示弱, 敏感化解...
- soften 示弱拉近: 示弱*, 主动示弱, 自曝拉近, 打破人设, 真实流露, 回忆拉近, 共情自曝...
- humor 幽默缓冲: 幽默*, 调侃*, 玩梗, 接梗, 玩笑*, 谐音...
- safety 安全铺垫: 安全铺垫, 试探设防, 预防缓冲, 冒犯预警, 边界声明, 措辞管理, 认同前置, 开场暖场, 共情铺垫, 共情预热...
- empathy 共情倾听: 共情*, 宽慰托底, 即时肯定, 即时喝彩, 夸奖*, 接话捧场, 软性批评...
- rhythm 节奏转场: 话题转场, 情绪转场, 猜谜转场, 节奏*, 情绪止损, 情绪降温, 收尾*, 提问互动, 通俗转译, 故事破冰, 共识软化, 比喻复述, 圆场转场...
- lift 托举救场: 托举抬价, 总结升华, 递话筒, 轻放沉重, 反抛话筒, 反抛平等...
"""
import json
from collections import Counter

items = json.load(open('/tmp/atmosphere-all.json', encoding='utf-8'))

CATEGORY_KEYWORDS = {
    'self-mock': ['自嘲', '接受批评', '主动认错', '坦诚道歉', '道歉示弱', '敏感化解'],
    'soften': ['示弱', '自曝拉近', '打破人设', '真实流露', '回忆拉近', '共情自曝', '亲近拉近'],
    'humor': ['幽默', '调侃', '玩梗', '接梗', '玩笑', '谐音', '互怼', '捧哏', '夸张', '夸赞缓冲'],
    'safety': ['安全铺垫', '试探设防', '预防缓冲', '冒犯预警', '边界声明', '措辞管理',
               '认同前置', '开场暖场', '共情铺垫', '共情预热'],
    'empathy': ['共情', '宽慰托底', '即时肯定', '即时喝彩', '夸奖', '捧场', '软性批评', '惊讶接话'],
    'rhythm': ['转场', '节奏', '情绪止损', '情绪降温', '收尾', '提问互动', '通俗转译',
               '故事破冰', '共识软化', '比喻复述', '圆场', '冲突缓和'],
    'lift': ['托举', '总结升华', '递话筒', '轻放沉重', '反抛'],
}


def classify(item):
    tech = item.get('technique', '')
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in tech for k in kws):
            return cat
    return 'other'


for item in items:
    item['_cat'] = classify(item)

print('分类分布:', dict(Counter(i['_cat'] for i in items)))


def pick(items, cat, limit):
    cand = [i for i in items if i['_cat'] == cat]
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
    {"id": "self-mock", "title": "一、自嘲救场：把自己放低，把尴尬化解",
     "color": "#2563EB",
     "intro": "氛围尴尬时最快的解药是自嘲——主动把自己放低，对方的攻击和尴尬瞬间失去着力点。主播们靠这个化解翻车、批评与冷场。",
     "limit": 10},
    {"id": "soften", "title": "二、示弱拉近：暴露真实，让距离变近",
     "color": "#059669",
     "intro": "权威和完美让人敬而远之，真实的脆弱才让人靠近。主动暴露自己的不懂、后悔与局限，是把对话从'表演'切换成'交心'的开关。",
     "limit": 9},
    {"id": "humor", "title": "三、幽默缓冲：用玩笑把尖锐软化",
     "color": "#D97706",
     "intro": "再严肃的碰撞，一个恰到好处的玩笑就能让火药味散掉。幽默不是逃避问题，而是给对话留出'可以轻松一点'的余裕。",
     "limit": 9},
    {"id": "safety", "title": "四、安全铺垫：先铺安全网，让对方敢开口",
     "color": "#7C3AED",
     "intro": "对方不肯说真话，往往不是不想说，而是觉得不安全。先给免责声明、先划安全边界、先示好，后面的话才听得进去。",
     "limit": 9},
    {"id": "empathy", "title": "五、共情倾听：让对方感到被理解",
     "color": "#DC2626",
     "intro": "很多对话失败是因为双方都在说话没人倾听。即时肯定、接住情绪、把对方的话复述出来——被理解的感觉本身就是最好的沟通润滑剂。",
     "limit": 9},
    {"id": "rhythm", "title": "六、节奏转场：控制走向，接住情绪",
     "color": "#0891B2",
     "intro": "高手不只接话，还控制对话的节奏：该停的时候停、该转的时候转、该收的时候收。话题的切换与情绪的刹车，都是氛围控制的硬功夫。",
     "limit": 8},
    {"id": "lift", "title": "七、托举救场：把对方抬高，让对话发光",
     "color": "#475569",
     "intro": "最好的控场不是自己出彩，而是让对方出彩。托举、递话筒、总结升华，让每个人在对话里都被看见，氛围自然就好了。",
     "limit": 7},
]

result = []
for sec in SECTIONS:
    picked = pick(items, sec['id'], sec['limit'])
    result.append({'section': sec, 'cards': picked})
    print(f"{sec['title'][:10]}: 选中 {len(picked)} 条")

json.dump({'sections': result}, open('/tmp/atmosphere-sections.json', 'w'),
          ensure_ascii=False, indent=1)
print('\n已保存 /tmp/atmosphere-sections.json')
