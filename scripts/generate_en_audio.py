#!/usr/bin/env python3
"""根据 en-content/{slug}.json 生成英文朗读 MP3（edge-tts en-US）。

产出（与 generate_en_html.py 的 data-audio 路径一致）：
  docs/audio/en/{slug}/s{N}.mp3            场景整段朗读（scene.speak）
  docs/audio/en/{slug}/s{N}-{idx:02d}.mp3  逐句英文朗读（scene.sentences[].en）
  docs/audio/en/{slug}/practice-{idx}.mp3  练习句朗读（practice[].en）

用法：
  python3 scripts/generate_en_audio.py supermarket-choice
  python3 scripts/generate_en_audio.py --all
"""
from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONTENT_DIR = ROOT / "en-content"
EN_VOICE = "en-US-JennyNeural"
MAX_CHUNK_LEN = 2000


def split_text(text: str, max_len: int = MAX_CHUNK_LEN) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
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


async def synthesize_speech(text: str, output_path: Path, voice: str) -> bool:
    chunks = split_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if len(chunks) == 1:
        await _synthesize_chunk(chunks[0], output_path, voice)
        return output_path.exists()

    temp_files: list[Path] = []
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


async def generate_scene(slug: str, scene: dict, voice: str) -> tuple[bool, bool]:
    base = DOCS / "audio" / "en" / slug
    base.mkdir(parents=True, exist_ok=True)
    sid = scene["id"]

    scene_ok = True
    if scene.get("speak"):
        out = base / f"{sid}.mp3"
        if out.exists():
            print(f"  (skip) {out.relative_to(ROOT)}")
        else:
            scene_ok = await synthesize_speech(scene["speak"], out, voice)
            print(f"  {'✓' if scene_ok else '✗'} {out.relative_to(ROOT)}")

    sent_ok = True
    for i, s in enumerate(scene.get("sentences", []), 1):
        if not s.get("en"):
            continue
        out = base / f"{sid}-{i:02d}.mp3"
        if out.exists():
            continue
        if not await synthesize_speech(s["en"], out, voice):
            sent_ok = False
            print(f"  ✗ FAIL {out.relative_to(ROOT)}")
    return scene_ok, sent_ok


async def generate_practice(slug: str, practice: list[dict], voice: str) -> bool:
    base = DOCS / "audio" / "en" / slug
    base.mkdir(parents=True, exist_ok=True)
    ok = True
    for i, it in enumerate(practice):
        if not it.get("en"):
            continue
        out = base / f"practice-{i}.mp3"
        if out.exists():
            print(f"  (skip) {out.relative_to(ROOT)}")
            continue
        if await synthesize_speech(it["en"], out, voice):
            print(f"  ✓ {out.relative_to(ROOT)}")
        else:
            ok = False
            print(f"  ✗ FAIL {out.relative_to(ROOT)}")
    return ok


async def generate_for_slug(slug: str) -> bool:
    json_path = CONTENT_DIR / f"{slug}.json"
    if not json_path.exists():
        print(f"✗ 缺少内容文件: {json_path}")
        return False
    data = json.loads(json_path.read_text(encoding="utf-8"))
    voice = data.get("voice", EN_VOICE)
    scenes = data.get("scenes", [])

    print(f"\n📢 {slug}: {len(scenes)} 场景")
    results = await asyncio.gather(
        *(generate_scene(slug, s, voice) for s in scenes)
    )
    scene_ok = all(r[0] for r in results)
    sent_ok = all(r[1] for r in results)

    practice_ok = True
    if data.get("practice"):
        practice_ok = await generate_practice(slug, data["practice"], voice)

    total = sum(len(s.get("sentences", [])) for s in scenes)
    print(f"  场景 {sum(1 for r in results if r[0])}/{len(scenes)} · 句子 done · 练习 {'✓' if practice_ok else '✗'}")
    return scene_ok and sent_ok and practice_ok


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    slugs = sorted(p.stem for p in CONTENT_DIR.glob("*.json")) if args[0] == "--all" else args

    ok = 0
    for slug in slugs:
        if asyncio.run(generate_for_slug(slug)):
            ok += 1
    print(f"\n完成: {ok}/{len(slugs)}")
    sys.exit(0 if ok == len(slugs) else 1)


if __name__ == "__main__":
    main()
