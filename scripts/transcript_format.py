#!/usr/bin/env python3
"""转录格式化：时间戳、中文标点、段落分组。"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass


PAUSE_BREAK_SEC = 1.2
MAX_PARAGRAPH_SEC = 90.0
MAX_PARAGRAPH_SEGMENTS = 12
SENTENCE_END = '。！？…'
PUNCT_NO_FORCE = SENTENCE_END + '，、；：""''）】》'


@dataclass
class Segment:
    start: float
    end: float
    text: str


def fmt_ts(seconds: float) -> str:
    total = max(0, int(seconds))
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f'{h:02d}:{m:02d}:{s:02d}'
    return f'{m:02d}:{s:02d}'


def fmt_srt_ts(seconds: float) -> str:
    ms = int(round(max(0.0, seconds) * 1000))
    h, rem = divmod(ms, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'


def normalize_punct(text: str) -> str:
    text = (text or '').strip()
    if not text:
        return text

    chinese = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    if chinese >= max(3, len(text) * 0.25):
        for en, zh in ((',', '，'), ('?', '？'), ('!', '！'), (':', '：'), (';', '；')):
            text = text.replace(en, zh)

    text = re.sub(r'([，。！？；：])\1+', r'\1', text)

    if text[-1] not in PUNCT_NO_FORCE:
        if text.endswith(('吗', '呢', '吧', '啊', '嘛', '呀', '么')):
            text += '？'
        elif len(text) >= 8:
            text += '。'
    return text


def _should_break_paragraph(prev: Segment, seg: Segment, group: list[Segment]) -> bool:
    if seg.start - prev.end >= PAUSE_BREAK_SEC:
        return True
    if group:
        duration = seg.end - group[0].start
        if duration >= MAX_PARAGRAPH_SEC:
            return True
        if len(group) >= MAX_PARAGRAPH_SEGMENTS:
            return True
    return False


def group_paragraphs(segments: list[Segment], pause_sec: float = PAUSE_BREAK_SEC) -> list[list[Segment]]:
    if not segments:
        return []
    groups: list[list[Segment]] = [[segments[0]]]
    for seg in segments[1:]:
        prev = groups[-1][-1]
        if _should_break_paragraph(prev, seg, groups[-1]):
            groups.append([seg])
        else:
            groups[-1].append(seg)
    return groups


def build_formatted_txt(segments: list[Segment]) -> str:
    blocks: list[str] = []
    for group in group_paragraphs(segments):
        start = group[0].start
        end = group[-1].end
        header = f'[{fmt_ts(start)} - {fmt_ts(end)}]'
        body = '\n'.join(normalize_punct(s.text) for s in group)
        blocks.append(f'{header}\n{body}')
    return '\n\n'.join(blocks) + '\n'


def build_srt(segments: list[Segment]) -> str:
    lines: list[str] = []
    for i, seg in enumerate(segments, 1):
        text = normalize_punct(seg.text)
        if not text:
            continue
        lines.append(str(i))
        lines.append(f'{fmt_srt_ts(seg.start)} --> {fmt_srt_ts(seg.end)}')
        lines.append(text)
        lines.append('')
    return '\n'.join(lines)


def build_vtt(segments: list[Segment]) -> str:
    lines = ['WEBVTT', '']
    for seg in segments:
        text = normalize_punct(seg.text)
        if not text:
            continue
        lines.append(f'{fmt_srt_ts(seg.start).replace(",", ".")} --> {fmt_srt_ts(seg.end).replace(",", ".")}')
        lines.append(text)
        lines.append('')
    return '\n'.join(lines)


def build_json_doc(segments: list[Segment], language: str = 'zh') -> dict:
    normalized = [Segment(s.start, s.end, normalize_punct(s.text)) for s in segments if s.text.strip()]
    return {
        'language': language,
        'text': ''.join(s.text for s in normalized),
        'segments': [
            {'start': round(s.start, 3), 'end': round(s.end, 3), 'text': s.text}
            for s in normalized
        ],
    }


def has_timestamp_format(text: str) -> bool:
    return bool(re.search(r'^\[\d{2}:\d{2}(?::\d{2})?\s*-\s*\d{2}:\d{2}', text, re.M))


def write_transcript_bundle(root, base: str, segments: list[Segment], language: str = 'zh') -> dict:
    """写入 txt / srt / vtt / json，返回统计信息。"""
    root = root if hasattr(root, 'write_text') else __import__('pathlib').Path(root)
    txt = build_formatted_txt(segments)
    srt = build_srt(segments)
    vtt = build_vtt(segments)
    doc = build_json_doc(segments, language)

    (root / f'{base}.txt').write_text(txt, encoding='utf-8')
    (root / f'{base}.srt').write_text(srt, encoding='utf-8')
    (root / f'{base}.vtt').write_text(vtt, encoding='utf-8')
    (root / f'{base}.json').write_text(
        json.dumps(doc, ensure_ascii=False, indent=2), encoding='utf-8')

    groups = group_paragraphs(segments)
    return {
        'chars': len(doc['text']),
        'segments': len(segments),
        'paragraphs': len(groups),
        'lines': len(segments),
    }
