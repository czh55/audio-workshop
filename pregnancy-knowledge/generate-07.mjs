import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from '/Users/chenzhiheng/Projects/audio-workshop/svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'topics', 'pregnancy', '07-孕期疾病治疗与护理.svg');

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f0fdf4,#dcfce7);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:38px;font-weight:900;background:linear-gradient(135deg,#065f46,#059669);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:24px;font-weight:700;color:#065f46;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #bbf7d0}
h3{font-size:19px;font-weight:700;color:#334155;margin-bottom:10px}
p{font-size:15px;line-height:1.8;color:#475569;margin-bottom:8px}
ul,ol{padding-left:20px;margin:8px 0}
li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:4px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-red{background:#fee2e2;color:#991b1b}
.tag-yellow{background:#fef3c7;color:#92400e}
.meta{margin:12px 0 20px}
.summary-line{font-size:17px;line-height:1.7;color:#064e3b;padding:18px 24px;background:#fff;border-radius:12px;border-left:4px solid #059669;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.section{margin-bottom:28px}
.sec-title{font-size:20px;font-weight:700;color:#065f46;margin-bottom:14px;padding-left:14px;border-left:4px solid #059669}
.card{background:#fff;border-radius:14px;padding:28px;margin-bottom:16px;box-shadow:0 4px 16px rgba(0,0,0,0.04);border-left:4px solid #059669}
.card.card-red{border-left-color:#dc2626}
.card h3{font-size:18px;font-weight:700;color:#064e3b;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#92400e;border-left:3px solid #f59e0b}
.card .pitfall{background:#fef2f2;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#991b1b;border-left:3px solid #ef4444}
.card .action{background:#eff6ff;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#1e40af;border-left:3px solid #3b82f6}
.conclusion{background:linear-gradient(135deg,#064e3b,#059669);color:#fff;border-radius:18px;padding:32px;margin-top:28px}
.conclusion h2{font-size:24px;font-weight:800;margin-top:0;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:17px;font-weight:700;color:rgba(255,255,255,0.9);margin:18px 0 8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:14px}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:28px 0 12px}
`;

const body = `
<div class="container">
  <h1>孕期疾病治疗与护理</h1>
  <div class="meta">
    <span class="tag tag-green">7 节课</span>
    <span class="tag tag-blue">甲状腺 · 糖尿病 · 高血压 · 乙肝 · 羊水 · 胎儿体重 · 胎盘</span>
  </div>
  <div class="summary-line">
    孕期常见疾病的识别、治疗原则与自我管理要点 —— 从甲功异常到胎盘急症，建立「早发现、科学治、不恐慌」的认知框架。
  </div>

  <div class="section">
    <div class="sec-title">第 81 课 · 甲亢、甲减、桥本氏甲状腺炎</div>

    <div class="card">
      <h3>在讲什么</h3>
      <p>孕期三种甲状腺功能异常的区别：甲减（TSH 升高，最常见）、甲亢（TSH 降低，分 HCG 相关/自身免疫/Graves 病）、桥本氏甲状腺炎（TPOAb 阳性），以及各自的诊断指标和治疗用药选择（PTU vs MMI）。</p>
      <div class="highlight">📌 关键理解：孕早期 HCG 升高可致暂时性甲亢，随 HCG 下降自愈，无需治疗；只有 Graves 病引起的有症状甲亢才需药物干预，利大于弊。桥本最终会走向甲减，产后尤其易爆发产后甲状腺炎。</div>
      <div class="action">✅ 行动项：甲亢用药期间每 4 周复查甲功 + 肝功能 + 血常规；控制目标 FT3/FT4 在正常上限或略高，TSH &lt; 2.5；产后首选甲巯咪唑（MMI），肝毒性小且不影响哺乳；桥本患者产后务必复查甲功。</div>
      <div class="pitfall">⚠️ 避坑：不要因孕期甲亢就直接引产（甲亢可治疗）；不要忽视产后甲功复查（桥本易转化为甲减）；PTU 肝毒性大，孕早期使用需监测肝功能。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 82 课 · 妊娠糖尿病</div>

    <div class="card">
      <h3>在讲什么</h3>
      <p>妊娠期糖尿病（GDM）的 OGTT 诊断标准（空腹 5.1/1h 10.0/2h 8.5 mmol/L）、血糖管理四步法（自我监测 → 饮食调整 → 运动 → 胰岛素），以及分娩方式选择和产后 OGTT 复查的重要性。</p>
      <div class="highlight">📌 关键理解：80%~90% 的 GDM 准妈妈仅靠生活方式调整即可控糖；胰岛素不通过胎盘，孕期使用安全；产后仍有 1/3 的人血糖异常，不可忽视复查。糖尿病 ≠ 必须剖宫产。</div>
      <div class="action">✅ 行动项：每天测 4 次血糖（空腹 + 三餐后 2h），目标空腹 ≤5.3、餐后 ≤6.7 mmol/L；少食多餐（5~6 餐/日），碳水 &lt; 40% 总热量，精米精面换全麦杂粮；每顿饭后散步 10~15 分钟；产后 6~12 周务必复查 OGTT，计划再孕前也需复查。</div>
      <div class="pitfall">⚠️ 避坑：不要以为生完就自愈而跳过产后复查（高达 1/3 异常率）；不要完全不吃主食（改用低 GI 碳水即可）；不要迷信「糖尿病必须剖宫产」（血糖控制好可顺产）。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 83 课 · 妊娠高血压和子痫前期</div>

    <div class="card card-red">
      <h3>在讲什么</h3>
      <p>妊高症（≥140/90 mmHg）与子痫前期（高血压 + 器官损伤）的区别、日常血压 &amp; 胎动监测方法、降压药使用原则（启动阈值 160/110）、终止妊娠时机，以及产后复查与再次怀孕的预防用药（阿司匹林）。</p>
      <div class="highlight">📌 关键理解：妊高症的根本原因在胎盘，只有终止妊娠才能根治；降压目标不是越低越好（高压 130~150，低压 80~100），过低影响胎盘供血；子痫前期可在 1 周内从轻症恶化为抽搐，必须高度警惕。</div>
      <div class="action">✅ 行动项：建立 Excel 记录每日血压时间 &amp; 数值、用药量和不适症状；严格数胎动；出现头痛、视物模糊、上腹痛、尿量减少、水肿急剧加重任一症状立即就医；产后 12 周复查血压；有子痫前期史者再次怀孕从 12~13 周起口服阿司匹林 100~150mg/日预防。</div>
      <div class="pitfall">⚠️ 避坑：不要盲目不吃盐（正常每日 6g 即可，需供碘）；不要卧床不动（仅血压控制不佳者需减少活动）；不要追求把血压降得越低越好（过低影响胎盘血流）。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 84 课 · 乙肝全孕期指南</div>

    <div class="card">
      <h3>在讲什么</h3>
      <p>按备孕→怀孕→分娩→产后四阶段讲解乙肝管理：备孕筛查 + 疫苗接种、孕期抗病毒治疗时机（病毒 DNA &gt; 2×10⁵ IU/mL）、分娩方式（顺产优先）、新生儿 12 小时内联合免疫及母乳喂养的安全性。</p>
      <div class="highlight">📌 关键理解：剖宫产不能减少乙肝母婴传播，无顺产禁忌应优先顺产；孕期可用替比夫定、替诺福韦等相对安全的抗病毒药；CDC 明确建议乙肝妈妈可以母乳喂养，仅乳头皲裂出血时暂停。</div>
      <div class="action">✅ 行动项：备孕前查乙肝表面抗原，全阴性者先接种疫苗再怀孕；乙肝携带者孕 26~28 周复查病毒 DNA，若 &gt; 2×10⁵ IU/mL 则 28~30 周启用抗病毒治疗；宝宝出生 12h 内注射乙肝免疫球蛋白 + 第一针乙肝疫苗（0-1-6 月方案）；9~12 月龄检测乙肝抗原抗体确认免疫效果。</div>
      <div class="pitfall">⚠️ 避坑：不要因为乙肝放弃母乳喂养（乳汁传播概率可忽略不计）；不要以为剖宫产能预防乙肝传播（无循证支持）；备孕女性不要跳过乙肝筛查（我国 1 亿携带者，10 人中 1 人）。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 85 课 · 羊水异常增多或减少</div>

    <div class="card">
      <h3>在讲什么</h3>
      <p>羊水的来源（胎儿尿液，动态循环）、羊水过少（AFI &lt; 5cm 或最大深度 &lt; 2cm）和羊水过多（AFI &gt; 24cm 或最大深度 &gt; 8cm）的诊断标准、常见原因（胎盘功能减退 / 胎儿畸形 / 糖尿病 / 胎膜早破）及分层处理方案。</p>
      <div class="highlight">📌 关键理解：羊水量随孕周动态变化，孕 38 周达峰值约 1000ml；80% 轻度羊水过多是特发性的，无需处理；羊水过少与喝水多少无关，孕晚期多为胎盘功能减退信号；羊水临界减少不必恐慌，多不影响顺产。</div>
      <div class="action">✅ 行动项：羊水减少时回忆有无阴道持续/阵发性流液（警惕胎膜早破）；羊水过多时筛查妊娠糖尿病；中重度羊水异常需评估胎儿畸形（泌尿系统/消化道）和胎盘功能；出现阵发性水样分泌物难以分辨时及时就医。</div>
      <div class="pitfall">⚠️ 避坑：不要以为多喝水能增加羊水（每日 2000ml 足量即可）；不要把羊水少等同于必须剖宫产；不要忽视阵发性水样分泌物（可能是间歇性破水，易被误认为分泌物增多）。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 86 课 · 胎儿严重偏小偏大</div>

    <div class="card">
      <h3>在讲什么</h3>
      <p>超声估重原理（头围+腹围+股骨长，±400g 误差）、正常个体差异范围（10%~90% 同孕周体重）、胎儿生长受限（FGR，&lt;10% 或偏小 &gt;3 周）和巨大儿（&gt;90% 或 ≥4kg）的病因、监测与处理。</p>
      <div class="highlight">📌 关键理解：超声估重有误差，医生看重连续趋势而非单次数值；偏大偏小 1~2 周多为正常个体差异；妊娠糖尿病既可导致巨大儿，也可能损伤胎盘功能造成胎儿偏小；FGR 内因是染色体异常（查羊穿），外因是胎盘脐带因素。</div>
      <div class="action">✅ 行动项：关注胎儿生长趋势而非单次超声数据；FGR 需排查染色体异常（羊水穿刺）+ 胎心监护评估宫内安危；巨大儿风险者控制孕期体重和血糖；医生评估宫内环境不安全时遵从终止妊娠建议。</div>
      <div class="pitfall">⚠️ 避坑：不要以为多吃能催肥宝宝（大部分孕妇无营养不良）；不要觉得生个八斤半大胖娃娃是好事（增加难产、新生儿低血糖、远期代谢疾病风险）；不要仅凭一次超声结果就恐慌下结论。</div>
    </div>
  </div>

  <div class="section">
    <div class="sec-title">第 87 课 · 胎盘老化、胎盘早剥、前置胎盘</div>

    <div class="card card-red">
      <h3>在讲什么</h3>
      <p>胎盘的功能（营养输送 + 废物代谢 + 激素合成 + 免疫屏障）、超声胎盘分级的不可靠性、前置胎盘（孕 28 周后胎盘覆盖宫颈内口）和胎盘早剥（产前胎盘剥离，产科急症）的识别、危险因素与紧急处理。</p>
      <div class="highlight">📌 关键理解：胎盘分级主观性强，不是可靠临床指标，不必因「3 级」或「钙化」而焦虑；前置胎盘 90% 在孕 28 周前自行恢复；胎盘早剥是产科极重症，典型表现为腹痛 + 阴道出血 + 宫缩，需紧急剖宫产。</div>
      <div class="action">✅ 行动项：前置胎盘者避免过度劳累和各种刺激，做好剖宫产心理准备；胎盘早剥高危人群（妊高症、腹部创伤史、既往早剥史）需高度警惕；出现腹痛+阴道出血+持续宫缩三联征立即就医；不要因胎盘钙化而减少饮食中的钙摄入。</div>
      <div class="pitfall">⚠️ 避坑：不要过度在意超声胎盘分级（主观性强，非临床决策依据）；不要因胎盘钙化就减钙（二者无关）；前置胎盘不需严格卧床（只需避免过劳和刺激即可）。</div>
    </div>
  </div>

  <div class="conclusion">
    <h2>核心总结：孕期疾病治疗与护理</h2>
    <h3>三大原则</h3>
    <ul>
      <li><strong>早筛查 · 早发现：</strong>甲功、OGTT、血压监测、乙肝抗原 —— 这些筛查一个都不能省，是早期干预的窗口。</li>
      <li><strong>科学治 · 不恐慌：</strong>甲亢可治疗、糖尿病可控糖、高血压可管理、乙肝可阻断 —— 绝大多数孕期疾病有成熟的治疗方案。</li>
      <li><strong>听医嘱 · 避误区：</strong>不要自行减药/断盐/卧床/催肥，每个疾病都有精准的管理目标和常见误区，遵医嘱比道听途说可靠一万倍。</li>
    </ul>
    <h3>七课速查表</h3>
    <ul>
      <li><strong>甲功异常：</strong>孕早期 HCG 甲亢自愈 → Graves 病才用药（PTU/MMI）→ 产后首选 MMI → 桥本防产后甲减</li>
      <li><strong>妊娠糖尿病：</strong>OGTT 确诊 → 生活方式 80%+ 可控 → 不行才胰岛素 → 产后 6~12 周必复查 OGTT</li>
      <li><strong>妊高症/子痫前期：</strong>≥140/90 诊断 → 160/110 才用药 → 目标 130~150/80~100 → 重症需住院终止妊娠</li>
      <li><strong>乙肝：</strong>备孕查抗原 → DNA 高者 28~30 周抗病毒 → 顺产优先 → 新生儿 12h 内联合免疫 → 可母乳</li>
      <li><strong>羊水异常：</strong>动态变化 → 少 ≠ 必须剖 → 多喝水无用 → 80% 轻度过多特发性 → 警惕破水</li>
      <li><strong>胎儿体重：</strong>±400g 误差 → 看趋势 → 10%~90% 正常 → FGR 查染色体/胎盘 → 巨大儿控糖控体重</li>
      <li><strong>胎盘异常：</strong>分级不靠谱 → 前置胎盘 90% 自愈 → 早剥是急症（腹痛+出血+宫缩）→ 立即就医</li>
    </ul>
  </div>

  <div class="footer">丁香妈妈 · 孕期全攻略 | 07-孕期疾病治疗与护理 | 共 7 课</div>
</div>
`;

fs.mkdirSync(path.dirname(OUT), { recursive: true });
const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
