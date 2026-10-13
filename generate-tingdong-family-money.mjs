/**
 * 听懂涨声 · 中国家庭最缺的一课：父子关于钱、认知与风险的坦白局 → SVG
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs/tingdong_family_money-总结.svg');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:32px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:78px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:16px 20px;text-align:center;min-width:130px;font-weight:700;font-size:14px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.node-purple{background:linear-gradient(135deg,#f5f3ff,#ede9fe);border-color:#c4b5fd;color:#5b21b6}
.arrow{font-size:22px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3{color:#92400e;margin-bottom:8px}.correction p{color:#92400e;font-size:15px}
.section{margin-bottom:28px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:28px;margin-bottom:18px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}.card.card-purple{border-left-color:#8b5cf6}
.card h3{font-size:19px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.speaker{display:inline-block;font-size:13px;font-weight:600;padding:2px 10px;border-radius:12px;margin-right:8px}
.speaker-host{background:#dbeafe;color:#1e40af}.speaker-guest{background:#ede9fe;color:#6b21a8}.speaker-son{background:#ffedd5;color:#9a3412}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,0.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}`;

const body = `
<div class="container">
  <h1>听懂涨声｜中国家庭最缺的一课：一对父子关于钱、认知与风险的坦白局</h1>
  <div class="meta">
    <span class="tag tag-blue">播客</span>
    <span class="tag tag-purple">代际金钱观</span>
    <span class="tag tag-orange">约88分钟</span>
    <span class="tag tag-green">杨天楠 × 冉总 × Warren</span>
  </div>
  <div class="summary-line">
    中国家庭最缺的不是又一门理财课，而是能像两个平等的人一样坦白谈钱。价值投资老爸（胜率）碰上科技/加密少年（赔率）：公路移动课堂、腌咸菜/鸭蛋的时间复利、气垫式父母——把「忌讳谈钱」换成「早开以时间为函数的事」。
  </div>

  <div class="timeline">
    <h3>关键时间轴</h3>
    <div class="timeline-item"><span class="timeline-time">01:27</span><span class="timeline-text">17岁Warren：四年级投美股，A股/加密并行，经历三轮牛熊</span></div>
    <div class="timeline-item"><span class="timeline-time">05:19</span><span class="timeline-text">父子横穿北美5万公里：边旅行边聊人生的「移动课堂」</span></div>
    <div class="timeline-item"><span class="timeline-time">12:59</span><span class="timeline-text">学校没教的三件事：怎么与人交流、怎么看待钱、怎么认识规律</span></div>
    <div class="timeline-item"><span class="timeline-time">16:14</span><span class="timeline-text">1997→房改起飞：建筑师撞上地产大时代，后遇周期尾部</span></div>
    <div class="timeline-item"><span class="timeline-time">28:44</span><span class="timeline-text">最难的不是换赛道，而是摆脱过去的成功经验</span></div>
    <div class="timeline-item"><span class="timeline-time">31:59</span><span class="timeline-text">「杀死昨天的自己」：认知升级是残酷过程</span></div>
    <div class="timeline-item"><span class="timeline-time">39:36</span><span class="timeline-text">财富、认知、人际连接都可以产生复利</span></div>
    <div class="timeline-item"><span class="timeline-time">50:46</span><span class="timeline-text">玩具堆旁讲市盈率：学习一旦连上财富就突然有趣</span></div>
    <div class="timeline-item"><span class="timeline-time">56:33</span><span class="timeline-text">一个追胜率，一个找高赔率：父子投资逻辑对撞</span></div>
    <div class="timeline-item"><span class="timeline-time">01:03:08</span><span class="timeline-text">有8000元投还是存？普世教育与投资常识的错位</span></div>
    <div class="timeline-item"><span class="timeline-time">01:20:22</span><span class="timeline-text">「禁忌越多，诱惑越大」：允许孩子摸一下热水壶</span></div>
    <div class="timeline-item"><span class="timeline-time">01:25:36</span><span class="timeline-text">父母不是规划师，是悬崖下的大气垫</span></div>
  </div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram">
      <div class="node">忌讳谈钱<br/>学校滤镜</div>
      <div class="arrow">→</div>
      <div class="node node-orange">公路坦白<br/>平等对话</div>
      <div class="arrow">→</div>
      <div class="node node-purple">胜率 × 赔率<br/>代际对撞</div>
      <div class="arrow">→</div>
      <div class="node node-green">早开时间函数<br/>气垫托底</div>
    </div>
  </div>

  <div class="correction">
    <h3>认知纠偏</h3>
    <p>这不是教你复制「十一岁炒股」或追加密；也不是否定价值投资。核心样本是：家庭可以不把钱当禁忌，用真实周期与小额试错做教育。嘉宾经历为个案，不构成投资建议。生活里「要答完每道题 / 去热闹处 / 总得做点什么」的普世教育，与投资里「不懂不碰 / 远离热闹 / 买完少动」经常是反的——混用会亏钱。</p>
  </div>

  <div class="section">
    <h2 class="sec-title">四张关键卡片</h2>

    <div class="card">
      <h3>① 代际金钱观差异：胜率老爸 × 赔率少年</h3>
      <p><span class="speaker speaker-guest">冉总</span>建筑师→地产周期→北美宏观投研；信奉价值与配置，过年生日送价值股（如长江电力）。<span class="speaker speaker-son">Warren</span>11岁听市盈率，四年级起投台积电/英伟达，美股科技+加密+A股三线并行，经历三轮牛熊——网约车上都能为策略吵翻。</p>
      <div class="quote">「对于有积累的人，高确定性、高胜率很重要；对特别年轻的人，连续下注高赔率是财务跃迁的关键点——但别把高赔率压注当成整套投资体系。」</div>
      <div class="relation">关系：差异不是对错，而是年龄与资本存量决定的最优策略不同；冲突本身就是教育素材。</div>
    </div>

    <div class="card card-orange">
      <h3>② 风险偏好：周期体感 vs 泡沫摸高</h3>
      <p>父亲从2014年起收缩地产业务，亲历「活儿还多、利润变薄」的尾部；2014「互联网+」真金白银踩坑，才理解摆脱旧成功经验有多痛。儿子在牛市刷信息、熊市攒仓，愿意在科技与加密里摸高，但也强调极端狂热时会出售。</p>
      <div class="highlight">宏观配置视角：看资产包的波峰波谷——底部略多、泡沫略减；中国投资者越来越需要全球宏观视角。</div>
      <div class="pitfall">陷阱：把父亲的周期谨慎照搬给年轻人（错过学习赔率），或把儿子的摸高照搬给已有积累者（用生活本金赌赔率）。</div>
    </div>

    <div class="card card-purple">
      <h3>③ 坦白机制：公路无信号 + 哥们式平等</h3>
      <p>5万公里北美公路：没信号、不能刷手机，父子被迫长时间对话；参观苹果/英伟达与通用/波音场，科技繁荣与制造业颓废形成对照。父母角色从「关门父子」切到「哥们」——平等、可说、自然，家庭紧密度反而上升。</p>
      <div class="quote">「禁忌越多，诱惑越大。」弟弟摸热水壶：允许小痛一次，比反复禁止更有效。非原则问题甩回孩子：「不折腾，没折腾。」</div>
      <div class="action">怎么用：每周留一段「无手机、可谈钱」的共处；先谈自己的踩坑，再谈规则——坦白先于说教。</div>
    </div>

    <div class="card card-green">
      <h3>④ 家庭缺课是什么：三件事 + 时间函数</h3>
      <p>学校科班缺三课：①怎么与人交流（情商操作面）；②怎么看待钱（中国忌讳提钱，却是终身必修）；③怎么认识/尊重/顺应规律。冉总：美好事物多为时间的函数——今天同时腌咸菜和鸭蛋，一个月后两样都有；只腌一样，就吃不到另一样。</p>
      <div class="highlight">父母定位：不是替孩子规划人生的人，而是悬崖下的大气垫——抓手他自己够，托底家庭给。</div>
      <div class="relation">对照8000元故事：有人说「存起来别投资」被视为金钱观陷阱；考试「每题都答」与投资「不懂交白卷」完全相反——家庭若只教存钱与卷题，会把孩子送进投资常识的对立面。</div>
    </div>
  </div>

  <div class="card">
    <h3>父子立场对比</h3>
    <table>
      <tr><th>维度</th><th>冉总（父）</th><th>Warren（子）</th></tr>
      <tr><td>核心策略</td><td>价值投资 / 宏观配置 / 高胜率</td><td>科技成长 + 加密摸高 / 高赔率试错</td></tr>
      <tr><td>礼物与教育</td><td>过年生日送价值类股票</td><td>玩具旁学市盈率、财报，真仓练手</td></tr>
      <tr><td>时代红利体感</td><td>中国地产大周期 → 全球宏观投研</td><td>中加美成长，AI/科技叙事更近</td></tr>
      <tr><td>风险姿态</td><td>周期底部加、泡沫减；杀昨日之我</td><td>年轻时连续下注赔率，狂热时也会卖</td></tr>
      <tr><td>人生复利</td><td>财富+认知+人际都可复利；不愿躺平</td><td>学习与财富挂钩后投入陡增；敢要敢问</td></tr>
      <tr><td>对父母角色</td><td>大气垫 + 开放环境，不替孩子定路线</td><td>当哥们聊策略；整合中美资源做组织</td></tr>
    </table>
  </div>

  <div class="section">
    <h2 class="sec-title">方法边界</h2>
    <div class="card">
      <h3>听完能带走的，与带不走的</h3>
      <p><strong>可迁移</strong>：家庭把钱从禁忌区移到可讨论区；用公路/旅行制造深度对话；早开启「以时间为函数」的事（认知、资产、人际）；父母做气垫而非编剧；区分生活教育与投资常识的反直觉点。</p>
      <p><strong>不可直接复制</strong>：特定阶层的资本缓冲、北美公路与跨境教育资源、11岁真仓交易的合规与心理代价、嘉宾个案收益数字。</p>
      <div class="pitfall">边界：没有气垫却逼孩子「高赔率试错」= 把家庭推下悬崖；只有说教没有坦白 = 禁忌继续制造诱惑。</div>
    </div>
  </div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <ul>
      <li>缺课不是「不会炒股」，而是缺平等坦白谈钱 + 认识规律的家庭练习场。</li>
      <li>胜率与赔率可并存：存量用胜率守，年轻学习期用可控赔率练——别互相反噬。</li>
      <li>认知升级=杀死昨天的自己：换赛道易，扔掉旧成功经验难。</li>
      <li>父母最优交付往往是气垫与开放，不是完美人生脚本。</li>
    </ul>
    <h3>行动清单</h3>
    <ol>
      <li>本周发起一次「钱的坦白局」：各说一笔赚过/亏过的钱，以及当时的判断（不评判）。</li>
      <li>列三件「以时间为函数」想早开的事（学习、资产、关系），本月各开一个最小动作。</li>
      <li>对照检查：家里是否在用「考试答满卷」逻辑指导投资——改成「不懂可以交白卷」。</li>
      <li>给孩子（或自己）划一条「可摸热水壶」小额试错预算，原则外的事交回本人决策。</li>
      <li>写清父母角色一句话：我是气垫还是编剧？下周只做气垫该做的一件事。</li>
    </ol>
    <h3>关键认知转变</h3>
    <p>从「家里不谈钱才体面」转向「像两个平等的人坦白谈钱、认知与风险」——家庭缺的一课，首先是对话机制，其次才是资产配置。</p>
  </div>
  <div class="footer">来源：听懂涨声 · 中国家庭最缺的一课 · 音频转写总结 · audio-workshop · 不构成投资建议</div>
</div>
`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
