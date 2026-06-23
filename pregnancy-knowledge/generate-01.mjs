import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from '/Users/chenzhiheng/Projects/audio-workshop/svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs', 'topics', 'pregnancy', '01-发刊词与备孕.svg');

const CSS = `
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f0f9ff,#e0f2fe);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:38px;font-weight:900;background:linear-gradient(135deg,#0369a1,#0284c7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:24px;font-weight:700;color:#0369a1;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #bae6fd}
h3{font-size:19px;font-weight:700;color:#334155;margin-bottom:10px}
p{font-size:15px;line-height:1.8;color:#475569;margin-bottom:8px}
ul,ol{padding-left:20px;margin:8px 0}
li{font-size:14px;line-height:1.7;color:#475569;margin-bottom:4px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}
.tag-pink{background:#fce7f3;color:#9d174d}
.meta{margin:12px 0 20px}
.summary-line{font-size:17px;line-height:1.7;color:#0c4a6e;padding:18px 24px;background:#fff;border-radius:12px;border-left:4px solid #0284c7;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.section{margin-bottom:28px}
.sec-title{font-size:20px;font-weight:700;color:#0369a1;margin-bottom:14px;padding-left:14px;border-left:4px solid #0284c7}
.card{background:#fff;border-radius:14px;padding:28px;margin-bottom:16px;box-shadow:0 4px 16px rgba(0,0,0,0.04);border-left:4px solid #0284c7}
.card.card-green{border-left-color:#10b981}
.card h3{font-size:18px;font-weight:700;color:#0c4a6e;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#92400e;border-left:3px solid #f59e0b}
.card .pitfall{background:#fef2f2;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#991b1b;border-left:3px solid #ef4444}
.card .action{background:#eff6ff;padding:10px 14px;border-radius:8px;margin:10px 0;font-size:14px;color:#1e40af;border-left:3px solid #3b82f6}
.conclusion{background:linear-gradient(135deg,#0c4a6e,#0284c7);color:#fff;border-radius:18px;padding:32px;margin-top:28px}
.conclusion h2{font-size:24px;font-weight:800;margin-top:0;margin-bottom:14px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:17px;font-weight:700;color:rgba(255,255,255,0.9);margin:18px 0 8px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:14px}
.footer{text-align:center;color:#94a3b8;font-size:12px;padding:28px 0 12px}
`;

