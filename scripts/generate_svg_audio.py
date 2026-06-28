#!/usr/bin/env python3
"""
从 SVG 总结提取结构化旁白，用 edge-tts 合成自然中文语音（与 daily-algo 同款）。

用法：
  python3 scripts/generate_svg_audio.py docs/2ndstreet_japan_used_clothing-总结.svg
  python3 scripts/generate_svg_audio.py --all              # 全部播客总结
  python3 scripts/generate_svg_audio.py --missing          # 仅缺 MP3 的
"""

import asyncio
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
AUDIO_DIR = DOCS / "audio"

DEFAULT_VOICE = "zh-CN-XiaoxiaoNeural"
MAX_CHUNK_LEN = 2000


def strip_html(html: str) -> str:
    if not html:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"</p>\s*<p[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"</(?:p|div|h\d|li|tr)>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def svg_to_audio_path(svg_path: Path) -> Path:
    rel = svg_path.relative_to(DOCS)
    stem = rel.stem
    if stem.endswith("-总结"):
        stem = stem[:-3]
    return AUDIO_DIR / rel.parent / f"{stem}.mp3"


def parse_svg_html(svg_path: Path) -> str:
    text = svg_path.read_text(encoding="utf-8")
    m = re.search(
        r'<div xmlns="http://www.w3.org/1999/xhtml">(.*?)</div>\s*</foreignObject>',
        text,
        re.S,
    )
    if not m:
        raise ValueError(f"无法解析 SVG foreignObject: {svg_path}")
    return m.group(1)


def extract_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    return strip_html(m.group(1)) if m else ""


def extract_tags(html: str) -> list[str]:
    tags = []
    for m in re.finditer(r'<span class="tag[^"]*">(.*?)</span>', html, re.S | re.I):
        t = strip_html(m.group(1))
        if t:
            tags.append(t)
    return tags[:4]


def extract_summary(html: str) -> str:
    m = re.search(r'<div class="summary-line"[^>]*>(.*?)</div>', html, re.S | re.I)
    return strip_html(m.group(1)) if m else ""


def extract_timeline(html: str) -> list[str]:
    items = []
    block = re.search(r'<div class="timeline"[^>]*>(.*?)</div>\s*(?=<div class="(?:map|correction|section|card|conclusion)|\Z)', html, re.S | re.I)
    if not block:
        return items
    for m in re.finditer(r'<div class="timeline-item"[^>]*>(.*?)</div>', block.group(1), re.S | re.I):
        time_m = re.search(r'timeline-time[^>]*>(.*?)</span>', m.group(1), re.S | re.I)
        text_m = re.search(r'timeline-text[^>]*>(.*?)</span>', m.group(1), re.S | re.I)
        if time_m and text_m:
            items.append(f"{strip_html(time_m.group(1))}，{strip_html(text_m.group(1))}")
    return items


