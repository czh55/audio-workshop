#!/usr/bin/env python3
"""补充映射 + 精选 68 条素材成 7 大板块，输出 HTML 生成用 JSON。"""
import json

items = json.load(open('/tmp/values-all.json', encoding='utf-8'))
M = json.load(open('/tmp/values-map.json'))

# 补充之前未映射的素材
EXTRA = {
    '16': 'growth', '57': 'travel', '74': 'society', '75': 'society',
    '111': 'tech', '138': 'growth', '152': 'growth', '153': 'life',
}
M.update(EXTRA)

# 每个板块的精选 index（人工挑选：独特、有洞察、覆盖多节目）
PICKS = {
    'work': [35, 39, 90, 123, 142, 167, 172, 190, 200],
    'money': [0, 17, 20, 29, 32, 50, 115, 124, 127, 139, 144],
    'tech': [9, 189, 105, 182, 121, 125, 151, 195, 197, 76],
    'growth': [7, 15, 23, 36, 56, 65, 87, 92, 137, 152, 183],
    'life': [1, 14, 27, 45, 48, 67, 79, 140, 154],
    'travel': [3, 42, 47, 68, 71, 113, 131, 174],
    'society': [5, 11, 12, 13, 19, 52, 54, 63, 84, 99],
}

SECTIONS = [
    {"id": "work", "title": "一、工作与事业：把上班这件事想清楚",
     "color": "#2563EB",
     "intro": "从'工作到底为了什么'到'要不要辞职去创业'，主播们给出一套和主流完全不同的工作观：工作不该是时间的默认大头，为自己工作反而更不自由，而判断一份职业适不适合，取决于你能不能接受同学三年后当你的领导。"},
    {"id": "money", "title": "二、金钱与消费：戳破钱的错觉",
     "color": "#059669",
     "intro": "欲望大多不是发自内心而是模仿来的，真正驱动人的是优越感而非富足。主播们戳破'没有中间商''电车省钱''金奖认证'等消费神话，也提醒：把资产决策偷换成消费决策，是最隐蔽的收割方式。"},
    {"id": "tech", "title": "三、科技与AI：AI时代的清醒判断",
     "color": "#7C3AED",
     "intro": "当所有人都在追捧AI时，这些主播给出反共识的判断：AI最先攻克的恰是理性工作，模糊的感性判断才是人的护城河；模型能力终会收敛，胜负在生态整合；真正不可替代的，是必须到场、依赖人际接触的手艺。"},
    {"id": "growth", "title": "四、自我与成长：换一种活法看自己",
     "color": "#D97706",
     "intro": "内耗未必需要被根治，狼狈是一种被激活的生命感受，'我不配'的惶恐反而让人保持饥饿。主播们反对'先找到热爱再行动'，主张先做起来再爱上；认为人生真正该问的不是'有没有意义'，而是'五年后你还想不想重过它'。"},
    {"id": "life", "title": "五、消费与生活方式：生活里的独特品味",
     "color": "#DB2777",
     "intro": "真实的第三空间恰恰在于不完美，'外油内干'不是缺水而是屏障求救，糖的直觉定义是错的。从便利店到实体唱片，主播们用独特的生活观察，拆解我们习以为常却未必真懂的日常。"},
    {"id": "travel", "title": "六、旅行与摄影：在路上看见真实",
     "color": "#0891B2",
     "intro": "摄影不该迷信决定性瞬间，镜头一握就是叙事权；旅行不必追求打卡完美，意外和疲惫才是记忆最深的部分。主播们反对没苦硬吃，也戳穿旅游经济里背夫交钱修路却让自己失业的悖论。"},
    {"id": "society", "title": "七、社会与人性：看穿世界的运行规则",
     "color": "#DC2626",
     "intro": "战争在停火那一刻并没有结束，旁观偷拍性侵同样是帮凶，'亲眼看过'必须用脚走到。从国家性格到人际关系，主播们用锋利的社会观察，揭示表层规则之下的真实运行逻辑。"},
]

result = []
all_picked = []
for sec in SECTIONS:
    cards = [items[i] for i in PICKS[sec['id']]]
    all_picked.extend(PICKS[sec['id']])
    result.append({'section': sec, 'cards': cards})
    print(f"{sec['title'][:10]}: {len(cards)} 条")

print('总计:', len(all_picked))
print('覆盖节目:', len(set(items[i]['source'] for i in all_picked)))

json.dump({'sections': result}, open('/tmp/values-sections.json', 'w'),
          ensure_ascii=False, indent=1)
print('已保存 /tmp/values-sections.json')
