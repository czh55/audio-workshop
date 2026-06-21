import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'SpaceX开发史-播客总结.svg');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}
.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:18px 24px;text-align:center;min-width:140px;font-weight:700;font-size:15px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3{color:#92400e;margin-bottom:8px}
.correction p{color:#92400e;font-size:15px;line-height:1.8}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}
.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}
.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .insight{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,0.95);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:15px;line-height:1.8}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.key-data{display:inline-block;background:#1e40af;color:#fff;padding:2px 8px;border-radius:4px;font-size:13px;font-weight:700;margin-right:4px}`;

const body = `<div class="container">

<h1>口述SpaceX开发史：与前高管洪力德聊马斯克用人观、最大IPO、太空与AI</h1>
<div class="meta">
  <span class="tag tag-blue">张小珺Jùn｜商业访谈录</span>
  <span class="tag tag-purple">SpaceX</span>
  <span class="tag tag-orange">Elon Musk</span>
  <span class="tag tag-green">航天产业</span>
  <span class="tag tag-red">AI+太空</span>
  <span class="tag" style="background:#f1f5f9;color:#64748b">3h01min</span>
</div>

<div class="summary-line">
<strong>一句话概括：</strong>前SpaceX火箭首席制造工程师洪力德（Lewis Hong），在SpaceX IPO与收购XAI的历史性时刻，从内部视角还原了Falcon 1/9/Starship的开发史，揭示马斯克"第一原理思维+极致量产化"如何颠覆航天业——把火箭从每公斤2万美元降到3000美元（终极目标100美元以下），并判断太空+AI的融合将开启人类文明扩张的新篇章。
</div>

<div class="timeline">
  <h3>⏱ 关键时间节点</h3>
  <div class="timeline-item"><span class="timeline-time">00:01:24</span><span class="timeline-text">SpaceX IPO 与收购 xAI 的深层逻辑：太空数据中心解决美国缺电+许可难题</span></div>
  <div class="timeline-item"><span class="timeline-time">00:31:30</span><span class="timeline-text">2013年马斯克：极端内向、不善言辞、极度真诚——与今天判若两人</span></div>
  <div class="timeline-item"><span class="timeline-time">01:03:42</span><span class="timeline-text">SpaceX内部真实情况：996文化、一人管全部、叠代第一、可乐罐启示</span></div>
  <div class="timeline-item"><span class="timeline-time">01:30:51</span><span class="timeline-text">"那我接受你的辞呈"——马斯克的管理风格与高压对话实录</span></div>
  <div class="timeline-item"><span class="timeline-time">01:56:35</span><span class="timeline-text">Falcon 9 成败史：2015首次回收→2016两次爆炸→600+连续成功</span></div>
  <div class="timeline-item"><span class="timeline-time">02:11:19</span><span class="timeline-text">航天产业地图：上游造火箭、中游管控、下游应用+中国航天分析</span></div>
</div>

<div class="map">
  <h2>🧩 SpaceX 发展脉络：三部曲</h2>
  <div class="diagram">
    <div class="node">第一部曲<br/>2002-2012<br/><small>0→1</small><br/><small>Falcon 1 成功</small></div>
    <div class="arrow">→</div>
    <div class="node node-green">第二部曲<br/>2012-2022<br/><small>1→1000</small><br/><small>Falcon 9 回收+量产</small></div>
    <div class="arrow">→</div>
    <div class="node node-orange">第三部曲<br/>2022-现在<br/><small>平台化</small><br/><small>Starlink+Starship+AI</small></div>
  </div>
  <div class="diagram" style="margin-top:16px;">
    <div class="node" style="font-size:14px;">Falcon 1<br/><small>2008 第4次成功<br/>公司险倒闭</small></div>
    <div class="arrow">→</div>
    <div class="node" style="font-size:14px;">Falcon 9<br/><small>2015 首次回收<br/>载重25x</small></div>
    <div class="arrow">→</div>
    <div class="node" style="font-size:14px;">Starship<br/><small>载重再5x<br/>目标$100/kg</small></div>
    <div class="arrow">→</div>
    <div class="node node-green" style="font-size:14px;">Starlink<br/><small>通訊网络<br/>赚去火星的钱</small></div>
    <div class="arrow">→</div>
    <div class="node node-orange" style="font-size:14px;">xAI 合并<br/><small>太空数据中心<br/>算力+能源</small></div>
  </div>
</div>

<div class="correction">
  <h3>⚠ 常见误解矫正</h3>
  <p><strong>误解1："SpaceX是一家火箭公司"</strong> → 真相：SpaceX从未把自己定位成火箭公司，火箭是<strong>手段</strong>而非目的。公司使命是"开拓宇宙给全人类探索"。</p>
  <p style="margin-top:8px;"><strong>误解2："马斯克天天乱发推特想一出是一出"</strong> → 真相：Starship、Starlink、太空数据中心这些计划<strong>十几年前就在内部roadmap上</strong>了，不是心血来潮。</p>
  <p style="margin-top:8px;"><strong>误解3："马斯克是个暴君，动不动咆哮骂人"</strong> → 真相：他从<strong>不咆哮</strong>，是个非常平的人。那句"那我接受你的辞呈"是超淡定说出来的。</p>
  <p style="margin-top:8px;"><strong>误解4："太空离我们太远了"</strong> → 真相：如果SpaceX达成目标，10-15年内普通人上太空的成本将是<strong>一张头等舱机票</strong>。</p>
</div>

<div class="section">
  <h2 class="sec-title">一、SpaceX IPO与xAI收购：太空数据中心的底层逻辑</h2>

  <div class="card">
    <h3>为什么是SpaceX收购xAI（而不是Tesla）</h3>
    <p>核心逻辑围绕<strong>太空数据中心</strong>展开。美国AI算力建设面临两大瓶颈：</p>
    <ol>
      <li><strong>许可难题</strong>：在美国建数据中心需要繁琐的审批、社区许可，耗时极长</li>
      <li><strong>电力缺口</strong>：美国在AI之前就有25%-40%的电网缺口（三个电网：东岸、西岸、德州，设施超30年），AI让问题雪上加霜</li>
    </ol>
    <div class="insight">
      <strong>太空的天然优势：</strong>① 无需许可——谁先上谁占位；② 无限太阳能——转换率比地球高10%+；③ 真空环境信息传输速度比最快光纤还快一倍（第一原理推导）；④ 分布式架构不受单一地区电网限制。
    </div>
    <p>Starlink计划2015年启动——火箭刚回收就立刻想到"第二步"。SpaceX从不做无目的之事：Starlink的目的是<strong>为去火星筹措天量资金</strong>。</p>
    <div class="highlight">
      <strong>Louis的判断：</strong>这不是偶然。2014年马斯克就注册了X.com，Zeus+XAI+SpaceX+Neuralink+Boring Company —— 每个公司都服务于一个更大的Master Plan，最终可能聚合成一个像Alphabet一样的"X"控股集团。
    </div>
  </div>

  <div class="card card-purple">
    <h3>xAI的差异化定位：Physical AI 世界模型</h3>
    <p>各AI巨头各有定位：Gemini 有Google搜索、Claude 走ToB编程工具、OpenAI 走大众消费者、而Grok有<strong>马斯克生态的海量物理世界数据</strong>（Tesla自动驾驶+机器人+SpaceX太空数据）。xAI的使命"Understand the Universe"可能指理解<strong>物理世界</strong>，而非泛泛的宇宙。</p>
    <div class="pitfall">
      <strong>争议点：</strong>Louis认为Grok在2026年将迎来突破（去年10万张GPU投入应有产出），但Sam Altman曾称马斯克的"太空算力"计划非常可笑。Louis回应："他眼红。"
    </div>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">二、极端内向的马斯克与反常识用人观</h2>

  <div class="card card-green">
    <h3>2013年的马斯克 vs 今天的马斯克：判若两人</h3>
    <p>2013年全公司大会上的马斯克是一个<strong>极端内向</strong>的人——站在台上极度不适，台下的人比他还不舒服。他不是不会讲，而是风格完全不同。<strong>但有一点从未改变：极度真诚、表里如一。</strong>这是他能凝聚团队的核心原因。</p>
    <div class="quote">
      "马总在X上面乱说话，我就希望他能够少说一点话。"——Louis的无奈。但今天的"表演性"是经过十几年练习出来的。
    </div>
  </div>

  <div class="card">
    <h3>SpaceX招什么人：不招航天专家</h3>
    <p>SpaceX<strong>故意不招</strong>传统航天背景的人。早期扩张Falcon 9生产线时，第一个被请来的团队是<strong>Mini Cooper</strong>的团队——因为Mini Cooper在所有车系中<strong>SKU最多</strong>（车顶7种颜色、后视镜多种颜色、内饰无数组合），最符合"高产量+高变化+稳定品控"的要求。</p>
    <div class="insight">
      <strong>底层逻辑：</strong>马斯克认为航天产业几十年来没有大变化，正是那些人做出来的。要颠覆，必须从行业外引入全新思维。SpaceX看重一个人在短时间内<strong>能多快吸收、成长、适应</strong>，而不是过去几十年的经验。
    </div>
  </div>

  <div class="card card-orange">
    <h3>Louis的入职信：从食品到火箭的跨界</h3>
    <p>Louis入职时正巧马斯克出差，成为<strong>少数没经过Musk亲自面试</strong>就入职的破例者——只能写一封自我陈述信。面对"你做食品的凭什么做火箭"的质疑，他在信中说：<strong>食品是世界上最难的产品</strong>——需要在极短时间内爆发式生产极大量产品，且每个产品都要经过"全人类最高品质审核"（你的嘴）。这些量产化、供应链管理的精髓，正是火箭生产最缺的。</p>
    <p>据说马斯克看到信后<strong>一分钟内拍板</strong>。</p>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">三、SpaceX内部真实情况：996、一人管全部、火箭=最高科技IKEA</h2>

  <div class="card card-red">
    <h3>人才密度与极限压力</h3>
    <ol>
      <li><strong>年轻化</strong>：员工大多20几岁，30出头算"大的"。工程+动手能力极强，有无尽的时间和精力</li>
      <li><strong>一人负责制</strong>：早期一个火箭部件只有一个负责人，你要设计、采购、生产、开发全包。做不出来全公司等你</li>
      <li><strong>6个月定律</strong>：SpaceX内部笑谈——能待超6个月就算元老。很多人进来后"这完全不是我想象的"，很快离开</li>
      <li><strong>996是常规</strong>：每天12小时、每周6天是基本配置。工程师是责任制不付加班费——"你一个小时能做完就回家，需要24小时就留着"</li>
      <li><strong>做好的奖赏是更多工作</strong>：你在SpaceX做得好不好，唯一标准是公司会不会给你加任务</li>
    </ol>
  </div>

  <div class="card">
    <h3>火箭的比喻：最后一滴油与IKEA家具</h3>
    <p><strong>"今天从这开车到洛杉矶，开到你家门口时最后一滴油刚好用完——这就是火箭。"</strong>火箭的最高境界是把运输过程的燃料精确到这个程度，多一点就是低效。</p>
    <p>而火箭内部的外壳/储物柜——Louis负责的部分——被他形容为<strong>"全世界最高科技的IKEA家具"</strong>：要最轻、要承受几倍重力、要跟所有系统完美共容。一个储物柜的成本可能比一栋美国房子还贵。</p>
  </div>

  <div class="card card-green">
    <h3>Falcon 9没有一个一模一样</h3>
    <p>Falcon 9早期发射上百次，<strong>没有两支是一模一样的</strong>。每一次发射都为下一支火箭收集数据——好的坏的立刻纳入改进，立刻迭代，立刻再发射。所以SpaceX需要一个"高产量+高变化+高稳定"的生产系统，这恰恰是Mini Cooper团队的专长。</p>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">四、"那我接受你的辞呈"——马斯克的管理风格</h2>

  <div class="card card-red">
    <h3>跟马斯克开会只谈三件事</h3>
    <p>① 你的东西迟到了 ② 你的东西做不出来 ③ 你的东西需要更多钱。<strong>从来没有轻松的聊天。</strong></p>
    <p>马斯克自称"SpaceX总设计师"不完全是吹牛——所有方向、规格、大大小小的事情，最后拍板的确实是他。</p>
  </div>

  <div class="card">
    <h3>可乐罐的启示</h3>
    <p>Louis的团队花了巨大心血，把Falcon 9上的超级高压桶（轮胎40PSI，这是上万PSI，且要最轻）从采购商那里抢回来自己开发，<strong>成本降低90%、产量翻倍</strong>，团队引以为傲。向马斯克汇报后，他没有说Good，没有说Fine——</p>
    <div class="quote">
      "你有沒有看過可樂罐的生產？可樂罐也是耐壓產品。為什麼可樂罐可以一分鐘生產上千個、幾分錢一個？你們這個，是不是還有改進的空間？"
    </div>
    <p>从第一原理看，<strong>你无法反驳他</strong>。但这就是马斯克——从不表扬，永远把你推向你不知道自己能到的境界。</p>
  </div>

  <div class="card card-orange">
    <h3>"那我接受你的辞呈"——真实故事</h3>
    <p>一位资深工程师在向马斯克汇报进度时，因进度不如预期被反复追问，最后说了一句：<strong>"你要做的这个东西不可能。"</strong></p>
    <p>马斯克<strong>非常淡定</strong>地回了一句："好，那我接受你的辞呈。"</p>
    <p>空气凝结。30秒沉默。那个人就走出去了。</p>
    <div class="insight">
      <strong>关键点：</strong>他没有咆哮、没有拍桌子、没有骂你是废物。Musk是一个<strong>没有等级感、没有太多喜怒哀乐的人</strong>——他开心时会像小孩一样笑，生气时直接让人走，但从不大声。他是一个极度"平"的人。
    </div>
  </div>

  <div class="card card-purple">
    <h3>马斯克<strong>没有任何情绪价值</strong>——但他用另一种方式领导</h3>
    <p>他不会鼓励你，不会表扬你。但他的情绪价值来自于：他是<strong>一个真的人</strong>——他相信自己在做的事，他把自己永远放在最前线跟你一起奋斗。大家跟着他，是因为他的真诚和愿景，不是因为他的夸奖。</p>
    <p>特斯拉员工曾抱怨：马斯克偏袒SpaceX——SpaceX是"被宠坏的妹妹"，特斯拉是"辛苦赚钱养妹妹的姐姐"。因为SpaceX得到了老板更多的关注和更好的资源。</p>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">五、Falcon 9 开发史：成功与失败</h2>

  <div class="card">
    <h3>发射成本革命：从2万到100美元/公斤</h3>
    <table>
      <tr><th>时代</th><th>每公斤上太空成本</th><th>代表</th></tr>
      <tr><td>SpaceX之前</td><td><span class="key-data">$10,000-$20,000</span></td><td>ULA、波音</td></tr>
      <tr><td>Falcon 9 回收后</td><td><span class="key-data">~$3,000</span> (降约10x)</td><td>SpaceX</td></tr>
      <tr><td>Starship 目标</td><td><span class="key-data">&lt;$100</span> (降200x)</td><td>SpaceX新城</td></tr>
    </table>
    <p>当成本降到200分之一时，很多以前"天方夜谭"的项目在账上都算得过来了。</p>
  </div>

  <div class="card card-red">
    <h3>Falcon 1：差点让SpaceX倒闭的火箭</h3>
    <p>SpaceX成立时只有够发射<strong>3次</strong>Falcon 1的钱。前3次全部失败，公司濒临倒闭。第4次杯水一救，2008年成功了。<strong>然而成功之后，SpaceX立刻把Falcon 1退役了</strong>——因为它从不是为了卖Falcon 1而存在。它可以变現（载重1吨，与今天Rocket Lab的Electron同级且有优势），但选择了更大的路。</p>
    <div class="insight">
      "Falcon 1只是一个手段，不是目的。SpaceX从来不是一家火箭公司。"
    </div>
  </div>

  <div class="card card-green">
    <h3>2015年12月21日：每一个SpaceX人铭记的日子</h3>
    <p>第一次成功将火箭送入轨道<strong>并成功回收</strong>。这支火箭至今仍在LA SpaceX总部展出。</p>
    <p>但2015/2016年紧随两次爆炸——<strong>两次都跟Louis的部门有关</strong>。那是在"已经是业界最先进的火箭"之后发生的失败——你无法问任何人，"未知未知"是最可怕的。靠直觉和运气猜中了根因，修改后至今600+发射无问题。</p>
    <div class="quote">
      "那是SpaceX真正最困难的时候。刚经历了多次成功，跑在全行业最前面——然后你失败了。"——Louis回忆这是他在SpaceX压力最大的时期，久未生病的他病倒了。
    </div>
  </div>

  <div class="card">
    <h3>Falcon 9 = 航空业的 Model T</h3>
    <p>Louis将Falcon 9比作福特Model T——第一次将火箭<strong>大量化</strong>的产品。Starship希望跨越到Model 3级别，但他认为能到Model S已经不错。</p>
    <p>Falcon 9从开发到回收耗时<strong>10年</strong>，Starship只用了<strong>一半时间</strong>达到相同里程碑。按此速度，2-3年内可能达到成熟。</p>
  </div>

  <div class="card card-orange">
    <h3>Louis离开SpaceX的契机：一台Model 3</h3>
    <p>2018年底马斯克发全员信促销特斯拉，Louis买了一台Model 3——他人生第一台新车。开车的瞬间他从机械工程角度意识到：<strong>电车不是噱头，潜力比油车大得多</strong>。如果有什么比SpaceX更大的机会，一定在电车产业里。2019年他跳槽到一家电池公司，后来成功退出。</p>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">六、航天产业链：上游-中游-下游</h2>

  <div class="card">
    <h3>产业链三层结构</h3>
    <table>
      <tr><th>环节</th><th>内容</th><th>关键词</th></tr>
      <tr><td><strong>上游</strong></td><td>火箭建造与开发、发射、卫星建造、太空站开发</td><td>"苦活"</td></tr>
      <tr><td><strong>中游</strong></td><td>卫星之间的管控调整、数据传输管理</td><td>"管控层"</td></tr>
      <tr><td><strong>下游</strong></td><td>Starink、全球监控、材料科学(完美球体、光纤)、太空制造</td><td>"So What?"</td></tr>
    </table>
  </div>

  <div class="card card-green">
    <h3>太空的独特价值：在地球上花大钱模拟太空，不如直接去太空</h3>
    <p>太空环境的<strong>真空+无重力+极端温差</strong>提供了地球上无法复制的制造条件：</p>
    <ul>
      <li><strong>完美球体</strong>：地球上无法做出真正的完美球体（受压、受材质局限），太空无重力下很容易</li>
      <li><strong>晶圆制造</strong>：建一个晶圆厂要几十亿美元，花那么多钱<strong>其实就是在模拟太空环境</strong></li>
      <li><strong>光纤</strong>：太空制造的光纤质量远超地球上任何工艺</li>
    </ul>
    <div class="insight">
      <strong>Louis的投资逻辑：</strong>"以前可能没有这个选择。但现在因为SpaceX，我们即将进入这个时代。"他投资的太空站公司甚至要做<strong>可控地心引力的太空站</strong>——人类首次拥有"温度、压力、引力"三个可控维度。
    </div>
  </div>

  <div class="card card-orange">
    <h3>竞争与垄断：真正的对手是谁</h3>
    <p><strong>SpaceX的对手是自己。</strong>但团队密切<strong>关注中国航天</strong>的发展——中国在生产迭代上有明显优势。Louis认为最被误解的是"中美谁更厉害"的话题——太空空间是全球的，<strong>不存在中国空间vs美国空间</strong>，所有东西都在环绕全球，唯一一个<strong>全人类必须共同发展</strong>的领域。</p>
  </div>

  <div class="card">
    <h3>SpaceX的终极估值：至少万亿级</h3>
    <p>Louis至今未出售任何SpaceX股票。"太空第一轨只是第一站，卫星只是第一站，月球只是第一站——太空的环境比地球大好太多太多了。"他认为SpaceX至少是<strong>万亿</strong>级的公司。</p>
    <p>SpaceX更深远的价值：创造了一批<strong>"SpaceX Mafia"</strong>——在美国做硬件的年轻创业者（20-30几岁），他们掌握了"怎么在美国生产全世界最先进硬件"的know-how。这是Louis当下基金的核心投资方向。</p>
  </div>
</div>

<div class="conclusion">
  <h2>总结与行动启示</h2>

  <h3>🎯 核心要点</h3>
  <ol>
    <li><strong>第一原理思维</strong>是SpaceX一切决策的根源：从物理定律出发而非行业惯例（可乐罐vs高压桶）</li>
    <li><strong>火箭只是手段</strong>——SpaceX从未定位为火箭公司，终极使命是多星球物种</li>
    <li><strong>不招行业专家</strong>——跨界人才+年轻化+高密度+极限授权，才是颠覆性创新的组织密码</li>
    <li><strong>发射成本降200倍</strong>是行业真正转折点，让"天方夜谭"变成算得过账的生意</li>
    <li><strong>太空+AI</strong>不是噱头：太空天然解决了AI算力建设的许可和能源瓶颈，xAI的差异化在Physical AI</li>
    <li><strong>航天业正在汽车产业化</strong>——Falcon 9是Model T，中国市场不可忽视</li>
  </ol>

  <h3>✅ 可执行的行动清单</h3>
  <ol>
    <li>关注2026年SpaceX IPO时机——主流市场首次对太空赛道"真正买单"</li>
    <li>跟踪"SpaceX Mafia"创业项目——从SpaceX/Tesla出来的年轻创业者，是美国硬件创新的核心力量</li>
    <li>太空下游应用（材料科学、太空制造、全球无缝监控、可控引力）是下一波投资机会，不只是卫星通信</li>
    <li>关注xAI + SpaceX 太空数据中心的工程进展——如果成功，将改变全球算力格局</li>
    <li>阅读《硅谷钢铁侠》而非《马斯克传》——Louis认为前者更能呈现"创业者真正需要的精髓"</li>
  </ol>

  <h3>🔄 关键认知转变</h3>
  <p><strong>以前以为：</strong>马斯克是个异想天开的暴君，想到什么说什么，火箭跟AI合并不合理。</p>
  <p><strong>现在理解：</strong>Starship、Starlink、太空数据中心十几年前就在roadmap上；马斯克是一个"极度真诚、从不咆哮、用第一原理不断推高你上限"的人；xAI+SpaceX合并是算力与运输问题的系统性解法，是同一张蓝图上的两块拼图。太空不是遥远的科幻——10-15年内普通人上太空只需一张头等舱机票的钱。</p>
</div>

<div class="footer">
  来源：小宇宙FM - 张小珺Jùn｜商业访谈录 第145期 | 嘉宾：洪力德 Lewis Hong (前SpaceX火箭首席制造工程师, Airis Fund GP) | 转录：Whisper small | 生成时间：2026-06-21
</div>

</div>`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