const body = `
<div class="container">
<h1>孕期全攻略 · 发刊词与备孕指南</h1>
<div class="meta">
  <span class="tag tag-blue">孕期知识</span>
  <span class="tag tag-pink">备孕</span>
  <span class="tag tag-orange">5节课</span>
</div>
<div class="summary-line">
  从孕前检查到备孕营养，从不孕不育判断到四种排卵监测方法——科学备孕不是焦虑的起点，而是为新生命打造最好起跑线的过程。卓正医疗16位医生联合丁香妈妈，陪你走过奇妙十月。
</div>

<div class="section">
  <h2 class="sec-title">发刊词：课程导览</h2>
  <div class="card">
    <h3>0. 奇妙的十月旅程，我们陪你一起走过 — 李达医生（大叔）</h3>
    <p>【在讲什么】卓正医疗16位医生与丁香妈妈联合推出孕期全攻略课程。主讲人李达医生（大叔）作为妇产科医生和丈夫，陪伴太太经历了孕吐20周、双子宫、顺转剖等全程，从亲历者与医生双重视角开篇。</p>
    <div class="highlight">
      <strong>关键理解：</strong><br/>
      ① 课程按两条主线编排：按孕周顺序（每4周讲检查/营养/体重控制） + 按主题独立展开（孕期不适、疾病、用药安全等），可按需跳听。<br/>
      ② 核心理念：怀孕不是生病，准妈妈不是病人。课程中听得最多的词是「可以、没问题、没影响」，而非处处受限。<br/>
      ③ 课程打磨720小时，涵盖妇产科、营养科、麻醉科、儿科、皮肤科、口腔科、运动医学科共16位资深医生。
    </div>
    <div class="action">
      <strong>行动清单：</strong>① 了解课程双主线结构，按孕周或按话题自由学习；② 记住核心理念：你是健康的准妈妈而非病人，注意即可、不必处处小心。
    </div>
    <div class="pitfall">
      <strong>避坑：</strong>网上孕期信息虽多，但有的专业晦涩难懂，有的说法各异难辨真假——本课程由16位资深医生联合制作，提供科学、专业、规范的孕期指导。
    </div>
  </div>
</div>

<div class="section">
  <h2 class="sec-title">备孕指南</h2>

  <!-- CARD 1: 备孕营养 — 来自 2. 备孕营养  备孕营养和注意事项.txt（杨伟宏医生） -->
  <div class="card">
    <h3>01. 备孕营养和注意事项 — 杨伟宏医生</h3>
    <p>【在讲什么】备孕最关键的营养补充（叶酸与碘）和饮食禁忌——提前干预比怀孕后补救有效得多。</p>
    <div class="highlight">
      <strong>关键理解：</strong><br/>
      ① <strong>叶酸：</strong>备孕前3个月开始，每天至少0.4mg，可降低50%-70%神经管畸形风险。富叶酸食物包括动物肝脏、绿叶蔬菜、豆类、牛油果、蛋奶等，但仅靠食补不够，必须吃补剂。特殊情况需增量：曾生过神经管缺陷宝宝→5mg/天，三代亲属有神经管缺陷→1mg/天。<br/>
      ② <strong>碘：</strong>孕期日需230μg（普通人的2倍），缺碘易致胎儿神经系统发育落后、早产流产。推荐含碘盐（约150μg/天）+ 每周1-2次富碘海产品（海带、紫菜、裙带菜、海鱼、贝类）。<br/>
      ③ <strong>饮食禁忌：</strong>不吃生肉（防弓形虫）；不吃大型食肉鱼类（马鲛鱼、金枪鱼、鲨鱼等含汞高）；戒酒戒烟（包括二手烟）；咖啡因每天控制在200-300mg（≈星巴克大杯拿铁）。
    </div>
    <div class="action">
      <strong>行动清单：</strong>① 提前3个月开始每天补0.4mg叶酸，持续整个孕期；② 吃含碘盐 + 每周1-2次海产品；③ 戒烟酒，咖啡因&lt;200mg/天，不喝奶茶（隐形咖啡因大户）。
    </div>
    <div class="pitfall">
      <strong>避坑：</strong>防辐射服完全没必要——电脑、手机、微波炉、电磁炉都是无害的非电离辐射。备孕不只是女性的事，准爸爸同样需要健康生活方式（但目前无证据需补叶酸）。奶茶是隐形咖啡因大户，备孕期最好不喝。推荐鱼种：青鱼、鳕鱼、鲈鱼、沙丁鱼、罗非鱼。
    </div>
  </div>

  <!-- CARD 2: 不孕不育 — 来自 3. 备孕问题  不孕不育判断及检查.txt（杨伟宏医生） -->
  <div class="card card-green">
    <h3>02. 不孕不育判断及检查 — 杨伟宏医生</h3>
    <p>【在讲什么】如何科学判断是否需要就医，以及不孕不育检查的原则与流程——不要3个月没怀上就自我怀疑。</p>
    <div class="highlight">
      <strong>关键理解：</strong><br/>
      ① <strong>时间标准：</strong>规律性生活未避孕12个月未孕即为不孕不育。6个月累积怀孕率60%-65%，12个月达80%-85%，24个月达90%-95%。不孕症发生率随年龄升高：18-35岁 10%-15%，35-39岁 23%-25%，40岁以上超30%。<strong>35岁以上尝试6个月未孕即应就诊，40岁以上直接就医。</strong><br/>
      ② <strong>夫妻同查：</strong>男性因素占26%，女性因素35%-40%，双方因素35%-40%。一旦出现怀孕困难，约一半男性会查出问题——男方精液检查是躲不掉的。<br/>
      ③ <strong>检查时机：</strong>女性基础性激素检查需月经第2-4天；男性精液常规需禁欲2-7天。男性时间更易安排，建议男方先查。
    </div>
    <div class="action">
      <strong>行动清单：</strong>① 35岁以下至少尝试12个月再就医；② 35岁以上6个月未孕即就诊，40岁以上直接找医生；③ 夫妻双方同时检查，男方先做精液常规（最简单无创，且结果决定后续治疗方案）。
    </div>
    <div class="pitfall">
      <strong>避坑：</strong>不要把3-6个月未怀孕等同于不孕不育——只是时候未到。不要只检查女方而让男方逃避——不管女方是否有问题，男方都必须查精液。不孕不育是事后诸葛亮判断，目的是避免过早进行昂贵且不舒服的检查。
    </div>
  </div>

  <!-- CARD 3: 孕前检查 / 夫妻参与 — 来自 1. 备孕检查  重视孕前检查，夫妻都要参与.txt -->
  <div class="card">
    <h3>03. 重视孕前检查，夫妻都要参与</h3>
    <p>【在讲什么】孕前检查的完整项目和重要意义——识别潜在风险并提前干预，比怀孕后补救有效得多。怀胎十月对身体是巨大考验。</p>
    <div class="highlight">
      <strong>关键理解：</strong><br/>
      ① <strong>检查内容：</strong>夫妻双方病史询问（年龄、体重、慢性病、用药、吸烟饮酒、传染病、月经情况、遗传病史等）+ 基本体格检查（血压、心肺、口腔、乳腺、甲状腺、子宫阴道）+ 实验室检查（血尿常规、肝肾功能、血糖、甲状腺功能、传染病筛查、女方宫颈癌筛查）。<br/>
      ② <strong>特殊筛查：</strong>南方地区（四川、重庆、两湖两广、海南等）夫妻双方需筛地中海贫血。备孕女性推荐检查风疹与水痘免疫力——阴性需接种疫苗后避孕3个月。风疹&水痘疫苗均为减毒活疫苗，接种相当于一次人为感染，有致畸风险。<br/>
      ③ <strong>TORCH：</strong>不推荐所有人群常规筛查——假阳性率高、解读困难。高风险人群可针对性检查：吃非全熟肉类/养猫→查弓形虫；幼师/常接触幼儿→查巨细胞病毒。<strong>养狗不会增加弓形虫感染风险。</strong>
    </div>
    <div class="action">
      <strong>行动清单：</strong>① 携带夫妻双方体检报告去看备孕咨询门诊；② 南方地区夫妻查地中海贫血；③ 查风疹/水痘抗体，阴性则接种疫苗并避孕3个月。
    </div>
    <div class="pitfall">
      <strong>避坑：</strong>有三类女性必须完善孕前检查：原有慢性疾病（糖尿病、高血压、甲状腺疾病、心脏病等）、曾有不良孕产史（多次自然流产/胎儿发育异常/孕期并发症）、有遗传病史（需做遗传咨询）。不要认为婚检或常规体检能替代孕前检查——备孕还有专门项目。
    </div>
  </div>

  <!-- CARD 4: 排卵监测 — 来自 4. 备孕方法  监测排卵 4 种方法.txt（杨伟宏医生） -->
  <div class="card card-green">
    <h3>04. 监测排卵的四种方法 — 杨伟宏医生</h3>
    <p>【在讲什么】四种排卵监测方法的原理、优劣对比与适用场景——找准排卵日是高效受孕的关键。</p>
    <div class="highlight">
      <strong>关键理解：</strong><br/>
      ① <strong>受孕窗口：</strong>排卵前5天到排卵后1天为受孕期，<strong>排卵前一天受孕率最高</strong>。精子在输卵管内可存活3-5天（个别达7天），卵子排卵后24小时内需受精，超时退化。<br/>
      ② <strong>四种方法对比：</strong><br/>
      &nbsp;&nbsp;▪ <strong>周期计算法</strong>（往回推12-14天）：最便捷但不准，易受情绪/睡眠干扰，适合周期极度规律者。<br/>
      &nbsp;&nbsp;▪ <strong>基础体温法</strong>（每日晨醒舌下温度）：排卵后体温升0.3-0.5℃，属事后诸葛亮，对同房时机无帮助，但可与周期法联合用于「对答案」。<br/>
      &nbsp;&nbsp;▪ <strong>排卵试纸</strong>（检测LH）：LH升高后24-36小时排卵。从周期第10天起每8小时测一次，看到两条线当天同房。准确率60%-70%，假阳性率7%。<br/>
      &nbsp;&nbsp;▪ <strong>B超监测</strong>（隔天检测卵泡直径）：最精准，预测误差&lt;1天。卵泡直径达18mm即成熟，隔天同房共2-3次。但费时费钱且增加心理负担。<br/>
      ③ <strong>B超适用情况：</strong>月经不规律、夫妻两地分居、一侧输卵管不正常、使用促排卵药、人工授精/试管婴儿。
    </div>
    <div class="action">
      <strong>行动清单：</strong>① 月经规律者：排卵试纸从周期第10天起每8小时测一次，看到两条线当天同房，隔天一次共2-3次；② 月经不规律或特殊需求者：B超监测；③ 一个小技巧：同房时间只让太太知道，不给先生发通知，减少男方压力。
    </div>
    <div class="pitfall">
      <strong>避坑：</strong>基础体温升高时卵已排出，对把握同房时机没有帮助。不要过分依赖手机APP预测排卵日期。不要过度频繁性生活——隔天一次即可，2-3次覆盖窗口期就够。B超监测会产生心理压力，紧张焦虑反会降低受孕概率。
    </div>
  </div>
</div>

<div class="conclusion">
  <h2>核心要点与行动清单</h2>
  <h3>三件最重要的事</h3>
  <ol>
    <li><strong>补叶酸：</strong>备孕前3个月开始，每天0.4mg（特殊情况遵医嘱增量），富含叶酸食物为辅，补剂为主，持续整个孕期。</li>
    <li><strong>把握就医时机：</strong>35岁以下规律性生活未避孕12个月未孕再就医；35岁以上缩短为6个月；40岁以上直接找医生。检查必须夫妻同时做。</li>
    <li><strong>抓准排卵时机：</strong>排卵前一天受孕率最高。月经规律者用排卵试纸从周期第10天起每日多测，看到两条线即同房。精子可等卵子3-5天，隔天一次覆盖窗口期。</li>
  </ol>
  <h3>关键认知转变</h3>
  <p>备孕不是一项考核任务，而是为新生命创造最佳起跑环境的过程。夫妻共同参与、科学面对，远比独自焦虑有效。怀孕不是生病，准妈妈不是病人——这门课想给你的不是「这不行那不能」，而是「可以、没问题、没影响」的从容与信心。</p>
  <h3>备孕核心检查清单</h3>
  <ul>
    <li>双方病史 + 体格检查 + 血尿常规/肝肾功能/血糖/甲状腺/传染病</li>
    <li>南方地区夫妻双方地中海贫血筛查</li>
    <li>女方风疹/水痘抗体检测（阴性→接种→避孕3个月）</li>
    <li>TORCH不常规查，高风险者针对性检查</li>
    <li>男方精液常规（禁欲2-7天，简单无创）</li>
  </ul>
</div>

<div class="footer">孕期全攻略 · 丁香妈妈 &amp; 卓正医疗 · 01 发刊词与备孕指南</div>
</div>
`;

// Create output directory
fs.mkdirSync(path.dirname(OUT), { recursive: true });

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
