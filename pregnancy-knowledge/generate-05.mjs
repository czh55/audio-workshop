import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from '/Users/chenzhiheng/Projects/audio-workshop/svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'topics', 'pregnancy', '05-用药护肤与破除谣言.svg');

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f5f3ff,#ede9fe);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:38px;font-weight:900;background:linear-gradient(135deg,#5b21b6,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:24px;font-weight:700;color:#5b21b6;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #ddd6fe}
h3{font-size:19px;font-weight:700;color:#334155;margin-bottom:10px}
p{font-size:15px;line-height:1.8;color:#475569;margin-bottom:8px}
ul,ol{padding-left:20px;margin:8px 0}
li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:4px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}
.meta{margin:12px 0 20px}
.summary-line{font-size:17px;line-height:1.7;color:#4c1d95;padding:18px 24px;background:#fff;border-radius:12px;border-left:4px solid #7c3aed;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.section{margin-bottom:28px}
.sec-title{font-size:20px;font-weight:700;color:#5b21b6;margin-bottom:14px;padding-left:14px;border-left:4px solid #7c3aed}
.card{background:#fff;border-radius:14px;padding:28px;margin-bottom:16px;box-shadow:0 4px 16px rgba(0,0,0,0.04);border-left:4px solid #7c3aed}
.card h3{font-size:18px;font-weight:700;color:#4c1d95;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#92400e;border-left:3px solid #f59e0b}
.card .pitfall{background:#fef2f2;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#991b1b;border-left:3px solid #ef4444}
.card .action{background:#eff6ff;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#1e40af;border-left:3px solid #3b82f6}
.conclusion{background:linear-gradient(135deg,#4c1d95,#7c3aed);color:#fff;border-radius:18px;padding:32px;margin-top:28px}
.conclusion h2{font-size:24px;font-weight:800;margin-top:0;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:17px;font-weight:700;color:rgba(255,255,255,0.9);margin:18px 0 8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:14px}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:28px 0 12px}
`;

const body = `<div class="container">
<h1>孕期用药护肤 &amp; 破除谣言</h1>
<div class="meta">
  <span class="tag tag-purple">12 孕期用药和护肤</span>
  <span class="tag tag-blue">13 破除谣言</span>
  <span class="tag tag-green">共 6 课</span>
</div>
<div class="summary-line">
  本专题涵盖孕期用药安全的两大核心场景（不知怀孕时用药 + 已知怀孕时用药），孕期护肤清洁、保湿、防晒的正确做法，以及破除饮食、症状、分娩、爱美与生活四类常见孕期谣言。核心原则：<strong>利弊权衡</strong>——用药看是否利大于弊，生活看证据而非传言。
</div>

<!-- ========== 第一部分：用药 ========== -->
<div class="section">
  <div class="sec-title">Part 1 · 孕期用药安全</div>

  <!-- 55 -->
  <div class="card">
    <h3>55. 不知道怀孕了，用药要不要紧</h3>
    <p><strong>在讲什么：</strong>不知道怀孕的情况下吃了药，如何从五个维度判断对胎儿的影响。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; 判断药物影响的五要素：用药<strong>时期</strong>、药物类型、用药途径、用药剂量、持续时间<br/>
      &bull; 用药时间分三阶段：孕 4 周前（全或无理论，要么胎停要么没事）、4-10 周（致畸敏感期）、10 周后（器官已分化但生长仍可能受影响）<br/>
      &bull; 98% 药物的致畸风险在 FDA 获批时为「待定」，医生只能给参考建议
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; 备孕期或未避孕时，就医一定告诉医生「可能已怀孕」<br/>
      &bull; 孕 4 周内用药且未发生胎停，不必过度担心<br/>
      &bull; 安全性不确定的药物，咨询医生后<strong>不要轻易选择流产</strong>
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 发生胎停迹象不要执着保胎<br/>
      &bull; 医生回复「风险很低」不代表不专业<br/>
      &bull; 孕 10 周后用药也非绝对安全
    </div>
  </div>

  <!-- 56 -->
  <div class="card">
    <h3>56. 孕期生病了，要不要用药</h3>
    <p><strong>在讲什么：</strong>已知怀孕时生病用药的核心原则与自限性疾病 / 必须用药的判断。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; 核心原则：<strong>利弊权衡（利大于弊）</strong>——不用药会怎样？用药有什么风险？<br/>
      &bull; 孕期能不用药就不用药，尤其孕早期；需要用则选最安全种类、最低有效剂量、最短治疗时长<br/>
      &bull; FDA 旧分级 A/B/C/D/X（2015 年已改为风险概述），可用「用药助手」APP 自查<br/>
      &bull; 自限性疾病（感冒、病毒性腹泻）不需要用药；流感等并发症风险高的疾病必须用药<br/>
      &bull; 局部用药优于口服：阴道给药、吸入、皮肤外用吸收剂量小，相对安全
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; 用药前与医生充分沟通，遵医嘱<br/>
      &bull; 感冒引起的严重头痛/咽痛可用<strong>对乙酰氨基酚</strong><br/>
      &bull; 孕期可用的安全抗生素：头孢、青霉素、阿奇霉素、克林霉素、阿莫西林克拉维酸钾、甲硝唑、红霉素（注意：依托红霉素除外！）
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 不要自行判断疾病是否自限性，拿不准就看医生<br/>
      &bull; 细菌感染时不要抗拒抗生素<br/>
      &bull; 不要习惯性嗓子稍疼就吃消炎药<br/>
      &bull; 不要擅自更改医生处方的用药方式
    </div>
  </div>
</div>

<!-- ========== 第二部分：护肤 ========== -->
<div class="section">
  <div class="sec-title">Part 2 · 孕期安全护肤</div>

  <!-- 57 -->
  <div class="card">
    <h3>57. 孕期安全护肤，做美丽准妈妈</h3>
    <p><strong>在讲什么：</strong>孕期清洁、保湿、防晒的正确方案，以及需慎用的成分与化妆品。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; <strong>清洁</strong>：每天早晚各 1 次，油性皮肤早晚用洁面产品，干性皮肤早上清水 + 晚上洁面；氨基酸洁面优先，皂基非绝对禁忌<br/>
      &bull; <strong>保湿</strong>：精简程序，洁面后直接用保湿乳/霜即可，不用水+精华+乳+霜全套；美白/抗衰/祛痘产品应换成纯保湿产品<br/>
      &bull; <strong>防晒</strong>：硬防晒优先（长袖长裤 + 遮阳伞 + 宽沿帽 + 墨镜），配合物理防晒霜（氧化锌/二氧化钛），避免二苯酮；外出尽量 10 点前或 16 点后<br/>
      &bull; 选无香或淡香产品，避免加重孕吐
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; 美白祛斑产品→换成单纯保湿产品<br/>
      &bull; 防晒霜首选纯物理防晒（氧化锌+二氧化钛），如接受不了泛白可选物理化学混合<br/>
      &bull; 如需化妆选粉质基础产品（粉饼/散粉），少用液体彩妆<br/>
      &bull; 美发美甲偶尔一次安全，选合规产品 + 通风环境，不建议频繁
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 禁用：维 A 酸类药膏（维 A 酸乳膏、阿达帕林、他扎罗汀）及含视黄醇/A 醇的护肤品<br/>
      &bull; 慎用：美白祛斑产品（可能含氢醌/曲酸，吸收率高；三无产品更可能含激素/重金属）<br/>
      &bull; 防晒避开有争议成分<strong>二苯酮（羟苯甲酮）</strong>——有研究认为与女婴低出生体重相关<br/>
      &bull; 不必特意买「孕妇专用」护肤品，正规合格产品即可
    </div>
  </div>
</div>

<!-- ========== 第三部分：破除谣言 ========== -->
<div class="section">
  <div class="sec-title">Part 3 · 破除孕期谣言</div>

  <!-- 58 -->
  <div class="card">
    <h3>58. 关于孕期「吃」的误区</h3>
    <p><strong>在讲什么：</strong>破除饮食数量、禁忌与「去胎毒」等常见饮食谣言。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; 「一人吃两人补」是误区：孕早期<strong>无需增加热量</strong>，孕中晚期每天仅需 +400 千卡（≈ 两盒牛奶）<br/>
      &bull; 真正不能吃的只有三类：<strong>未煮熟的食物</strong>（肉/蛋/海鲜）、<strong>未消毒的牛奶</strong>、<strong>烟酒</strong>和高汞大型深海鱼<br/>
      &bull; 咖啡因每天 ≤ 200mg（约一大杯拿铁）；注意茶、奶茶、可乐也含咖啡因<br/>
      &bull; 「去胎毒」是伪概念：鹅蛋、绿豆、老鸽汤等与新生儿湿疹无关
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; 孕期饮食三原则：<strong>营养均衡、卫生安全、不要过量</strong><br/>
      &bull; 控制体重比「多吃」更重要<br/>
      &bull; 注意隐形咖啡因：奶茶、可乐、浓茶
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 螃蟹、桂圆、山楂不会导致流产<br/>
      &bull; 辣椒、榴莲不会让宝宝「太毒」<br/>
      &bull; 不要盲目吃「去胎毒」食物
    </div>
  </div>

  <!-- 60 -->
  <div class="card">
    <h3>60. 孕期「症状」与「疾病」的误区</h3>
    <p><strong>在讲什么：</strong>破除孕吐、性别判断、医疗检查、胎心监测、糖尿病饮食等常见误区。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; 孕吐厉害 ≠ 宝宝怀得稳，与是否流产<strong>没有显著关系</strong><br/>
      &bull; 「酸儿辣女」「肚子尖圆判男女」——所有非医学性别判断都不可信<br/>
      &bull; 孕期可以安全用药、做影像检查：超声绝对安全；X 光 / MRI 有需要时也相对安全<br/>
      &bull; 摸肚子不会导致胎位不正或脐带绕颈<br/>
      &bull; <strong>胎动</strong>才是判断胎儿宫内安全的核心指标，胎心仪不能替代！<br/>
      &bull; 妊娠期糖尿病不能不吃主食，应控制量 + 选低 GI 主食（粗粮等）
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; <strong>胎动不好一定要去医院！</strong>（课程强调三遍）<br/>
      &bull; 生病别硬扛，利大于弊时遵医嘱安全用药<br/>
      &bull; 妊娠期糖尿病：控制主食量，多吃粗粮和低 GI 主食
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 不要用非医学方法判断男女<br/>
      &bull; 不要因怕影响宝宝就不看病、不吃药、不做检查<br/>
      &bull; 不要用胎心仪替代胎动监测
    </div>
  </div>

  <!-- 61 -->
  <div class="card">
    <h3>61. 关于「爱美与生活」的误区</h3>
    <p><strong>在讲什么：</strong>破除化妆护肤、运动、性生活、养宠物、电子辐射等方面的孕期谣言。</p>
    <div class="highlight">
      <strong>关键理解</strong><br/>
      &bull; 化妆护肤可以继续：选质量过硬产品，避免水杨酸和维 A 酸；不必特意买「孕妇专用」护肤品<br/>
      &bull; 染发偶尔一次安全：选正规产品 + 通风环境，但不要频繁<br/>
      &bull; <strong>适度运动被推荐</strong>，不会导致流产（先咨询医生）<br/>
      &bull; 性生活无证据增加流产/早产几率（除非有高危因素，需咨询医生）<br/>
      &bull; 宠物可以养：弓形虫更多来自生肉，注意卫生+定期免疫驱虫即可<br/>
      &bull; 手机电磁辐射无明确危害证据，<strong>防辐射服无科学依据</strong>
    </div>
    <div class="action">
      <strong>行动项</strong><br/>
      &bull; 化妆用品选正规品牌，廉价口红可能铅超标<br/>
      &bull; 运动前咨询医生，按需选孕期运动课<br/>
      &bull; 宠物保持卫生 + 定期免疫驱虫，避免接触生肉
    </div>
    <div class="pitfall">
      <strong>避坑</strong><br/>
      &bull; 不要穿防辐射服（无科学依据）<br/>
      &bull; 不要因怀孕就送走宠物<br/>
      &bull; 不要相信「孕妇不能用任何护肤品化妆品」
    </div>
  </div>
</div>

<!-- ========== 总结 ========== -->
<div class="conclusion">
  <h2>核心结论</h2>
  <h3>用药</h3>
  <p>孕 4 周前「全或无」——没胎停就没问题。4-10 周是致畸敏感期，用药必须医生评估。<strong>核心思维：利弊权衡</strong>。自限性疾病（感冒）不硬吃，该吃的病（流感、细菌感染）不硬扛。局部用药优于口服。</p>
  <h3>护肤</h3>
  <p>清洁看肤质、保湿要精简、防晒硬优先。唯一真禁忌：维 A 酸类及衍生物。美白祛斑品慎用。物理防晒霜 + 硬防晒是最佳组合。</p>
  <h3>破谣</h3>
  <p>饮食：控制体重，不盲信禁忌。症状：孕吐≠怀得稳，胎动才是安全指标。生活：化妆/护肤/美发/运动/宠物/性生活都可以正常进行，关键是选对产品、咨询医生、把握分寸。</p>
</div>

<div class="footer">
  内容来源：丁香妈妈《孕期全攻略》| 12 孕期用药和护肤 + 13 破除谣言 | 共 6 课
</div>
</div>`;

fs.mkdirSync(path.dirname(OUT), { recursive: true });
const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
