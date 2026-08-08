#!/usr/bin/env python3
"""把 docs/ 下的播客总结 SVG 批量转换为独立 HTML 版本（内容相同）。

用法：
  python3 scripts/svg-to-html.py            # 全部 docs/*.svg（排除 topics/）
  python3 scripts/svg-to-html.py foo-总结.svg
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
AUDIO = DOCS / "audio"

# 与 viewer.html / svg-auto-height.mjs 保持一致的移动端适配
MOBILE_CSS = "@media (max-width:640px){.container{padding:16px 12px!important}.container{max-width:100%!important}h1{font-size:24px!important}h2,.sec-title{font-size:18px!important}h3{font-size:16px!important}p,li{font-size:14px!important}.summary-line{font-size:15px!important;padding:14px 16px!important}.map,.card,.timeline{padding:16px!important;margin-bottom:16px!important}.map h2{font-size:18px!important}.diagram{gap:10px!important;padding:10px 0!important}.node{min-width:100px!important;padding:12px 16px!important;font-size:13px!important}.arrow{font-size:18px!important}.conclusion{padding:20px!important}.footer{padding:20px 0 12px!important}}"

# 独立 HTML 页面的顶栏 + 布局修正（body 原 padding 由 .container 接管，顶栏才能贴顶）
PAGE_CSS = """\
.html-toolbar{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:16px;padding:12px 20px;background:rgba(248,250,252,.92);backdrop-filter:blur(8px);border-bottom:1px solid #e2e8f0;font-family:"PingFang SC","Microsoft YaHei",sans-serif}
.html-toolbar .back-link{font-size:14px;color:#3b82f6;text-decoration:none;white-space:nowrap;font-weight:600}
.html-toolbar .back-link:hover{text-decoration:underline}
.html-toolbar-title{flex:1;font-size:14px;font-weight:600;color:#1e293b;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.html-toolbar .html-audio{width:260px;height:36px;border-radius:8px}
       .html-toolbar .html-svg-link{font-size:13px;color:#64748b;text-decoration:none;white-space:nowrap}
       .html-toolbar .html-svg-link:hover{color:#3b82f6;text-decoration:underline}
       .html-toolbar .html-en-link{font-size:13px;color:#0d686c;text-decoration:none;white-space:nowrap;font-weight:600;padding:4px 10px;border:1px solid #99c6c0;border-radius:99px;background:#f0faf6}
       .html-toolbar .html-en-link:hover{color:#3b82f6;border-color:#3b82f6}
       @media (max-width:640px){
  .html-toolbar{flex-wrap:wrap;gap:10px;padding:10px 12px}
  .html-toolbar-title{flex-basis:100%;order:-1;font-size:13px}
  .html-toolbar .html-audio{width:100%}
}
"""


def extract_inner(svg_text: str) -> str:
    m = re.search(
        r'<div xmlns="http://www.w3.org/1999/xhtml">(.*?)</div>\s*</foreignObject>',
        svg_text, re.S,
    )
    if not m:
        raise ValueError("无法解析 foreignObject")
    return m.group(1)


def split_css_body(inner: str) -> tuple[str, str]:
    sm = re.search(r"<style>(.*?)</style>", inner, re.S)
    css = sm.group(1) if sm else ""
    body = re.sub(r"<style>.*?</style>", "", inner, flags=re.S).strip()
    return css, body


def extract_title(html: str) -> str:
    m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    if not m:
        return ""
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()


def svg_to_audio_path(svg_name: str) -> Path:
    stem = re.sub(r"-(?:播客)?总结(?=\.svg$)", "", svg_name, flags=re.I)
    stem = re.sub(r"\.svg$", "", stem)
    return AUDIO / f"{stem}.mp3"


def build_html(css: str, body: str, title: str, svg_name: str) -> str:
    audio = svg_to_audio_path(svg_name)
    has_audio = audio.exists()
    audio_html = (
        f'<audio controls preload="metadata" class="html-audio" '
        f'src="audio/{audio.name}">您的浏览器不支持音频播放</audio>'
        if has_audio
        else ""
    )
    svg_href = svg_name.replace(" ", "%20")
    en_stem = re.sub(r"-(?:播客)?总结(?=\.svg$)", "", svg_name, flags=re.I)
    en_stem = re.sub(r"\.svg$", "", en_stem)
    en_html = f"{en_stem}-en.html"
    en_link = (
        f'<a class="html-en-link" href="{en_html}" target="_blank">EN 双语版 ↗</a>'
        if (DOCS / en_html).exists()
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{css}
{PAGE_CSS}
body{{padding:0!important;margin:0!important}}
.container{{padding:48px 60px}}
{MOBILE_CSS}
</style>
</head>
<body>
<div class="html-toolbar">
  <a class="back-link" href="index.html">← 返回首页</a>
  <div class="html-toolbar-title">{title}</div>
  {audio_html}
  {en_link}
  <a class="html-svg-link" href="viewer.html?f={svg_href}" target="_blank">SVG 版 ↗</a>
</div>
{body}
</body>
</html>
"""


def convert(svg_path: Path) -> bool:
    svg_text = svg_path.read_text(encoding="utf-8")
    inner = extract_inner(svg_text)
    css, body = split_css_body(inner)
    title = extract_title(body)
    out = svg_path.with_suffix(".html")
    out.write_text(build_html(css, body, title, svg_path.name), encoding="utf-8")
    print(f"✓ {out.name} ({out.stat().st_size // 1024} KB, {'有音频' if svg_to_audio_path(svg_path.name).exists() else '无音频'})")
    return True


def find_svg_files() -> list[Path]:
    return sorted(p for p in DOCS.glob("*.svg") if p.is_file())


def main():
    args = sys.argv[1:]
    if args:
        cwd = Path.cwd()
        targets = [Path(a) if Path(a).is_absolute() else cwd / a for a in args]
    else:
        targets = find_svg_files()

    ok = 0
    for p in targets:
        if not p.exists():
            print(f"✗ 不存在: {p}")
            continue
        try:
            if convert(p):
                ok += 1
        except Exception as e:
            print(f"✗ {p.name}: {e}")
    print(f"\n完成: {ok}/{len(targets)}")
    sys.exit(0 if ok == len(targets) else 1)


if __name__ == "__main__":
    main()
