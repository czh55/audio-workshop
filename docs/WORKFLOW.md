# Blog → SVG 自动化工作流

当 Cursor Automation 通过 Webhook 收到博客 URL 后，严格按本文档逐步骤执行。**不要跳过或合并任何步骤。**

```
Task Progress:
- [ ] 1. 抓取网页（WebFetch 获取全文）
- [ ] 2. 内容分析（六项硬性要求 + 六种卡片模板）
- [ ] 3. 编写 SVG 生成脚本（.mjs + buildSvg + 完整 CSS）
- [ ] 4. 执行脚本生成 SVG（node generate-{slug}.mjs）
- [ ] 5. 更新 index.json
- [ ] 6. Git 提交与推送
- [ ] 7. 清理临时脚本
```

---

## 入口

Webhook payload 格式：

```json
{ "url": "https://example.com/your-blog-post" }
```

从 payload 中提取 `url` 字段。若缺失，记录错误到 `docs/index.json` 并结束。

---

## Step 1：抓取网页

1. 使用 `WebFetch` 工具抓取 `url` 的内容
2. 提取：标题、正文全文、作者（如有）、发布日期（如有）
3. 若 WebFetch 返回 403/404 或无正文内容，在 `docs/index.json` 中记录失败项（见 Step 5），然后结束
4. **必须完整阅读正文全文**，不要跳过任何章节

---

## Step 2：内容分析

这是整个流程最关键的步骤。按照以下规则分析文章内容。

### 必须包含（继承 web-to-svg）

1. **不罗列名词**：每张卡片回答「在讲什么 → 关键理解 → 与其他概念关系 → 怎么用 → 原文依据」
2. **行动清单**：可立刻执行的 3-5 件事
3. **避坑总结**：原文提到的陷阱/误区/不要做的事
4. **对比分析**：多概念/观点并列时做横向对比表
5. **方法边界**：每种方法/观点的适用上下限

### 六种卡片模板（按需组合）

根据文章类型，从以下模板中选取 3–5 种。每张卡片独立可读。

**模板 A：概念拆解卡**
```
标题：是什么 + 一句话定性
核心机制：用 2-3 句大白话解释怎么运作
关键理解：为什么这样设计（深层原因）
典型场景：什么时候用它
边界说明：什么时候不该用它
原文依据：引原文关键句
相关概念：和 X 的区别/联系
```

**模板 B：方法/工具卡**
```
方法名 + 标签（适用场景标签）
核心思路：一句话
操作步骤：1→2→3→4 流程
选型条件：什么情况下选它而非别的
避坑：原文提到的陷阱或反模式
对比相邻方法：和 Y 的关键差异
原文引用
```

**模板 C：避坑清单卡**
```
坑名：一句话描述现象
原因：为什么会踩
原文说法：作者原话
解法：怎么避免或修复
严重程度：致命 / 小心 / 可忽略
```

**模板 D：决策/选型表**
```
场景 | 推荐方案 | 核心理由 | 不推荐的方案 | 为什么不行
（至少覆盖 3 个不同场景）
```

**模板 E：跨概念对比表**
```
对比维度 | 概念A | 概念B | 概念C | 一句话结论
（至少 3 维度 × 2 概念）
```

**模板 F：心法/原则卡**
```
原则：一句可记住的话
为什么重要：反面案例
原文支撑
怎么落地：具体操作
适用边界：什么情况例外
```

### 文章类型识别

| 文章类型 | 识别特征 | 优先模板 | 侧重 |
|---------|---------|---------|------|
| 技术教程 | 含代码、步骤、命令 | B(方法卡)+C(避坑)+D(选型) | 落地操作 |
| 观点/趋势文 | 含"我认为"、趋势判断 | A(概念拆解)+F(心法)+E(对比) | 认知转变 |
| 工具介绍 | 介绍某产品/工具 | B(方法卡)+D(选型)+C(避坑) | 上手路径 |
| 理论/方法论 | 含学术框架、模型 | A(概念拆解)+E(对比)+F(心法) | 边界与关系 |
| 综述/盘点 | 含列表、分类 | D(选型表)+E(对比表)+A(概念拆解) | 全景对比 |

