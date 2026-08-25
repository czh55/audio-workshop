#!/usr/bin/env python3
"""从 /tmp/huashu-sections.json 生成说服话术 HTML 专题。
输出: docs/说服话术-从播客中学到的表达武器.html
"""
import json
import html

data = json.load(open('/tmp/huashu-sections.json', encoding='utf-8'))
sections = data['sections']

TOTAL_CARDS = sum(len(s['cards']) for s in sections)
PODCASTS = len(set(c['source_name'] for s in sections for c in s['cards']))

# 现有标签页用于配色（保持与之前一致）
COLORS = {
    '#2563EB': {'badge': '#eff6ff', 'text': '#1e40af', 'border': '#bfdbfe'},
    '#059669': {'badge': '#ecfdf5', 'text': '#065f46', 'border': '#a7f3d0'},
    '#D97706': {'badge': '#fffbeb', 'text': '#92400e', 'border': '#fde68a'},
    '#7C3AED': {'badge': '#f5f3ff', 'text': '#5b21b6', 'border': '#ddd6fe'},
    '#DC2626': {'badge': '#fef2f2', 'text': '#991b1b', 'border': '#fecaca'},
    '#0891B2': {'badge': '#ecfeff', 'text': '#155e75', 'border': '#a5f3fc'},
    '#475569': {'badge': '#f8fafc', 'text': '#334155', 'border': '#cbd5e1'},
}


def esc(s):
    return html.escape(str(s or ''), quote=False)


def build_css():
    return """  *{margin:0;padding:0;box-sizing:border-box}
  body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(160deg,#f8fafc,#eef2ff);padding:48px 56px;color:#1e293b}
  .container{max-width:1180px;margin:0 auto}
  h1{font-size:38px;font-weight:900;background:linear-gradient(135deg,#1e40af,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:10px;line-height:1.3;letter-spacing:-0.01em}
  .subtitle{font-size:15px;color:#64748b;margin-bottom:28px}
  .map{background:#fff;border-radius:20px;padding:32px 36px;margin-bottom:36px;box-shadow:0 4px 24px rgba(30,64,175,0.06)}
  .map h2{font-size:23px;font-weight:800;color:#1e293b;margin-bottom:12px}
  .map-intro{font-size:15px;line-height:1.8;color:#475569;margin-bottom:20px}
  .legend{display:flex;flex-wrap:wrap;gap:10px;margin-bottom:18px}
  .legend-item{display:inline-flex;align-items:center;gap:7px;font-size:13px;color:#334155;background:#f8fafc;border:1px solid #e2e8f0;border-radius:999px;padding:5px 14px}
  .dot{width:9px;height:9px;border-radius:50%;display:inline-block}
  .nav{display:flex;flex-wrap:wrap;gap:10px}
  .nav-item{display:inline-flex;align-items:center;gap:7px;font-size:13px;color:#475569;text-decoration:none;background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:7px 14px;transition:all .2s}
  .nav-item:hover{background:#eff6ff;border-color:#93c5fd;color:#1e40af}
  .nav-dot{width:8px;height:8px;border-radius:2px;display:inline-block}
  .section{margin-bottom:36px}
  .sec-head{display:flex;align-items:flex-start;gap:14px;margin-bottom:18px}
  .sec-line{width:5px;height:52px;border-radius:3px;flex-shrink:0;margin-top:2px}
  .sec-head h2{font-size:24px;font-weight:800;margin-bottom:4px;letter-spacing:-0.01em}
  .sec-intro{font-size:14px;line-height:1.7;color:#64748b;max-width:960px}
  .cards{display:flex;flex-direction:column;gap:16px}
  .card{background:#fff;border-radius:16px;padding:22px 26px;box-shadow:0 2px 14px rgba(0,0,0,0.05);border:1px solid #eef2f7}
  .card-top{display:flex;align-items:center;gap:10px;margin-bottom:12px}
  .tech-badge{display:inline-block;font-size:12px;font-weight:700;padding:3px 12px;border-radius:999px;border:1px solid}
  .source{font-size:12px;color:#94a3b8}
  .card-index{margin-left:auto;font-size:12px;font-weight:700;color:#cbd5e1;font-variant-numeric:tabular-nums}
  .quote{font-size:16px;line-height:1.85;color:#1e293b;font-weight:600;padding:14px 18px;background:#f8fafc;border-left:4px solid;border-radius:8px;margin-bottom:14px}
  .detail{display:flex;flex-direction:column;gap:10px}
  .detail-row{display:flex;gap:10px;align-items:flex-start}
  .detail-tag{flex-shrink:0;font-size:12px;font-weight:700;padding:2px 10px;border-radius:6px;margin-top:2px}
  .detail-tag.reuse{background:#f1f5f9;color:#475569 !important}
  .detail-text{font-size:13.5px;line-height:1.7;color:#475569}
  .conclusion{background:linear-gradient(135deg,#1e40af,#7c3aed);border-radius:20px;padding:32px 36px;margin:40px 0 8px;box-shadow:0 8px 32px rgba(30,64,175,0.18)}
  .conclusion h2{font-size:22px;font-weight:800;color:#fff;margin-bottom:12px}
  .conclusion-text{font-size:16px;line-height:1.9;color:#e0e7ff;font-weight:500}
  .footer{text-align:center;padding:20px 0 8px}
  .footer p{font-size:13px;color:#94a3b8}
.html-toolbar{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:16px;padding:12px 20px;background:rgba(248,250,252,.92);backdrop-filter:blur(8px);border-bottom:1px solid #e2e8f0;font-family:"PingFang SC","Microsoft YaHei",sans-serif}
.html-toolbar .back-link{font-size:14px;color:#3b82f6;text-decoration:none;white-space:nowrap;font-weight:600}
.html-toolbar .back-link:hover{text-decoration:underline}
.html-toolbar-title{flex:1;font-size:14px;font-weight:600;color:#1e293b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
@media (max-width:640px){
  .html-toolbar{flex-wrap:wrap;gap:10px;padding:10px 12px}
  .html-toolbar-title{flex-basis:100%;order:-1;font-size:13px}
}
body{padding:0!important;margin:0!important}
.container{padding:48px 60px}
@media (max-width:640px){.container{padding:16px 12px!important}.container{max-width:100%!important}h1{font-size:24px!important}h2,.sec-title{font-size:18px!important}h3{font-size:16px!important}p,li{font-size:14px!important}.summary-line{font-size:15px!important;padding:14px 16px!important}.map,.card,.timeline{padding:16px!important;margin-bottom:16px!important}.map h2{font-size:18px!important}.conclusion{padding:20px!important}.footer{padding:20px 0 12px!important}}"""


