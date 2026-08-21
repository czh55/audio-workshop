/**
 * 说服话术提炼 SVG 生成器
 * 输入: /tmp/huashu-sections.json（7 大板块 53 条话术）
 * 输出: docs/说服话术-从播客中学到的表达武器.svg
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs/说服话术-从播客中学到的表达武器.svg');

const sections = JSON.parse(fs.readFileSync('/tmp/huashu-sections.json', 'utf-8'));

const COLORS = {
  '#2563EB': { bg: '#eff6ff', border: '#bfdbfe', text: '#1e40af' },
  '#059669': { bg: '#ecfdf5', border: '#a7f3d0', text: '#065f46' },
  '#D97706': { bg: '#fffbeb', border: '#fde68a', text: '#92400e' },
  '#7C3AED': { bg: '#f5f3ff', border: '#ddd6fe', text: '#5b21b6' },
  '#DC2626': { bg: '#fef2f2', border: '#fecaca', text: '#991b1b' },
  '#0891B2': { bg: '#ecfeff', border: '#a5f3fc', text: '#155e75' },
  '#475569': { bg: '#f8fafc', border: '#cbd5e1', text: '#334155' },
};

function esc(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function sourceLabel(s) {
  const map = {
    'nvidia-cosmos-interview': '张小珺商业访谈',
    'neo-labs-capital-wave': '张小珺商业访谈',
    'spacex_history_podcast': '口述SpaceX开发史',
    'finding-kindred': '半拿铁',
    'good-feelings-together': '对话好状态',
    'friends-third-place': '第三杯别空',
    'taipei-witch-house': '小心地滑',
    'bull-market-desire': '重阳Talk',
    'china-consumption-confidence': '武财人',
    'huajing-s-value': '百车全说',
    'why-pay-consumer-vol36': '消费启示录',
    'supermarket-choice': '逛街专家',
    'nyc-year-pessimist': '起朱楼宴宾客',
    'moving-12-times-self-discovery': '切片不计划',
    'distant-goal-first-step': '另辟西径',
    'philippines-english-study': '墙里墙外',
    'japan-price-changes': '范来张口FM',
    'summer-skincare': '夏季护肤指南',
    'longterm-outdoor-gear': '岳下户外',
    'kailash-trekking-guide': '冈仁波齐徒步',
    'tanian-taweng-hiking-guide': '他念他翁徒步',
    'travel-camera-spring-guide': '旅行相机指南',
    'suntory-oolong-china-photography': '风土摄影',
  };
  return map[s] || s;
}

function cardHtml(c, color, index) {
  const cpal = COLORS[color];
  const technique = esc(c.technique.split('（')[0]);
  const source = esc(sourceLabel(c.source));
  return `
    <div class="card">
      <div class="card-top">
        <span class="tech-badge" style="background:${cpal.bg};color:${cpal.text};border-color:${cpal.border}">${technique}</span>
        <span class="source">${source}</span>
        <span class="card-index">${String(index).padStart(2, '0')}</span>
      </div>
      <div class="quote" style="border-left-color:${color}">${esc(c.quote)}</div>
      <div class="detail">
        <div class="detail-row"><span class="detail-tag" style="background:${cpal.bg};color:${cpal.text}">场景</span><span class="detail-text">${esc(c.context)}</span></div>
        <div class="detail-row"><span class="detail-tag reuse" style="background:${cpal.bg};color:${cpal.text}">复用</span><span class="detail-text">${esc(c.why)}</span></div>
      </div>
    </div>`;
}

function sectionHtml(s) {
  const color = s.color;
  const cards = s.cards.map((c, i) => cardHtml(c, color, i + 1)).join('\n');
  return `
    <div class="section" id="${s.id}">
      <div class="sec-head">
        <span class="sec-line" style="background:${color}"></span>
        <div>
          <h2 style="color:${color}">${esc(s.title)}</h2>
          <p class="sec-intro">${esc(s.intro)}</p>
        </div>
      </div>
      <div class="cards">${cards}</div>
    </div>`;
}

const body = `
  <div class="container">
    <h1>说服话术 · 从播客中学到的表达武器</h1>
    <p class="subtitle">从 23 档中文播客的真实讨论中提炼 · 143 条候选 → 精选 53 条</p>

    <div class="map">
      <h2>话术总览：说服不是天赋，是七套可复用的句式</h2>
      <p class="map-intro">播客主播和嘉宾之所以听起来"很会说话"，不是因为聪明，而是反复使用七类话术结构。每一类都配了真实原句、说服场景和日常复用方法。建议按板块逐条练习：先背句式，再套自己的场景。</p>
      <div class="legend">
        <span class="legend-item"><span class="dot" style="background:#2563EB"></span>重新定义</span>
        <span class="legend-item"><span class="dot" style="background:#059669"></span>类比说服</span>
        <span class="legend-item"><span class="dot" style="background:#D97706"></span>反常识冲击</span>
        <span class="legend-item"><span class="dot" style="background:#7C3AED"></span>数字与细节</span>
        <span class="legend-item"><span class="dot" style="background:#DC2626"></span>推演未来</span>
        <span class="legend-item"><span class="dot" style="background:#0891B2"></span>对话技巧</span>
        <span class="legend-item"><span class="dot" style="background:#475569"></span>可信度经营</span>
      </div>
      <div class="nav">
        ${sections.map(s => `<a class="nav-item" href="#${s.id}"><span class="nav-dot" style="background:${s.color}"></span>${esc(s.title.split('：')[1])}（${s.cards.length}）</a>`).join('\n')}
      </div>
    </div>

    ${sections.map(sectionHtml).join('\n')}

    <div class="conclusion">
      <h2>一句话带走</h2>
      <p class="conclusion-text">先改变定义（这不是X而是Y），再找个类比（就像Z），配上具体数字，把选择推到未来，最后用问题把结论变成对方自己的——七招合一，就是播客里那些"很会说"的人的底层套路。</p>
    </div>

    <div class="footer">
      <p>音频工作坊 · 播客话术提炼 · ${new Date().getFullYear()}</p>
    </div>
  </div>
`;

const css = `
  *{margin:0;padding:0;box-sizing:border-box}
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
`;

const { svg, height } = await buildSvg({ css, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log(`已生成: ${OUT}`);
console.log(`高度: ${height}px`);