def extract_sections(html: str) -> list[tuple[str, list[str]]]:
    """按 .section 或大块 .card 提取章节"""
    sections: list[tuple[str, list[str]]] = []

    # 核心脉络 / 认知纠偏
    for cls, label in [("map", "核心脉络"), ("correction", "认知纠偏")]:
        m = re.search(rf'<div class="{cls}"[^>]*>(.*?)</div>\s*(?=<div class="(?:map|correction|section|card|conclusion)|\Z)', html, re.S | re.I)
        if m:
            parts = []
            for tag in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", m.group(1), re.S | re.I):
                parts.append(strip_html(tag.group(1)))
            for tag in re.finditer(r"<p[^>]*>(.*?)</p>", m.group(1), re.S | re.I):
                t = strip_html(tag.group(1))
                if t:
                    parts.append(t)
            if parts:
                sections.append((label, parts))

    # 按 section 分块
    for sec in re.finditer(
        r'<div class="section"[^>]*>(.*?)</div>\s*(?=<div class="(?:section|card card|conclusion)|\Z)',
        html,
        re.S | re.I,
    ):
        block = sec.group(1)
        title_m = re.search(r'class="sec-title"[^>]*>(.*?)</h2>', block, re.S | re.I)
        sec_title = strip_html(title_m.group(1)) if title_m else "正文"

        parts: list[str] = []
        for card in re.finditer(r'<div class="card[^"]*"[^>]*>(.*?)</div>\s*(?=<div class="card|<div class="section|\Z)', block, re.S | re.I):
            card_html = card.group(1)
            h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", card_html, re.S | re.I)
            if h3_m:
                parts.append(strip_html(h3_m.group(1)))
            for p in re.finditer(r"<p[^>]*>(.*?)</p>", card_html, re.S | re.I):
                t = strip_html(p.group(1))
                if t:
                    parts.append(re.sub(r"^(核心机制|关键理解|典型场景|原因|解法|严重程度|为什么重要|适用边界|怎么落地)[：:]\s*", r"\1，", t))
            for cls in ["quote", "highlight", "pitfall", "action", "relation"]:
                for q in re.finditer(rf'<div class="{cls}"[^>]*>(.*?)</div>', card_html, re.S | re.I):
                    t = strip_html(q.group(1))
                    if t:
                        parts.append(t)

        if parts:
            sections.append((sec_title, parts))

    # 独立 card（不在 section 内）
    if not sections:
        for card in re.finditer(r'<div class="card[^"]*"[^>]*>(.*?)</div>', html, re.S | re.I):
            parts = []
            h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", card.group(1), re.S | re.I)
            if h3_m:
                parts.append(strip_html(h3_m.group(1)))
            for p in re.finditer(r"<p[^>]*>(.*?)</p>", card.group(1), re.S | re.I):
                t = strip_html(p.group(1))
                if t:
                    parts.append(t)
            if parts:
                sections.append(("要点", parts))

    # 结论区
    m = re.search(r'<div class="conclusion"[^>]*>(.*?)</div>', html, re.S | re.I)
    if m:
        parts = []
        for li in re.finditer(r"<li[^>]*>(.*?)</li>", m.group(1), re.S | re.I):
            t = strip_html(li.group(1))
            if t:
                parts.append(t)
        for p in re.finditer(r"<p[^>]*>(.*?)</p>", m.group(1), re.S | re.I):
            t = strip_html(p.group(1))
            if t:
                parts.append(t)
        if parts:
            sections.append(("总结与行动", parts))

    return sections


def _ordinal(n: int) -> str:
    names = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
    if 1 <= n <= len(names):
        return f"第{names[n - 1]}"
    return f"第{n}"


def estimate_duration_label(char_count: int) -> str:
    minutes = char_count / 280
    low = max(1, int(minutes))
    high = max(low, int(minutes + 0.99))
    return f"约 {low} 分钟" if low == high else f"约 {low} 到 {high} 分钟"


def build_narration_script(svg_path: Path) -> str:
    html = parse_svg_html(svg_path)
    title = extract_title(html)
    tags = extract_tags(html)
    summary = extract_summary(html)
    timeline = extract_timeline(html)
    sections = extract_sections(html)

    body_parts: list[str] = []

    if summary:
        body_parts.append(f"一句话概括。{summary}")

    if timeline:
        body_parts.append("关键时间轴如下。" + "。".join(timeline))

    for i, (sec_title, parts) in enumerate(sections, 1):
        body_parts.append(f"接下来，{_ordinal(i)}部分，{sec_title}。")
        body_parts.extend(parts)

    body_text = "\n\n".join(p.strip() for p in body_parts if p.strip())
    body_text = body_text.replace("→", "，得到").replace("=>", "等于")
    body_text = re.sub(r"`([^`]+)`", r"\1", body_text)

    tag_str = "、".join(tags) if tags else "播客"
    section_count = len(sections) + (1 if timeline else 0) + (1 if summary else 0)
    duration = estimate_duration_label(len(body_text) + 200)

    intro = (
        f"欢迎收听知识总结语音讲解。本期主题，{title}。"
        f"标签包括{tag_str}。"
        f"本次讲解预计时长 {duration}，共 {max(section_count, 1)} 个部分。"
        f"好，我们开始。"
    )

    outro = "讲解完毕。建议对照页面上的图表和代码动手实践。祝学习顺利！"
    return f"{intro}\n\n{body_text}\n\n{outro}"


def split_text(text: str, max_len: int = MAX_CHUNK_LEN) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks = []
    current = ""
    for para in text.split("\n\n"):
        if len(para) > max_len:
            if current:
                chunks.append(current.strip())
                current = ""
            for i in range(0, len(para), max_len):
                chunks.append(para[i : i + max_len])
            continue
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks


async def _synthesize_chunk(text: str, output: Path, voice: str):
    import edge_tts

    communicate = edge_tts.Communicate(text, voice)
    await asyncio.wait_for(communicate.save(str(output)), timeout=120)


