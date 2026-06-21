# Blog → SVG 自动化工作流

当 Cursor Automation 通过 Webhook 收到博客 URL 后，严格按本文档逐步骤执行。不要跳过或合并步骤。

---

## 入口

Webhook payload 格式：

```json
{ "url": "https://example.com/your-blog-post" }
```

从 payload 中提取 `url` 字段。如果缺失，记录错误到日志并结束。

---

## 步骤 1：抓取网页

1. 使用 `WebFetch` 工具抓取 `url` 的内容
2. 提取：标题、正文全文、作者（如有）、发布日期（如有）
3. 如果 WebFetch 失败或返回 403/404，在 `docs/index.json` 中记录失败项（见步骤 7），然后结束

---

## 步骤 2：内容分析

从抓取内容中提取以下结构化信息：

### 2.1 固定字段
- **title**：文章标题，≤80 字符
- **summary**：一句话摘要（含关键结论），≤120 字符
- **tags**：2-4 个分类标签，从固定标签池选取：
  `AI`、`前端`、`后端`、`架构`、`DevOps`、`产品`、`设计`、`性能`、`安全`、`方法论`、`趋势`、`工具`、`数据库`、`算法`、`职业生涯`、`商业`、`开源`
- **url**：原始博客链接
- **one_sentence**：本文解决的核心问题，以"本文解决的核心问题是……"开头

### 2.2 概念提取
- **concepts**：核心概念列表，每个包含 `name` + `explanation`（2-3 句话白话解释）
- **concept_relations**：概念间关系，格式 `{ from, to, label }`，例如 `{ from: "微服务", to: "API Gateway", label: "统一入口" }`

### 2.3 行动与避坑
- **actions**：3-5 条可立刻执行的操作（有操作步骤，非空泛建议）
- **pitfalls**：1-3 条避坑点，每条含 `title` + `why` + `fix`
- **decision_table**（如涉及多方案对比）：`场景 | 推荐方案 | 理由 | 不推荐方案 | 原因` 至少 3 行

### 2.4 概念对比（如有 ≥2 个对比概念）
- **comparison**：`维度 | 概念A | 概念B | 一句话结论` 至少 3 维度

### 2.5 认知转变（如有）
- **mindshift**：1-2 条，每条含 `old`（以前怎么想）+ `new`（现在怎么理解）

---

## 步骤 3：生成 SVG 文件

### 3.1 文件名
格式：`{YYYY-MM-DD}-{slug}.svg`

- `YYYY-MM-DD`：当天日期（北京时间 UTC+8）
- `slug`：标题拼音首字母缩写或英文关键词，≤30 字符，不含空格和特殊字符
- 示例：`2026-06-21-microservices-patterns.svg`

### 3.2 SVG 结构
生成一个完整的 SVG 文件，使用 `foreignObject` 内嵌 HTML/CSS。核心结构：

```html
<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="{实际高度}">
  <foreignObject width="1320" height="{实际高度}">
    <div xmlns="http://www.w3.org/1999/xhtml" style="...">
      <!-- 内容区域 -->
    </div>
  </foreignObject>
</svg>
```

### 3.3 内容模块顺序
1. **标题区**：文章标题 + 标签 + 日期 + 原文链接
2. **一句话概括**："本文解决的核心问题是……"
3. **概念关系图**：用 flex + div 绘制节点箭头图（concepts + concept_relations）
4. **概念拆解卡**：每个概念一张卡（名称 + 白话解释 + 适用场景 + 边界）
5. **选型/对比表**（如有 decision_table 或 comparison）
6. **避坑卡片**（如有 pitfalls）
7. **行动清单**：编号列表
8. **认知转变**（如有 mindshift）
9. **结论摘要**：3-5 条核心要点

