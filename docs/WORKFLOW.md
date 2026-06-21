# Blog → SVG 自动化工作流

当 Cursor Automation 通过 Webhook 收到博客 URL 后，严格按本文档逐步骤执行。**不要跳过或合并任何步骤。**

---

## 入口

Webhook payload 格式：

```json
{ "url": "https://example.com/your-blog-post" }
```

从 payload 中提取 `url` 字段。若缺失，记录错误到日志并结束。

---

## 步骤 1：抓取网页

1. 使用 `WebFetch` 工具抓取 `url` 的内容
2. 提取：标题、正文全文、作者（如有）、发布日期（如有）
3. 若 WebFetch 返回 403/404 或无正文内容，在 `docs/index.json` 中记录失败项（见步骤 5），然后结束
4. **关键**：必须完整阅读正文全文，不要跳过任何章节

---

## 步骤 2：内容分析（核心方法论）

这是整个流程最关键的步骤。按照以下**六项硬性要求**分析文章内容。

### 2.1 不罗列名词，每张卡回答五个问题

每张卡片必须包含：
- **在讲什么问题**
- **关键理解是什么**
- **和其他概念什么关系**
- **怎么落地用**
- **原文依据 / 例子**

禁止出现"XX 是 XX 的缩写"这类空洞卡片。每个要点向下追问"所以呢？"。

### 2.2 必须有落地建议

提取原文中可立刻执行的操作步骤、配置方法、命令序列。若无显式建议，从作者态度和案例中推断。

### 2.3 必须有避坑总结

主动挖掘原文中的"不要"、"注意"、"踩过的坑"、"常见误区"。没有显式避坑内容时，根据作者立场推导"什么情况下不该用这个方法"。

### 2.4 必须有选型 / 决策指南

当文章涉及多个方法/工具/方案时，生成决策对照表：什么场景选哪个、判断依据是什么、各自边界在哪。不并列介绍。

### 2.5 必须阐明方法边界

每种方法/概念要说清楚：适用场景的上限和下限——什么时候能用、什么时候超出能力范围、和相邻方法的交界线在哪。

### 2.6 必须有对比分析

两个以上概念并存时，强制做横向对比：维度 × 概念矩阵，点出关键差异。

---

## 步骤 2-2：卡片模板选用

根据文章类型，从以下六种模板中选取 3–5 种。每张卡片独立可读，有标题、有展开、有关联。

### 模板 A：概念拆解卡

```
标题：是什么 + 一句话定性
核心机制：用 2-3 句大白话解释怎么运作
关键理解：为什么这样设计（深层原因）
典型场景：什么时候用它
边界说明：什么时候不该用它
原文依据：引原文关键句
相关概念：和 X 的区别/联系
```

### 模板 B：方法/工具卡

```
方法名 + 标签（适用场景标签）
核心思路：一句话
操作步骤：1→2→3→4 流程
选型条件：什么情况下选它而非别的
避坑：原文提到的陷阱或反模式
对比相邻方法：和 Y 的关键差异
原文引用
```

### 模板 C：避坑清单卡

```
坑名：一句话描述现象
原因：为什么会踩
原文说法：作者原话
解法：怎么避免或修复
严重程度：致命 / 小心 / 可忽略
```

### 模板 D：决策 / 选型表

```
场景 | 推荐方案 | 核心理由 | 不推荐的方案 | 为什么不行
（至少覆盖 3 个不同场景）
```

### 模板 E：跨概念对比表

```
对比维度 | 概念A | 概念B | 概念C | 一句话结论
（至少 3 维度 × 2 概念）
```

### 模板 F：心法/原则卡

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

## 步骤 2-3：提取结构化信息

完成分析后，提取以下字段供后续步骤使用：

### 固定字段
- **title**：文章标题，≤80 字符
- **summary**：一句话摘要（含关键结论），≤120 字符
- **tags**：2-4 个分类标签，从固定标签池选取：
  `AI`、`前端`、`后端`、`架构`、`DevOps`、`产品`、`设计`、`性能`、`安全`、`方法论`、`趋势`、`工具`、`数据库`、`算法`、`职业生涯`、`商业`、`开源`
- **url**：原始博客链接

### 概念与关系
- **concepts**：核心概念列表，每个含 `name` + `explanation`（2-3 句话白话解释） + `boundary`（什么时候不该用）
- **concept_relations**：概念间关系，格式 `{ from, to, label }`，例如 `{ from: "微服务", to: "API Gateway", label: "统一入口" }`

### 行动与避坑
- **actions**：3-5 条可立刻执行的操作（有操作步骤，非空泛建议）
- **pitfalls**：1-3 条避坑点，每条含 `title` + `why` + `fix` + `severity`（致命/小心/可忽略）