def _concat_mp3(files: list[Path], output: Path):
    list_file = output.parent / f".concat_{output.stem}.txt"
    try:
        with open(list_file, "w", encoding="utf-8") as f:
            for p in files:
                f.write(f"file '{p.resolve()}'\n")
        subprocess.run(
            [
                "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                "-i", str(list_file), "-c", "copy", str(output),
            ],
            check=True,
            capture_output=True,
        )
    finally:
        if list_file.exists():
            list_file.unlink()


async def synthesize_speech(text: str, output_path: Path, voice: str = DEFAULT_VOICE) -> bool:
    chunks = split_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if len(chunks) == 1:
        await _synthesize_chunk(chunks[0], output_path, voice)
        return output_path.exists()

    temp_files = []
    try:
        for i, chunk in enumerate(chunks):
            tmp = output_path.parent / f".tmp_{output_path.stem}_{i}.mp3"
            await _synthesize_chunk(chunk, tmp, voice)
            temp_files.append(tmp)
        _concat_mp3(temp_files, output_path)
        return output_path.exists()
    finally:
        for f in temp_files:
            if f.exists():
                f.unlink()


def generate_for_svg(svg_path: Path, voice: str = DEFAULT_VOICE, force: bool = False) -> bool:
    svg_path = svg_path.resolve()
    if not svg_path.exists():
        print(f"✗ 文件不存在: {svg_path}")
        return False

    out_mp3 = svg_to_audio_path(svg_path)
    out_txt = out_mp3.with_suffix(".txt")

    if out_mp3.exists() and not force:
        print(f"○ 已存在，跳过: {out_mp3.relative_to(ROOT)}")
        return True

    try:
        script = build_narration_script(svg_path)
    except Exception as e:
        print(f"✗ 解析失败 {svg_path.name}: {e}")
        return False

    try:
        ok = asyncio.run(synthesize_speech(script, out_mp3, voice))
        if ok:
            out_txt.write_text(script, encoding="utf-8")
            size_kb = out_mp3.stat().st_size // 1024
            print(f"✓ {out_mp3.relative_to(ROOT)} ({size_kb} KB)")
        return ok
    except Exception as e:
        print(f"✗ 合成失败 {svg_path.name}: {e}")
        return False


def find_svg_files(all_topics: bool = False, pregnancy_only: bool = False) -> list[Path]:
    if pregnancy_only:
        return sorted(DOCS.glob("topics/pregnancy/*.svg"))
    files = sorted(DOCS.glob("*-总结.svg"))
    if all_topics:
        files.extend(sorted(DOCS.glob("topics/**/*.svg")))
    return files


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="从 SVG 总结生成 edge-tts 语音讲解")
    parser.add_argument("svg", nargs="?", help="SVG 文件路径")
    parser.add_argument("--all", action="store_true", help="处理全部播客总结 SVG")
    parser.add_argument("--with-topics", action="store_true", help="包含 topics/ 目录")
    parser.add_argument("--pregnancy", action="store_true", help="仅孕期全攻略专题 (topics/pregnancy/)")
    parser.add_argument("--missing", action="store_true", help="仅处理尚无 MP3 的")
    parser.add_argument("--force", action="store_true", help="覆盖已有 MP3")
    parser.add_argument("--voice", default=DEFAULT_VOICE)
    parser.add_argument("--print-script", action="store_true", help="只打印旁白稿")
    args = parser.parse_args()

    if args.print_script:
        if not args.svg:
            parser.error("需要指定 SVG 路径")
        print(build_narration_script(Path(args.svg)))
        return

    targets: list[Path] = []
    if args.svg:
        targets = [Path(args.svg)]
    elif args.all or args.missing or args.pregnancy:
        targets = find_svg_files(all_topics=args.with_topics, pregnancy_only=args.pregnancy)
        if args.missing:
            targets = [p for p in targets if not svg_to_audio_path(p).exists()]
    else:
        parser.error("请指定 SVG 路径，或使用 --all / --missing")

    ok_count = 0
    for svg in targets:
        if generate_for_svg(svg, voice=args.voice, force=args.force):
            ok_count += 1

    print(f"\n完成: {ok_count}/{len(targets)}")
    sys.exit(0 if ok_count == len(targets) else 1)


if __name__ == "__main__":
    main()
