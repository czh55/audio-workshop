#!/usr/bin/env python3
"""从 en-content/{slug}.json 提取英文可搜索文本，生成 docs/en-index.json。

索引供 docs/index.html 的英文全文搜索使用：输入英文关键词可匹配
英文标题、简介、场景讲解、英文例句与练习/纠错内容，结果卡片跳转到
对应 {slug}-en.html 的锚点。

用法：
  python3 scripts/generate_en_search_index.py     # 全量生成 docs/en-index.json
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONTENT_DIR = ROOT / "en-content"
OUT = DOCS / "en-index.json"


def _join(parts) -> str:
    if isinstance(parts, str):
        return parts.strip()
    return " ".join(str(p).strip() for p in parts if str(p).strip())


def build_entry(data: dict) -> dict:
    slug = data["slug"]
    blocks = []

    title_en = _join(data.get("title_en", ""))
    if title_en:
        blocks.append({"anchor": "", "label": "英文标题", "text": title_en})

    summary_en = _join(data.get("summary_en", ""))
    if summary_en:
        blocks.append({"anchor": "", "label": "本集英文简介", "text": summary_en})

    for scene in data.get("scenes", []):
        sid = scene.get("id", "")
        label = scene.get("title_en", "")
        parts = [scene.get("speak", "")]
        parts.extend(s.get("en", "") for s in scene.get("sentences", []))
        for p in scene.get("paraphrase", []):
            parts.extend(p.get("phrases", []))
        text = _join(parts)
        if text:
            blocks.append({"anchor": sid, "label": label or "场景讲解", "text": text})

    practice = _join(item.get("en", "") for item in data.get("practice", []))
    if practice:
        blocks.append({"anchor": "practice", "label": "Practice · 练习", "text": practice})

    pitfalls = _join(item.get("right", "") for item in data.get("pitfalls", []))
    if pitfalls:
        blocks.append({"anchor": "pitfalls", "label": "Pitfalls · 常见错误", "text": pitfalls})

    return {
        "slug": slug,
        "title_en": title_en,
        "en_page": f"{slug}-en.html",
        "blocks": blocks,
    }


def main() -> None:
    entries = []
    for json_path in sorted(CONTENT_DIR.glob("*.json")):
        data = json.loads(json_path.read_text(encoding="utf-8"))
        if not data.get("title_en"):
            print(f"⚠ 跳过（缺 title_en）: {json_path.name}")
            continue
        entries.append(build_entry(data))

    OUT.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(f"✓ {OUT.relative_to(ROOT)} ({len(entries)} 篇, {OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
