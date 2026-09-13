# audio-workshop

播客 → SVG 知识总结长图 + 静态站点的内容流水线。无后端、无数据库，产物是 `docs/` 下的静态文件（GitHub Pages 部署）。完整流程见 `docs/WORKFLOW.md`。

## Cursor Cloud specific instructions

服务与常用命令（标准命令已在 `docs/WORKFLOW.md` 中，勿重复照抄）：

- 生成 SVG 长图：`node generate-{slug}.mjs`（脚本须 `import { buildSvg } from './svg-auto-height.mjs'`）。`generate-{slug}.mjs` 是一次性脚本，用完即删，勿提交。
- 生成语音旁白：`python3 scripts/generate_svg_audio.py docs/{slug}-总结.svg`（`--missing` 批量补全）。
- 本地预览站点：`python3 -m http.server 8000 --directory docs`，浏览器打开 `http://localhost:8000/`（首页 `index.html`，单篇 `viewer.html?f={slug}-总结.svg`）。

非显而易见的注意事项：

- 没有 `package.json`／`node_modules`：所有 `.mjs` 只用 Node 内置模块 + 原生 `fetch`/`WebSocket`，无需 `npm install`。Node 需 v18+（当前环境 v22）。
- 没有 lint/test/build 流程。「构建」= 运行生成脚本产出 SVG；「运行」= 起静态服务器预览 `docs/`。
- `svg-auto-height.mjs` 的 `buildSvg` 用无头 Chrome 经 CDP 实测高度，Chrome 缺失时回退到 `estimateHeightFromHtml()`。本环境 Chrome 在 `/usr/local/bin/google-chrome`，会走 CDP 精确测高。设 `SVG_MEASURE_DEBUG=1` 可打印 CDP 错误。
- 已知：`estimateHeightFromHtml()` 回退路径存在 bug（`olItems is not iterable`），仅在无 Chrome 时触发；有 Chrome 时主路径（CDP）正常，不受影响。
- `edge-tts` 语音合成需外网访问微软 Edge TTS 服务器；多段合成的拼接依赖 `ffmpeg`（本环境 `/usr/bin/ffmpeg` 可用）。`pip` 安装的 `edge-tts` CLI 落在 `~/.local/bin`（不在 PATH，但脚本用的是 Python 模块，无影响）。
- 数据存于 JSON：`docs/index.json`（首页时间轴/日历按条目 `date` 字段分组，非文件时间）、`docs/topics.json`。
- 发布：GitHub Pages 从 `main` 分支 `docs/` 部署，仅推送到 `main` 才会展示（见 `docs/WORKFLOW.md` Step 9）。`.gitignore` 会忽略原始音频与转录稿，勿提交测试用的临时 SVG/MP3。
