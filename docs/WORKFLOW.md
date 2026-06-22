# 播客 → SVG 自动化工作流

当 Cursor Automation 通过 Webhook 收到小宇宙播客链接后，严格按本文档逐步骤执行。**不要跳过或合并任何步骤。**

```
Task Progress:
- [ ] 1. 浏览器提取音频 URL（CDP 获取 audio src）
- [ ] 2. 下载音频（curl -L -o）
- [ ] 3. 安装依赖（ffmpeg + openai-whisper，仅首次）
- [ ] 4. Whisper 转录（--model small --language Chinese）
- [ ] 5. 读取转录稿并总结
- [ ] 6. 生成 SVG（Node .mjs + svg-auto-height.mjs）
- [ ] 7. 更新 index.json
- [ ] 8. Git 提交并推送到 main（**必须**，Pages 才能展示）
- [ ] 9. 清理临时文件
```

---

## 入口

Webhook payload 格式：

```json
{
  "url": "https://www.xiaoyuzhoufm.com/episode/6a2be5da43a22a695582ad20",
  "date": "2026-06-22"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | 小宇宙播客链接 |
| `date` | 否 | 前端展示日期，格式 `YYYY-MM-DD`；**未提供时使用当天日期**（服务器本地时区） |

从 payload 中提取 `url` 字段。若缺失，记录错误并结束。

`date` 字段用于 Step 8 写入 `index.json`，首页按此日期分组展示（时间轴、日历打点均读取该字段，**不是**文件生成时间或播客发布时间）。

---

## Step 1：浏览器提取音频 URL

小宇宙的音频 URL 在 `<audio>` 标签内，需用浏览器打开页面提取。

```bash
# 1.1 浏览器打开页面
browser_navigate → {url}

# 1.2 CDP 提取 audio src
browser_cdp: Runtime.evaluate 执行:
document.querySelector('audio')?.src || document.querySelector('audio source')?.src

# 1.3 同时提取播客标题
browser_cdp: Runtime.evaluate 执行:
document.querySelector('.episode-title, h1')?.textContent?.trim()
```

获取到 audio_url 和 title 后进入下一步。若未找到音频链接，记录失败项并结束。

---

## Step 2：下载音频

```bash
curl -L -o "~/Projects/audio-workshop/{slug}.m4a" "{audio_url}" --progress-bar
```

- `{slug}`：从标题提取英文/拼音关键词，≤30 字符，不含空格和特殊字符
- 示例：`curl -L -o "~/Projects/audio-workshop/spacex_history_podcast.m4a" "https://media.xyzcdn.net/xxx.m4a"`

若下载失败（网络错误、403 等），重试最多 3 次。

---

## Step 3：安装依赖

仅首次运行需要，已安装则跳过：

```bash
# 检查 ffmpeg
which ffmpeg || brew install ffmpeg

# 检查 whisper
python3 -c "import whisper" 2>/dev/null || pip3 install --user openai-whisper

# 设置 PATH
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin"
```

---

## Step 4：Whisper 转录

```bash
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin"
cd ~/Projects/audio-workshop
whisper {slug}.m4a --model small --language Chinese --output_dir .
```

**模型选择**：

| 模型 | 中文质量 | 速度 | 适用 |
|------|---------|------|------|
| tiny | 一般 | 极快 | 快速预览 |
| **small** | 较好 | 中等(~1h 音频≈1.5h) | **默认** |
| medium | 很好 | 慢(~1h 音频≈4h) | 高质量需求 |

转录产物：`{slug}.txt` `{slug}.srt` `{slug}.vtt` `{slug}.json`。

---

## Step 5：读取转录稿并总结

读取 `{slug}.txt` 转录稿全文，按以下规则分析。

### 必须包含（继承 web-to-svg）

1. **不罗列名词**：每张卡片回答「在讲什么 → 关键理解 → 与其他概念关系 → 怎么用 → 原文依据」
2. **行动清单**：可立刻执行的 3-5 件事
3. **避坑总结**：原文提到的陷阱/误区/不要做的事
4. **对比分析**：多概念/观点并列时做横向对比表
5. **方法边界**：每种方法/观点的适用上下限

### 播客特有处理

- **标注时间戳关键节点**（Outline 章节）：如 `[02:15] SpaceX 早期融资困境`
- **区分「嘉宾观点」与「主持人提问」**：使用 `.speaker-guest` `.speaker-host` 标签
- **保留有争议的讨论点**，标注各方立场
- **提取关键金句**：用 `.quote` 样式框标注

---

## Step 6：生成 SVG

在仓库根目录创建 `generate-{slug}.mjs` 脚本。**必须使用 `svg-auto-height.mjs` 的 `buildSvg` 函数。**

### 脚本模板

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', '{slug}-总结.svg');

const CSS = `/* 见下方完整 CSS */`;

const body = `<!-- 见下方 body 区模板 -->`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
```