### 3.4 样式参考
```css
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "PingFang SC","Microsoft YaHei",sans-serif;
  background: linear-gradient(135deg,#f8fafc,#e2e8f0);
  padding: 48px 60px;
  color: #1e293b;
  width: 1320px;
}
h1 { font-size: 38px; font-weight: 900; color: #1e40af; margin-bottom: 8px; }
.tags { margin-bottom: 20px; }
.tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; margin-right: 8px; }
.tag-blue   { background: #dbeafe; color: #1e40af; }
.tag-purple { background: #ede9fe; color: #6b21a8; }
.tag-green  { background: #d1fae5; color: #065f46; }
.tag-orange { background: #ffedd5; color: #9a3412; }
.card {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
  border-left: 5px solid #3b82f6;
}
.card h3 { font-size: 22px; font-weight: 700; color: #1e40af; margin-bottom: 12px; }
.card p { font-size: 16px; line-height: 1.8; color: #475569; margin-bottom: 10px; }
.diagram {
  display: flex; align-items: center; justify-content: center;
  gap: 24px; flex-wrap: wrap; padding: 20px 0; margin: 24px 0;
  background: #fff; border-radius: 20px; padding: 36px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.node {
  background: linear-gradient(135deg,#eff6ff,#dbeafe);
  border: 2px solid #93c5fd;
  border-radius: 16px;
  padding: 16px 24px;
  font-weight: 700; font-size: 16px; color: #1e40af;
  text-align: center;
}
.arrow { font-size: 24px; color: #94a3b8; margin: 0 4px; }
.pitfall {
  background: #fef2f2; padding: 16px; border-radius: 12px;
  margin: 12px 0; border-left: 4px solid #ef4444; color: #991b1b;
}
.highlight {
  background: #fef3c7; padding: 12px 16px; border-radius: 10px;
  margin: 12px 0; border-left: 4px solid #f59e0b; color: #92400e;
}
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 15px; }
th { background: #f1f5f9; padding: 12px 16px; text-align: left; font-weight: 700; color: #1e40af; border-bottom: 2px solid #cbd5e1; }
td { padding: 12px 16px; border-bottom: 1px solid #e2e8f0; color: #475569; vertical-align: top; }
.conclusion {
  background: linear-gradient(135deg,#1e40af,#3b82f6); color: #fff;
  border-radius: 20px; padding: 36px; margin-top: 24px;
}
.source-link { color: #3b82f6; font-size: 14px; text-decoration: none; }
```

### 3.5 高度计算
- 估算内容总高度（每个模块累加），加上 200px 缓冲
- 最小高度 1200px
- 记录最终高度

### 3.6 输出
将 SVG 文件写入 `docs/{filename}`。

---

## 步骤 4：更新 index.json

读取 `docs/index.json`，将新总结追加到数组开头（最新在前）。

```json
{
  "date": "YYYY-MM-DD",
  "filename": "YYYY-MM-DD-slug.svg",
  "title": "文章标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["AI", "趋势"],
  "url": "https://原始链接",
  "svg_height": 3500
}
```

**字段说明：**
- `date`：生成日期 YYYY-MM-DD
- `filename`：SVG 文件名
- `title`：文章标题
- `summary`：摘要（120 字内）
- `tags`：标签数组（2-4 个，从固定标签池选）
- `url`：原始博客链接
- `svg_height`：SVG 高度像素值

写入后立即 git 操作（见步骤 9）。

---

## 步骤 5：失败处理

如果任何步骤失败（WebFetch 失败、生成失败），在 `index.json` 数组中记录失败项：

```json
{
  "date": "YYYY-MM-DD",
  "title": "（失败）原始URL",
  "summary": "处理失败",
  "tags": [],
  "url": "https://原始链接",
  "error": true,
  "error_message": "具体错误原因"
}
```

失败项也会显示在前端，方便排查。

---

## 步骤 6：Git 提交与推送

```bash
git add docs/
git commit -m "blog: summarize {文章标题}"
git push origin main
```

- 如果 push 失败（冲突），先 `git pull --rebase` 再 push
- 如果仍然失败，记录错误，不阻塞后续流程

---

## 完成

GitHub Pages 会在推送后自动部署。总结链接：
`https://czh55.github.io/audio-workshop/`

---

## 约束

- 不修改任何非 `docs/` 目录的文件
- 不修改 `.gitignore`
- SVG 文件大小控制在 200KB 以内
- 每个 URL 只处理一次（检查是否已存在相同 `url` 的条目）