### 选型与对比
- **decision_table**（如涉及多方案对比）：`场景 | 推荐方案 | 理由 | 不推荐方案 | 原因` 至少 3 行
- **comparison_table**（如有 ≥2 个对比概念）：`维度 | 概念A | 概念B | 一句话结论` 至少 3 行 × 2 列

### 认知转变
- **mindshift**（如有）：1-2 条，每条含 `old`（以前怎么想）+ `new`（现在怎么理解）

---

## 步骤 3：编写 SVG 生成脚本

### 3.1 脚本结构

在仓库根目录创建 `generate-{slug}.mjs` 脚本。**必须使用 `svg-auto-height.mjs` 的 `buildSvg` 函数。**

脚本模板：

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', 'YYYY-MM-DD-slug.svg');

const CSS = `/* 见下方 CSS 参考 */`;

const body = `<!-- HTML 内容：按步骤 3.2 顺序组织 -->`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
```

### 3.2 SVG 内容模块顺序

必须按以下顺序组织 HTML 内容：

1. **标题区**：文章标题 `<h1>` + 标签 `.tag` + 日期 + 原文链接
2. **一句话概括**：以"本文解决的核心问题是……"开头的醒目段落（`.highlight`）
3. **认知纠偏**（如有常见误解）：醒目样式标注
4. **概念关系图**：`.diagram` 内用 `.node` + `.arrow` 绘制节点箭头图
5. **概念拆解卡**：每个概念一张 `.card`（A 模板）
6. **选型 / 对比表**（如有 D/E 模板）
7. **避坑卡片**（C 模板）：`.pitfall` 样式
8. **心法 / 原则卡**（如有 F 模板）
9. **结论区** `.conclusion`：
   - **总结**：3-5 条核心要点
   - **行动清单**：编号列表，可立刻做的 3-5 件事
   - **关键认知转变**（如有）

### 3.3 CSS 参考（必须使用）

```css
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
h1{font-size:38px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
.tag{display:inline-block;padding:4px 12px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}
.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:24px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-left:5px solid #3b82f6}
.card h3{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.diagram{display:flex;align-items:center;justify-content:center;gap:24px;flex-wrap:wrap;padding:20px 0;background:#fff;border-radius:20px;padding:36px;margin-bottom:32px;box-shadow:0 4px 24px rgba(0,0,0,0.06)}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:160px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.actions{margin-top:24px}
.actions h3{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:12px}
.actions li{font-size:16px;line-height:1.8;color:#475569;margin-bottom:8px}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:24px}
.conclusion h2{font-size:26px;margin-bottom:16px}
.conclusion p{font-size:16px;line-height:1.8;opacity:0.95}
.conclusion li{font-size:16px;line-height:1.8;opacity:0.95;margin-bottom:6px}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
```

### 3.4 XML 避坑（重要）

- **禁止 HTML 注释中出现连续双连字符** `<!-- ... -->` 内不能有 `--`（XML 规范限制）
- **禁止裸 `<` 符号**出现在文本中（如 `<$100`），必须转义为 `&lt;`
- `buildSvg` 内置了 50% 高度缓冲，无需手动加高度

### 3.5 输出与执行

```bash
node generate-{slug}.mjs
```

文件名：`docs/YYYY-MM-DD-slug.svg`（日期为北京时间 UTC+8，slug 为标题拼音首字母缩写或英文关键词，≤30 字符，不含空格和特殊字符）

---

## 步骤 4：质量自检

生成前检查：

- [ ] 每张卡片能回答"在问什么、关键理解、怎么用"
- [ ] 至少包含 1 处落地建议（可执行的操作步骤）
- [ ] 至少包含 1 处避坑总结（不该做什么）
- [ ] 涉及多方法时有选型 / 决策表
- [ ] 每个概念都说明了适用边界
- [ ] 多概念间有对比表（如有 2+ 概念）
- [ ] 文首有概念关系图
- [ ] 结论区有三段式（总结 + 行动清单 + 认知转变）
- [ ] SVG 高度正常、XML 无错配标签

---

## 步骤 5：更新 index.json

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

若步骤 1 抓取失败或步骤 3 SVG 生成失败，记录失败项：

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

## 步骤 6：Git 提交与推送

```bash
git add docs/
git commit -m "blog: summarize {文章标题}"
git push origin main
```

- 若 push 失败（冲突），先 `git pull --rebase` 再 push
- 若仍然失败，记录错误到日志，不阻塞后续流程

---

## 步骤 7：清理

删除步骤 3 中创建的 `generate-{slug}.mjs` 临时脚本文件，完成后提交。

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