---

## Step 3：编写 SVG 生成脚本

在仓库根目录创建 `generate-{slug}.mjs` 脚本。**必须使用 `svg-auto-height.mjs` 的 `buildSvg` 函数。**

### 脚本模板

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', 'YYYY-MM-DD-slug.svg');

const CSS = `/* 见下方完整 CSS */`;

const body = `<!-- 见下方 body 区模板 -->`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
```

### body 区模板

```html
<div class="container">

<!-- 文首区：标题 + 标签 + 一句话概括 -->
<h1>{文章标题}</h1>
<div class="meta">
  <span class="tag tag-blue">博客总结</span>
  <span class="tag tag-purple">{主题标签2}</span>
  <span class="tag tag-orange">{主题标签3}</span>
</div>
<div class="summary-line">{一句话概括}（以"本文解决的核心问题是……"开头）</div>

<!-- 认知纠偏（如有） -->
<div class="correction">
  <h3>⚠ 常见误解</h3>
  <p>{纠偏内容}</p>
</div>

<!-- 文首核心概念关系图 -->
<div class="map">
  <h2>核心脉络</h2>
  <div class="diagram"><!-- 节点+箭头 --></div>
</div>

<!-- 正文卡片区（按章节分组） -->
<div class="section">
  <h2 class="sec-title">{章节标题}</h2>

  <!-- 概念拆解卡（模板 A） -->
  <div class="card">
    <h3>{概念名称}</h3>
    <p><b>核心机制：</b>用 2-3 句大白话解释</p>
    <p><b>关键理解：</b>为什么这样设计</p>
    <p><b>典型场景：</b>什么时候用它</p>
    <div class="relation">相关概念：和 X 的区别/联系</div>
    <div class="highlight">原文依据：引原文关键句</div>
  </div>

  <!-- 方法/工具卡（模板 B） -->
  <div class="card">
    <h3>{方法名}</h3>
    <p><b>核心思路：</b>一句话</p>
    <p><b>操作步骤：</b></p>
    <ol>
      <li>步骤1</li>
      <li>步骤2</li>
      <li>步骤3</li>
      <li>步骤4</li>
    </ol>
    <div class="pitfall">避坑：原文提到的陷阱或反模式</div>
    <div class="quote">原文引用</div>
  </div>

  <!-- 避坑清单卡（模板 C） -->
  <div class="card card-orange">
    <h3>⚠ {坑名}</h3>
    <p><b>原因：</b>为什么会踩</p>
    <div class="pitfall">原文说法：作者原话</div>
    <p><b>解法：</b>怎么避免或修复</p>
    <p><b>严重程度：</b>致命 / 小心 / 可忽略</p>
  </div>
</div>

<!-- 多观点对比表（模板 D/E） -->
<div class="card">
  <h3>决策对比</h3>
  <table>
    <tr><th>场景</th><th>推荐方案</th><th>核心理由</th><th>不推荐的方案</th><th>为什么不行</th></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
  </table>
</div>

<!-- 心法/原则卡（模板 F） -->
<div class="card card-purple">
  <h3>💡 心法：{原则}</h3>
  <p><b>为什么重要：</b>反面案例</p>
  <div class="quote">原文支撑</div>
  <div class="action">怎么落地：具体操作</div>
  <p><b>适用边界：</b>什么情况例外</p>
</div>

<!-- 结论区：三段式 -->
<div class="conclusion">
  <h2>总结与行动</h2>
  <h3>核心要点</h3>
  <ul>
    <li>要点1</li>
    <li>要点2</li>
    <li>要点3</li>
  </ul>
  <h3>行动清单</h3>
  <ol>
    <li>可立刻做的具体操作1</li>
    <li>可立刻做的具体操作2</li>
    <li>可立刻做的具体操作3</li>
  </ol>
  <h3>关键认知转变</h3>
  <p>以前认为…… 现在理解了……</p>