### body 区模板

```html
<div class="container">

<!-- 文首区：标题 + 标签 + 一句话概括 + 时间轴 -->
<h1>{播客标题}</h1>
<div class="meta">
  <span class="tag tag-blue">播客</span>
  <span class="tag tag-purple">{主题标签}</span>
  <span class="tag tag-orange">{时长}</span>
</div>
<div class="summary-line">{一句话概括}</div>

<!-- 关键时间轴 -->
<div class="timeline">
  <h3>关键时间轴</h3>
  <div class="timeline-item">
    <span class="timeline-time">00:00</span>
    <span class="timeline-text">开场介绍：主题引出</span>
  </div>
  <div class="timeline-item">
    <span class="timeline-time">12:30</span>
    <span class="timeline-text">核心章节1：...</span>
  </div>
  <!-- 更多时间节点 -->
</div>

<!-- 文首核心概念关系图 -->
<div class="map">
  <h2>核心脉络</h2>
  <div class="diagram"><!-- 节点+箭头 --></div>
</div>

<!-- 认知纠偏（如有） -->
<div class="correction">
  <h3>⚠ 常见误解 / 认知纠偏</h3>
  <p>{纠偏内容}</p>
</div>

<!-- 正文卡片区（按章节分组） -->
<div class="section">
  <h2 class="sec-title">{章节标题}</h2>

  <!-- 概念拆解卡（模板 A） -->
  <div class="card">
    <h3>{概念名称}</h3>
    <p><b>核心机制：</b>用 2-3 句大白话解释</p>
    <p><b>关键理解：</b>为什么这样</p>
    <p><b>典型场景：</b>什么时候用</p>
    <div class="relation">相关概念：和 X 的区别/联系</div>
    <div class="highlight">原文依据：转录稿关键句</div>
  </div>

  <!-- 嘉宾观点卡 -->
  <div class="card card-purple">
    <h3>
      <span class="speaker speaker-guest">嘉宾观点</span>
      {观点摘要}
    </h3>
    <p>{详细阐述}</p>
    <div class="quote">"{嘉宾原话}"</div>
  </div>

  <!-- 避坑清单卡（模板 C） -->
  <div class="card card-orange">
    <h3>⚠ {坑名}</h3>
    <p><b>原因：</b>为什么会踩</p>
    <div class="pitfall">嘉宾说法：{原话}</div>
    <p><b>解法：</b>怎么避免或修复</p>
    <p><b>严重程度：</b>致命 / 小心 / 可忽略</p>
  </div>
</div>

<!-- 多观点对比表（模板 D/E） -->
<div class="card">
  <h3>观点对比</h3>
  <table>
    <tr><th>维度</th><th>嘉宾观点</th><th>主流观点</th><th>一句话结论</th></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
    <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
  </table>
</div>

<!-- 心法/原则卡（模板 F） -->
<div class="card card-purple">
  <h3>💡 心法：{原则}</h3>
  <p><b>为什么重要：</b>反面案例</p>
  <div class="quote">播客金句</div>
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
    <li>要点4</li>
    <li>要点5</li>
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
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
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
.speaker{display:inline-block;font-size:13px;font-weight:600;padding:2px 10px;border-radius:12px;margin-right:8px}
.speaker-host{background:#dbeafe;color:#1e40af}
.speaker-guest{background:#ede9fe;color:#6b21a8}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,0.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
```

### 运行

```bash
node generate-{slug}.mjs
```

**Node 路径**：优先 `/Applications/Cursor.app/Contents/Resources/app/resources/helpers/node`。

### XML 避坑

- HTML 注释中禁止连续双连字符 `--`
- 文本中裸 `<` 必须转义为 `&lt;`
- `buildSvg` 已内置 `fixSvgXml()` 修复 `&` 和 `<br/>`

---

## Step 7：质量自检

