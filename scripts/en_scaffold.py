#!/usr/bin/env python3
"""从中文总结 HTML 自动提取结构，生成 en-content JSON 骨架。

骨架包含：meta（slug/title/date/platform/duration/source_url）、
summary_cn、各 section 的标题与卡片要点（中文）、音频目录。
英文字段（title_en/summary_en/scenes[].title_en/context/speak/sentences[].en/note
/paraphrase/practice/pitfalls/shifts）留空，由 AI 逐篇撰写。

用法：
  python3 scripts/en_scaffold.py               # 为所有未生成 en-content 的 slug 生成骨架
  python3 scripts/en_scaffold.py supermarket-choice
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONTENT_DIR = ROOT / "en-content"
INDEX_JSON = DOCS / "index.json"


def strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<br\s*/?>", " ", html, flags=re.I)
    text = re.sub(r"</p>\s*<p[^>]*>", "。", text, flags=re.I)
    text = re.sub(r"</(?:p|div|h\d|li|tr)>", "。", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = re.sub(r"\s+", " ", text)
    return text.strip().rstrip("。")


def extract_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    return strip_html(m.group(1)) if m else ""


def extract_summary(html: str) -> str:
    m = re.search(r'<div class="summary-line"[^>]*>(.*?)</div>', html, re.S | re.I)
    return strip_html(m.group(1)) if m else ""


def extract_tags(html: str) -> list[str]:
    tags = []
    for m in re.finditer(r'<span class="tag[^>]*">(.*?)</span>', html, re.S | re.I):
        t = strip_html(m.group(1))
        if t:
            tags.append(t)
    return tags[:4]


def iter_card_inner(block: str):
    pos = 0
    while pos < len(block):
        m = re.search(r'<div class="card[^"]*"[^>]*>', block[pos:], re.I)
        if not m:
            break
        start = pos + m.end()
        depth = 1
        i = start
        while i < len(block) and depth > 0:
            nxt_open = re.search(r"<div[\s>]", block[i:], re.I)
            nxt_close = re.search(r"</div>", block[i:], re.I)
            if not nxt_close:
                break
            if nxt_open and nxt_open.start() < nxt_close.start():
                depth += 1
                i += nxt_open.end()
            else:
                depth -= 1
                i += nxt_close.end()
        if depth == 0:
            yield block[start : i - len("</div>")]
        pos = i


def extract_card_points(card: str) -> list[str]:
    points: list[str] = []
    for p in re.finditer(r"<p[^>]*>(.*?)</p>", card, re.S | re.I):
        t = strip_html(p.group(1))
        t = re.sub(r"^(核心机制|关键理解|典型场景|在讲什么|原因|解法|严重程度|为什么重要|适用边界|怎么落地|行动项|避坑|原文依据|怎么用)[：:]\s*", r"\1：", t)
        if t and len(t) > 12:
            points.append(t)
    for cls in ["quote", "highlight", "pitfall", "action", "relation", "insight"]:
        for q in re.finditer(rf'<div class="{cls}"[^>]*>(.*?)</div>', card, re.S | re.I):
            t = strip_html(q.group(1))
            if t and len(t) > 12:
                points.append(f"（引用）{t}")
    return points


def extract_scenes(html: str) -> list[dict]:
    scenes: list[dict] = []
    for block in re.split(r'<div class="section"[^>]*>', html)[1:]:
        inner = re.split(r'<div class="(?:section|conclusion)"', block, maxsplit=1, flags=re.I)[0]
        m = re.search(r'(?:<h2 class="sec-title"|<div class="sec-title")[^>]*>(.*?)</(?:h2|div)>', inner, re.S | re.I)
        if not m:
            continue
        title_cn = strip_html(m.group(1))
        if not title_cn:
            continue
        points: list[str] = []
        for card in iter_card_inner(inner):
            points.extend(extract_card_points(card))
        if not points:
            continue
        scenes.append({"id": f"s{len(scenes) + 1}", "title_cn": title_cn, "points": points[:6]})
    return scenes


def html_path_for(filename: str) -> Path:
    return DOCS / re.sub(r"\.svg$", ".html", filename, flags=re.I)


def main():
    args = sys.argv[1:]
    index = json.loads(INDEX_JSON.read_text(encoding="utf-8"))

    if args:
        targets = args
    else:
        targets = []
        for d in index:
            if d.get("error") or d.get("en"):
                continue
            filename = d.get("filename", "")
            if not filename:
                continue
            slug = re.sub(r"-(?:播客)?总结\.svg$", "", filename, flags=re.I)
            if (CONTENT_DIR / f"{slug}.json").exists():
                continue
            targets.append(slug)

    ok = 0
    for slug in targets:
        # 定位 HTML：优先标准名，其次 -播客总结 变体
        html_path = None
        for cand in [f"{slug}-总结.html", f"{slug}-播客总结.html"]:
            p = DOCS / cand
            if p.exists():
                html_path = p
                break
        if not html_path:
            print(f"✗ {slug}: 无中文 HTML")
            continue

        html = html_path.read_text(encoding="utf-8")
        entry = next((d for d in index if d.get("filename", "").replace(".svg", ".html") == html_path.name), None)
        if not entry:
            entry = next((d for d in index if re.sub(r"-(?:播客)?总结\.svg$", "", d.get("filename", ""), flags=re.I) == slug), None)

        scenes = extract_scenes(html)
        if not scenes:
            print(f"✗ {slug}: 未提取到场景")
            continue

        data = {
            "slug": slug,
            "date": entry.get("date", "") if entry else "",
            "platform": "小宇宙FM",
            "title": entry.get("title", extract_title(html)) if entry else extract_title(html),
            "title_en": "",
            "eyebrow": "Bilingual Learning · Podcast Knowledge",
            "duration": entry.get("duration", "") if entry else "",
            "source_url": entry.get("url", "") if entry else "",
            "summary_cn": extract_summary(html),
            "summary_en": "",
            "scenes": [],
            "practice": [],
            "pitfalls": [],
            "shifts": [],
            "voice": "en-US-JennyNeural",
            "audio_dir": f"audio/en/{slug}",
        }
        for s in scenes:
            data["scenes"].append({
                "id": s["id"],
                "title_cn": s["title_cn"],
                "title_en": "",
                "context": "",
                "speak": "",
                "sentences": [
                    {"cn": p, "en": "", "note": ""}
                    for p in s["points"]
                ],
                "paraphrase": [],
            })

        out = CONTENT_DIR / f"{slug}.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"✓ {out.relative_to(ROOT)}（{len(data['scenes'])} 场景，{sum(len(s['sentences']) for s in data['scenes'])} 句）")
        ok += 1

    print(f"\n完成: {ok}/{len(targets)}")
    sys.exit(0 if ok == len(targets) else 1)


if __name__ == "__main__":
    main()