</div>

</div>
```

### 完整 CSS（必须使用）

```css
*{margin:0;padding:0;box-sizing:border-box}
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
.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:160px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3{color:#92400e;margin-bottom:8px}
.correction p{color:#92400e;font-size:15px}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}
.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,0.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
```

### XML 避坑（重要）

- **禁止 HTML 注释中出现连续双连字符** `<!-- ... -->` 内不能有 `--`（XML 规范限制）
- **禁止裸 `<` 符号**出现在文本中（如 `<$100`），必须转义为 `&lt;`
- `buildSvg` 内置 `fixSvgXml()` 做了 `&` 转义和 `<br/>` 自闭合修复，无需手动处理
- `buildSvg` 内置 50% 高度缓冲，无需手动加高度
- `rsvg-convert` / Inkscape 不能正确渲染 foreignObject，勿用

---

## Step 4：执行脚本生成 SVG

```bash
node generate-{slug}.mjs
```

**Node 路径**：优先 `/Applications/Cursor.app/Contents/Resources/app/resources/helpers/node`。

若执行失败，尝试 `which node` 找到系统 Node 路径。

文件名：`docs/YYYY-MM-DD-slug.svg`
- `YYYY-MM-DD`：当天日期（北京时间 UTC+8）
- `slug`：标题拼音首字母缩写或英文关键词，≤30 字符，不含空格和特殊字符

---

## Step 5：质量自检

生成后检查：

- [ ] 每张卡片能回答"在问什么、关键理解、怎么用"
- [ ] 至少包含 1 处落地建议（可执行的操作步骤）
- [ ] 至少包含 1 处避坑总结（不该做什么）
- [ ] 涉及多方法时有选型/决策表
- [ ] 每个概念都说明了适用边界
- [ ] 多概念间有对比表（如有 2+ 概念）
- [ ] 文首有概念关系图
- [ ] 结论区有三段式（总结 + 行动清单 + 认知转变）
- [ ] SVG 高度正常、XML 无错配标签
- [ ] 用 file 命令确认文件是 SVG 格式，在浏览器可正常打开

---

## Step 6：更新 index.json

读取 `docs/index.json`，将新总结追加到数组开头（最新在前）。

```json
{
  "date": "YYYY-MM-DD",
  "filename": "YYYY-MM-DD-slug.svg",
  "title": "文章标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["AI", "趋势"],
  "url": "https://原始链接",
  "svg_height": 12345
}
```

若 Step 1 抓取失败或 Step 3-4 SVG 生成失败，记录失败项：

```json
{
  "date": "YYYY-MM-DD",
  "title": "（失败）原始URL省略部分",
  "summary": "处理失败",
  "tags": [],
  "url": "https://原始链接",
  "error": true,
  "error_message": "具体错误原因"
}
```

---

## Step 7：Git 提交与推送

```bash
git add docs/
git commit -m "blog: summarize {文章标题}"
git push origin main
```

- 若 push 失败（冲突），先 `git pull --rebase` 再 push
- 若仍然失败，记录错误到日志，不阻塞后续流程

---

## Step 8：清理

删除步骤 3 中创建的 `generate-{slug}.mjs` 临时脚本文件。

```bash
rm generate-{slug}.mjs
```

---

## 完成

GitHub Pages 会在推送后自动部署（约 1 分钟内生效）。

- 首页：`https://czh55.github.io/audio-workshop/`
- 直接 SVG 链接：`https://czh55.github.io/audio-workshop/YYYY-MM-DD-slug.svg`

---

## 约束

- 不修改任何非 `docs/` 目录的文件（`generate-{slug}.mjs` 除外，用完立即删除）
- 不修改 `.gitignore`
- SVG 文件大小控制在 200KB 以内
- 每个 URL 只处理一次（检查 `index.json` 中是否已存在相同 `url` 的条目）
- 严禁使用 `rsvg-convert` 或 Inkscape 渲染 SVG（它们不支持 `foreignObject`）