- [ ] 每张卡片能回答"在问什么、关键理解、怎么用"
- [ ] 至少包含 1 处落地建议（可执行的操作步骤）
- [ ] 至少包含 1 处避坑总结（不该做什么）
- [ ] 涉及多方法时有选型/决策表
- [ ] 每个概念都说明了适用边界
- [ ] 多概念间有对比表（如有 2+ 概念）
- [ ] 文首有核心脉络关系图
- [ ] 结论区有三段式（总结 + 行动清单 + 认知转变）
- [ ] 有时间轴关键节点
- [ ] 区分了嘉宾观点与主持人提问
- [ ] SVG 高度正常、XML 无错配标签

---

## Step 8：更新 index.json

读取 `docs/index.json`，将新总结追加到数组开头。

```json
{
  "date": "YYYY-MM-DD",
  "filename": "slug-总结.svg",
  "title": "播客标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["商业", "科技"],
  "url": "https://www.xiaoyuzhoufm.com/episode/原始ID",
  "duration": "3小时01分",
  "svg_height": 12620
}
```

**字段说明**：
- `date`：展示日期 `YYYY-MM-DD`。优先使用 Webhook payload 的 `date`；未提供则用**当天日期**（`date +%Y-%m-%d`）。前端首页时间轴与日历均读取此字段
- `filename`：SVG 文件名（在 docs/ 目录下）
- `title`：播客标题
- `summary`：摘要（120 字内）
- `tags`：标签数组（2-4 个）
- `url`：原始播客链接
- `duration`：音频时长
- `svg_height`：SVG 高度像素值

若失败，记录失败项：

```json
{
  "date": "YYYY-MM-DD",
  "title": "（失败）原始URL",
  "summary": "处理失败",
  "tags": [],
  "url": "https://原始链接",
  "duration": "",
  "error": true,
  "error_message": "具体错误原因"
}
```

---

## Step 9：Git 提交与推送到 main（**必须**）

> **此步骤不可跳过。** GitHub Pages 从 `main` 分支的 `docs/` 目录部署，只有推送到 `main` 后首页才能展示新内容。

```bash
# 9.1 提交变更
git add docs/
git commit -m "podcast: summarize {播客标题}"

# 9.2 确保在 main 分支并推送（必须）
git checkout main
git pull origin main
git merge {当前工作分支}   # 若已在 main 上则跳过
git push -u origin main
```

**要求：**
- 最终变更**必须**出现在 `origin/main` 上，任务才算完成
- 禁止仅推送到 feature 分支就结束；若 Automation 在 feature 分支开发，合并到 `main` 并 push 是收尾的必做动作
- 推送前确认 `docs/index.json` 与 `docs/{slug}-总结.svg` 均已纳入提交

若 push 失败（冲突），先 `git pull --rebase origin main` 再 push。若仍然失败，记录错误并标记任务未完成。

---

## Step 10：清理

```bash
# 删除生成脚本
rm generate-{slug}.mjs

# 可选：删除原始音频文件节省空间（转录稿保留）
# rm {slug}.m4a
```

---

## 完成

变更已推送到 `main` 后，GitHub Pages 会自动部署（约 1 分钟内生效）。

- 首页：`https://chenzhiheng.cn/audio-workshop/`

**验收：** 在浏览器打开首页，确认新条目与 SVG 链接可访问；若未出现，检查是否已 push 到 `main` 而非仅停留在 feature 分支。

---

## 产出文件清单

| 文件 | 说明 |
|------|------|
| `{slug}.m4a` | 原始音频 |
| `{slug}.txt` | 纯文本转录稿 |
| `{slug}.srt` | SRT 字幕 |
| `{slug}.vtt` | WebVTT 字幕 |
| `{slug}.json` | Whisper JSON（含置信度） |
| `docs/{slug}-总结.svg` | 内容总结长图 |

---

## 约束

- 仅处理小宇宙（xiaoyuzhoufm.com）链接
- 不修改非 `docs/` 目录的文件（`generate-{slug}.mjs` 除外，用完删除）
- 不修改 `.gitignore`
- 每个 URL 只处理一次（检查 `index.json` 中是否已存在相同 `url` 的条目）
- 严禁使用 `rsvg-convert` 或 Inkscape 渲染 SVG
- **必须将产出推送到 `main` 分支**，否则 GitHub Pages 无法展示，视为任务未完成