def build_cards(section):
    color = section['section']['color']
    c = COLORS[color]
    out = []
    for idx, card in enumerate(section['cards'], 1):
        badge_bg = c['badge']
        badge_text = c['text']
        badge_border = c['border']
        tech = esc(card['technique'])
        src = esc(card['source_name'])
        quote = esc(card['quote'])
        ctx = esc(card['context'])
        why = esc(card['why'])
        out.append(f"""    <div class="card">
      <div class="card-top">
        <span class="tech-badge" style="background:{badge_bg};color:{badge_text};border-color:{badge_border}">{tech}</span>
        <span class="source">{src}</span>
        <span class="card-index">{idx:02d}</span>
      </div>
      <div class="quote" style="border-left-color:{color}">{quote}</div>
      <div class="detail">
        <div class="detail-row"><span class="detail-tag" style="background:{badge_bg};color:{badge_text}">场景</span><span class="detail-text">{ctx}</span></div>
        <div class="detail-row"><span class="detail-tag reuse" style="background:{badge_bg};color:{badge_text}">复用</span><span class="detail-text">{why}</span></div>
      </div>
    </div>
""")
    return '\n'.join(out)


def build_sections():
    out = []
    for sec in sections:
        s = sec['section']
        color = s['color']
        cards_html = build_cards(sec)
        out.append(f"""    <div class="section" id="{s['id']}">
      <div class="sec-head">
        <span class="sec-line" style="background:{color}"></span>
        <div>
          <h2 style="color:{color}">{esc(s['title'])}</h2>
          <p class="sec-intro">{esc(s['intro'])}</p>
        </div>
      </div>
      <div class="cards">
{cards_html}      </div>
    </div>
""")
    return '\n'.join(out)


def build_map():
    legend = []
    nav = []
    for sec in sections:
        s = sec['section']
        color = s['color']
        short_title = s['title'].split('：')[1].split('，')[0] if '：' in s['title'] else s['title']
        legend.append(f'<span class="legend-item"><span class="dot" style="background:{color}"></span>{esc(short_title)}</span>')
        count = len(sec['cards'])
        nav.append(f'<a class="nav-item" href="#{s["id"]}"><span class="nav-dot" style="background:{color}"></span>{esc(s["title"].split("：")[1])}（{count}）</a>')
    return f"""    <div class="map">
      <h2>话术总览：说服不是天赋，是七套可复用的句式</h2>
      <p class="map-intro">从 {PODCASTS} 档中文播客、120 篇完整转录中，提炼出 {TOTAL_CARDS} 条真实说服话术。每一类都配了真实原句、说服场景和日常复用方法。建议按板块逐条练习：先背句式，再套自己的场景。</p>
      <div class="legend">
        {'\n        '.join(legend)}
      </div>
      <div class="nav">
        {'\n        '.join(nav)}
      </div>
    </div>
"""


def main():
    css = build_css()
    map_html = build_map()
    sections_html = build_sections()

    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>说服话术 · 从播客中学到的表达武器</title>
<style>
{css}
</style>
</head>
<body>
<div class="html-toolbar">
  <a class="back-link" href="index.html">← 返回首页</a>
  <div class="html-toolbar-title">说服话术 · 从播客中学到的表达武器</div>
</div>
<div class="container">
    <h1>说服话术 · 从播客中学到的表达武器</h1>
    <p class="subtitle">从 120 篇完整转录中提炼 · 286 条候选 → 精选 {TOTAL_CARDS} 条 · 覆盖 {PODCASTS} 档播客</p>

{map_html}
{sections_html}
    <div class="conclusion">
      <h2>一句话带走</h2>
      <p class="conclusion-text">先改变定义（这不是X而是Y），再找个类比（就像Z），配上具体数字，把选择推到未来，最后用问题把结论变成对方自己的——七招合一，就是播客里那些"很会说"的人的底层套路。</p>
    </div>

    <div class="footer">
      <p>音频工作坊 · 播客话术提炼 · 2026 · 覆盖 {PODCASTS} 档播客</p>
    </div>
  </div>
</body>
</html>
"""
    out_path = 'docs/说服话术-从播客中学到的表达武器.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    print(f'已生成 {out_path}')
    print(f'卡片数: {TOTAL_CARDS}, 覆盖播客: {PODCASTS}')


if __name__ == '__main__':
    main()
