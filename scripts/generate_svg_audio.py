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


def _normalize_speech_text(text: str) -> str:
    text = text.replace("&bull;", "。").replace("•", "。")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"。+", "。", text)
    return text


def _extract_sec_title(block: str) -> str:
    for pat in [
        r'<div class="sec-title"[^>]*>(.*?)</div>',
        r'<h2 class="sec-title"[^>]*>(.*?)</h2>',
        r'class="sec-title"[^>]*>(.*?)</h2>',
    ]:
        m = re.search(pat, block, re.S | re.I)
        if m:
            return _normalize_speech_text(strip_html(m.group(1)))
    return "正文"


def _iter_card_inner_html(block: str):
    """按 card 边界迭代，正确处理嵌套 div"""
    pos = 0
    while pos < len(block):
        m = re.search(r'<div class="card[^"]*"[^>]*>', block[pos:], re.I)
        if not m:
            break
        start = pos + m.end()
        depth = 1
        i = start
        while i < len(block) and depth > 0:
            next_open = re.search(r"<div[\s>]", block[i:], re.I)
            next_close = re.search(r"</div>", block[i:], re.I)
            if not next_close:
                break
            if next_open and next_open.start() < next_close.start():
                depth += 1
                i += next_open.end()
            else:
                depth -= 1
                i += next_close.end()
        if depth == 0:
            yield block[start : i - len("</div>")]
        pos = i


def _extract_card_parts(card_html: str) -> list[str]:
    parts: list[str] = []
    h3_m = re.search(r"<h3[^>]*>(.*?)</h3>", card_html, re.S | re.I)
    if h3_m:
        parts.append(_normalize_speech_text(strip_html(h3_m.group(1))))

    for p in re.finditer(r"<p[^>]*>(.*?)</p>", card_html, re.S | re.I):
        t = _normalize_speech_text(strip_html(p.group(1)))
        if t:
            t = re.sub(
                r"^(核心机制|关键理解|典型场景|在讲什么|原因|解法|严重程度|为什么重要|适用边界|怎么落地|行动项|避坑)[：:]\s*",
                r"\1，",
                t,
            )
            parts.append(t)

    for cls in ["quote", "highlight", "pitfall", "action", "relation"]:
        for q in re.finditer(rf'<div class="{cls}"[^>]*>(.*?)</div>', card_html, re.S | re.I):
            t = _normalize_speech_text(strip_html(q.group(1)))
            if t:
                parts.append(t)
    return parts


def _split_div_blocks(html: str, class_name: str) -> list[str]:
    """按 class 切分 div 块（跳过中间 HTML 注释）"""
    chunks = re.split(rf'<div class="{class_name}"[^>]*>', html, flags=re.I)
    return chunks[1:]


def extract_sections(html: str) -> list[tuple[str, list[str]]]:
    """按 .section / .card / .conclusion 提取章节，避免重复与 HTML 泄漏"""
    sections: list[tuple[str, list[str]]] = []

    for cls, label in [("map", "核心脉络"), ("correction", "认知纠偏")]:
        for block in _split_div_blocks(html, cls):
            inner = re.split(r'<div class="(?:map|correction|section|card|conclusion)"', block, maxsplit=1, flags=re.I)[0]
            parts: list[str] = []
            for tag in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", inner, re.S | re.I):
                t = _normalize_speech_text(strip_html(tag.group(1)))
                if t:
                    parts.append(t)
            for tag in re.finditer(r"<p[^>]*>(.*?)</p>", inner, re.S | re.I):
                t = _normalize_speech_text(strip_html(tag.group(1)))
                if t:
                    parts.append(t)
            if parts:
                sections.append((label, parts))
            break

    for block in _split_div_blocks(html, "section"):
        inner = re.split(r'<div class="(?:section|conclusion)"', block, maxsplit=1, flags=re.I)[0]
        sec_title = _extract_sec_title(inner)
        parts: list[str] = []
        for card_html in _iter_card_inner_html(inner):
            parts.extend(_extract_card_parts(card_html))
        if parts:
            sections.append((sec_title, parts))

    if not sections:
        for card_html in _iter_card_inner_html(html):
            parts = _extract_card_parts(card_html)
            if parts:
                sections.append(("要点", parts))

    for block in _split_div_blocks(html, "conclusion"):
        inner = re.split(r'<div class="footer"', block, maxsplit=1, flags=re.I)[0]
        parts: list[str] = []
        for tag in re.finditer(r"<h[23][^>]*>(.*?)</h[23]>", inner, re.S | re.I):
            t = _normalize_speech_text(strip_html(tag.group(1)))
            if t:
                parts.append(t)
        for tag in re.finditer(r"<li[^>]*>(.*?)</li>", inner, re.S | re.I):
            t = _normalize_speech_text(strip_html(tag.group(1)))
            if t:
                parts.append(t)
        for tag in re.finditer(r"<p[^>]*>(.*?)</p>", inner, re.S | re.I):
            t = _normalize_speech_text(strip_html(tag.group(1)))
            if t:
                parts.append(t)
        if parts:
            sections.append(("核心结论", parts))
        break

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
        seen: set[str] = set()
        for p in parts:
            key = p[:80]
            if key not in seen:
                seen.add(key)
                body_parts.append(p)

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
