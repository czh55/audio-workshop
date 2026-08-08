#!/usr/bin/env python3
"""根据 en-content/{slug}.json 生成双语学习型英文版 HTML（借鉴 language_paraphrase 场景式学习卡）。

用法：
  python3 scripts/generate_en_html.py supermarket-choice     # 生成 docs/{slug}-en.html
  python3 scripts/generate_en_html.py --all                  # 全部有 JSON 的
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONTENT_DIR = ROOT / "en-content"

CSS = """:root{--teal-950:#073f42;--teal-800:#0d686c;--teal-700:#0f7c80;--teal-600:#14919b;--mint-100:#dff4ec;--mint-50:#f0faf6;--ink:#183536;--muted:#607879;--line:#d7e8e2;--paper:#fff;--amber:#a85d08;--shadow:0 12px 32px rgba(7,63,66,.08)}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:24px}
body{margin:0;color:var(--ink);background:#edf7f2;font-family:Inter,"PingFang SC","Noto Sans SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.65}
button,select{font:inherit}
a{color:inherit}
.hero{color:#fff;background:radial-gradient(circle at 85% 10%,rgba(129,230,196,.24),transparent 30%),linear-gradient(125deg,#073f42,#0d7377 56%,#14919b)}
.hero-inner{width:min(1440px,100%);margin:auto;padding:44px clamp(20px,5vw,72px) 36px}
.hero-flex{display:flex;gap:clamp(18px,3vw,40px);align-items:flex-start}
.hero-cover{width:min(240px,42vw);height:auto;max-height:320px;object-fit:contain;object-position:center;border-radius:16px;border:1px solid rgba(255,255,255,.28);box-shadow:0 18px 44px rgba(0,0,0,.32);flex-shrink:0;background:rgba(255,255,255,.08)}
.hero-text{min-width:0;flex:1}
.eyebrow{margin:0 0 12px;font-size:.78rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase;opacity:.8}
h1{max-width:1020px;margin:0;font-size:clamp(1.7rem,3.6vw,3rem);line-height:1.15;letter-spacing:-.04em}
.hero-en{margin:12px 0 22px;font-size:clamp(1rem,2vw,1.25rem);opacity:.82}
.hero-meta{display:flex;flex-wrap:wrap;gap:9px;align-items:center}
.chip{border:1px solid rgba(255,255,255,.28);border-radius:99px;padding:5px 11px;font-size:.82rem;background:rgba(255,255,255,.08)}
.source-link{font-weight:750;text-decoration:none;border-bottom:1px solid rgba(255,255,255,.5)}
.toolbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-top:22px}
.toolbar label{font-size:.82rem;opacity:.82}
.toolbar select{color:#fff;background:#0a5d61;border:1px solid rgba(255,255,255,.3);border-radius:8px;padding:7px 9px}
.stop-btn{display:none;color:#fff;background:#8c3b2a;border:0;border-radius:8px;padding:8px 12px;cursor:pointer}
.stop-btn.visible{display:inline-flex}
.speech-status{min-height:1.4em;font-size:.82rem;opacity:.88}
.lang-switch{display:inline-flex;gap:6px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.28);border-radius:99px;padding:4px}
.lang-switch a{display:inline-block;padding:4px 13px;border-radius:99px;font-size:.8rem;font-weight:700;text-decoration:none;color:rgba(255,255,255,.75)}
.lang-switch a.active{background:#fff;color:var(--teal-800)}
.narration-player{margin-top:16px;padding:14px 18px;background:rgba(255,255,255,.1);border-radius:12px;border:1px solid rgba(255,255,255,.15)}
.audio-label{color:rgba(255,255,255,.88);font-size:.82rem;font-weight:700;margin:0 0 8px}
.page{width:min(1440px,100%);margin:auto;padding:28px clamp(16px,3vw,44px) 64px;display:grid;grid-template-columns:minmax(230px,280px) minmax(0,1fr);gap:30px;align-items:start}
.sidebar{position:sticky;top:20px;min-width:0}
.sidebar-box{background:rgba(255,255,255,.8);border:1px solid var(--line);border-radius:16px;padding:17px;box-shadow:var(--shadow);backdrop-filter:blur(12px)}
.sidebar h2{margin:0 0 13px;font-size:.9rem;letter-spacing:.08em;color:var(--teal-800)}
.map-link{display:grid;grid-template-columns:34px minmax(0,1fr);gap:9px;padding:10px 6px;text-decoration:none;border-top:1px solid var(--line)}
.map-link:hover b{color:var(--teal-700)}
.map-id{width:30px;height:30px;display:grid;place-items:center;border-radius:9px;color:#fff;background:var(--teal-700);font-size:.72rem;font-weight:800}
.map-link b{display:block;font-size:.78rem;line-height:1.4}
.map-link small{display:block;color:var(--muted);font-size:.67rem;line-height:1.4;margin-top:2px;overflow-wrap:anywhere}
.content{min-width:0}
.scene-card{background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:clamp(20px,3vw,34px);margin-bottom:24px;box-shadow:var(--shadow);overflow:hidden}
.scene-topline{display:flex;justify-content:space-between;gap:16px;align-items:center;margin-bottom:16px}
.scene-id{display:inline-grid;place-items:center;min-width:42px;height:30px;padding:0 10px;color:#fff;background:var(--teal-700);border-radius:8px;font-size:.78rem;font-weight:850}
.time{margin-left:10px;color:var(--muted);font-size:.82rem;font-variant-numeric:tabular-nums}
.scene-card h2{margin:0 0 2px;font-size:clamp(1.35rem,2.4vw,2rem);line-height:1.25;color:var(--teal-950)}
.scene-title-en{margin:0 0 18px;color:var(--teal-600);font-weight:700;font-size:.98rem}
.context{margin:0 0 20px;padding:12px 15px;color:#496566;background:var(--mint-50);border-left:3px solid var(--teal-600);border-radius:0 10px 10px 0;font-size:.88rem}
.context b{margin-right:10px;color:var(--teal-800)}
.sentence-list{display:grid;gap:12px}
.sentence{position:relative;display:grid;grid-template-columns:38px minmax(0,1fr);gap:12px;padding:16px;border:1px solid #e2ece8;border-radius:14px;background:#fcfefd;min-width:0}
.sentence-no{color:var(--teal-600);font-size:.76rem;font-weight:850;font-variant-numeric:tabular-nums;padding-top:4px}
.bilingual{min-width:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(14px,2vw,28px)}
.lang-block{min-width:0}
.lang-block p{margin:5px 0 0;overflow-wrap:anywhere}
.en-block{padding-left:clamp(14px,2vw,28px);border-left:1px solid var(--line)}
.en-block p{color:#0b5c60;font-weight:650}
.lang-tag{display:inline-block;color:var(--muted);font-size:.66rem;font-weight:850;letter-spacing:.12em}
.en-head{display:flex;justify-content:space-between;gap:10px;align-items:center;min-height:30px}
.note{grid-column:2;margin:1px 0 0;color:#708182;font-size:.78rem}
.note span{margin-right:7px;color:var(--amber);font-weight:750}
.speak-btn{display:inline-flex;align-items:center;gap:7px;border:1px solid #b8d9d1;border-radius:9px;padding:7px 11px;color:var(--teal-800);background:#f5fbf8;cursor:pointer;white-space:nowrap;font-size:.78rem;font-weight:750;transition:.15s ease}
.speak-btn:hover{color:#fff;background:var(--teal-700);border-color:var(--teal-700);transform:translateY(-1px)}
.speak-btn.playing{color:#fff;background:var(--teal-700);border-color:var(--teal-700)}
.speak-btn.compact{padding:4px 8px;font-size:.7rem}
.speak-btn.icon-only{padding:3px 7px;margin-left:6px}
.speak-btn.icon-only span:last-child{display:none}
.pronounce-word{display:inline;margin:0;padding:0 2px;color:inherit;background:rgba(20,145,155,.08);border:0;border-bottom:1px dashed var(--teal-600);border-radius:3px;font:inherit;font-weight:inherit;line-height:inherit;cursor:pointer}
.pronounce-word:hover,.pronounce-word:focus{color:var(--teal-950);background:#cceee4;border-bottom-style:solid;outline:3px solid rgba(20,145,155,.42);outline-offset:2px}
.pronounce-word.playing{color:#fff;background:var(--teal-700);border-bottom-color:var(--teal-700)}
.paraphrase{margin-top:18px;border-top:1px solid var(--line)}
.paraphrase summary{padding:16px 0 3px;color:var(--teal-800);cursor:pointer;font-weight:800}
.paraphrase summary span{color:var(--muted);font-size:.75rem;font-weight:500;margin-left:8px}
.paraphrase ol{margin:12px 0 0;padding-left:22px}
.paraphrase li{padding:7px 0 9px 5px}
.paraphrase li p{margin:0;font-size:.9rem;font-weight:650}
.paraphrase li small{display:block;color:var(--muted);font-size:.72rem;margin-top:2px}
.chunks{margin-top:4px;color:var(--teal-700);font-size:.78rem}
.study-section{margin:38px 0 0}
.section-heading{display:flex;align-items:baseline;gap:10px;margin:0 0 15px;color:var(--teal-950);font-size:1.35rem}
.section-heading small{color:var(--teal-600);font-size:.78rem;letter-spacing:.05em}
.study-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
.study-grid article{padding:17px;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 6px 18px rgba(7,63,66,.05);min-width:0}
.study-grid p{margin:0}
.practice-en{margin-top:9px;color:var(--teal-700);font-weight:650;overflow-wrap:anywhere}
.wrong{color:#a24831;text-decoration:line-through;overflow-wrap:anywhere}
.right{color:var(--teal-700);font-weight:750;margin:5px 0;overflow-wrap:anywhere}
.pitfalls p{color:var(--muted);font-size:.82rem}
.shifts article{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1.5fr);gap:12px;align-items:center}
.shifts b{color:var(--teal-600);font-size:1.2rem}
.shifts strong{color:var(--teal-800)}
footer{margin-top:38px;color:var(--muted);font-size:.78rem;text-align:center}
.footer-note{margin-top:6px}
@media (max-width:900px){
  .page{grid-template-columns:1fr}
  .sidebar{position:static}
  .sidebar-box{overflow-x:auto;padding:12px}
  .sidebar h2{padding-left:5px}
  .map-nav{display:flex;width:max-content;gap:8px}
  .map-link{width:240px;border:1px solid var(--line);border-radius:10px;padding:8px}
  .bilingual{grid-template-columns:1fr}
  .en-block{padding:12px 0 0;border-left:0;border-top:1px dashed var(--line)}
}
@media (max-width:620px){
  .hero-inner{padding-top:30px}
  .hero-flex{flex-direction:column;align-items:center}
  .hero-cover{width:100%;max-width:360px}
  .hero-text{text-align:center}
  .page{padding-inline:10px;gap:18px}
  .scene-card{border-radius:14px;padding:17px 13px}
  .scene-topline{align-items:flex-start}
  .scene-speak span:last-child{display:none}
  .sentence{grid-template-columns:26px minmax(0,1fr);padding:13px 10px;gap:6px}
  .note{grid-column:2}
  .study-grid{grid-template-columns:1fr}
  .shifts article{grid-template-columns:1fr;gap:5px}
  .shifts b{transform:rotate(90deg);justify-self:start}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.speak-btn{transition:none}}"""

JS = """(() => {
  let activeAudio = null;
  let activeBtn = null;
  const status = document.getElementById('speech-status');
  const stopBtn = document.getElementById('stop-speech');
  const rateSel = document.getElementById('speech-rate');

  const reset = () => {
    if (activeAudio) { activeAudio.pause(); activeAudio = null; }
    activeBtn?.classList.remove('playing');
    activeBtn = null;
    stopBtn.classList.remove('visible');
    status.textContent = '';
  };

  const playAudio = (url, btn) => {
    reset();
    const audio = new Audio(url);
    audio.playbackRate = Number(rateSel.value);
    activeAudio = audio;
    activeBtn = btn;
    btn.classList.add('playing');
    stopBtn.classList.add('visible');
    status.textContent = btn.classList.contains('scene-speak')
      ? 'Reading the whole scene…'
      : 'Reading…';

    audio.onended = () => { if (activeAudio === audio) reset(); };
    audio.onerror = () => { status.textContent = 'Audio failed to load.'; if (activeAudio === audio) reset(); };
    audio.play().catch(() => { status.textContent = 'Playback failed.'; if (activeAudio === audio) reset(); });
  };

  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-audio]');
    if (!btn) return;
    e.preventDefault();
    if (btn === activeBtn && activeAudio) { reset(); return; }
    playAudio(btn.dataset.audio, btn);
  });

  stopBtn.addEventListener('click', reset);

  const synth = window.speechSynthesis;
  const getEnglishVoice = () => {
    const voices = synth.getVoices();
    return voices.find(v => /^en-(US|GB)/i.test(v.lang))
        || voices.find(v => /^en/i.test(v.lang)) || null;
  };

  const difficultWords = new Set([
    'assortment', 'SKU', 'premium', 'margin', 'middleman', 'OEM', 'rebranding',
    'hoarding', 'PTSD', 'curation', 'repurchase', 'touchpoint', 'backlash',
    'reshuffle', 'funnel', 'anchor', 'contract', 'psychology', 'private', 'label',
    'editorial', 'familiar', 'competitors', 'authorization', 'flexibility'
  ]);

  const shouldPronounce = word => {
    const n = word.toLowerCase().replace(/^[^a-z]+|[^a-z]+$/g, '');
    return n.replace(/[^a-z]/g, '').length >= 8 || difficultWords.has(n);
  };

  const markPronounceableWords = root => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      if (node.parentElement?.closest('button, script, style')) return;
      const text = node.nodeValue;
      let m, last = 0, changed = false;
      const frag = document.createDocumentFragment();
      const re = /[A-Za-z]+(?:[-'\u2019][A-Za-z]+)*/g;
      while ((m = re.exec(text))) {
        if (!shouldPronounce(m[0])) continue;
        changed = true;
        frag.append(text.slice(last, m.index));
        const wb = document.createElement('button');
        wb.type = 'button'; wb.className = 'pronounce-word';
        wb.dataset.speak = m[0];
        wb.setAttribute('aria-label', '\\u8bfb\\u5355\\u8bcd ' + m[0]);
        wb.title = '\\u70b9\\u51fb\\u542c\\u53d1\\u97f3';
        wb.textContent = m[0];
        frag.append(wb);
        last = m.index + m[0].length;
      }
      if (!changed) return;
      frag.append(text.slice(last));
      node.replaceWith(frag);
    });
  };

  document.querySelectorAll(
    '.english, .scene-title-en, .paraphrase li p, .chunks, .practice-en, .wrong, .right, .summary-en'
  ).forEach(markPronounceableWords);

  document.addEventListener('click', e => {
    const wb = e.target.closest('.pronounce-word');
    if (!wb) return;
    e.preventDefault();
    if (!synth) return;
    synth.cancel();
    if (activeAudio) { activeAudio.pause(); activeAudio = null; }
    activeBtn?.classList.remove('playing');
    activeBtn = wb;
    wb.classList.add('playing');
    const u = new SpeechSynthesisUtterance(wb.dataset.speak);
    u.lang = 'en-US';
    u.rate = 0.88;
    const v = getEnglishVoice();
    if (v) u.voice = v;
    u.onend = () => { activeBtn?.classList.remove('playing'); activeBtn = null; };
    u.onerror = () => { activeBtn?.classList.remove('playing'); activeBtn = null; };
    synth.speak(u);
  });
})();"""


def cn_html_name(slug: str) -> str:
    return f"{slug}-总结.html"


def svg_name(slug: str) -> str:
    return f"{slug}-总结.svg"


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_scene(scene: dict, slug: str) -> str:
    sid = scene["id"]
    sentences = scene.get("sentences", [])
    audio_base = f"audio/en/{slug}/{sid}"

    sent_html = []
    for i, s in enumerate(sentences, 1):
        note = s.get("note", "")
        sent_html.append(f'''<article class="sentence">
          <div class="sentence-no">{i:02d}</div>
          <div class="bilingual">
            <div class="lang-block zh-block">
              <span class="lang-tag">中文</span>
              <p>{s["cn"]}</p>
            </div>
            <div class="lang-block en-block">
              <div class="en-head">
                <span class="lang-tag">EN</span>
                <button class="speak-btn compact" type="button" data-audio="{audio_base}-{i:02d}.mp3" aria-label="朗读本句"><span aria-hidden="true">▶</span><span>朗读本句</span></button>
              </div>
              <p class="english">{s["en"]}</p>
            </div>
          </div>
          <p class="note">{note}</p>
        </article>''')

    pars = scene.get("paraphrase", [])
    para_html = ""
    if pars:
        items = "\n".join(
            f'''<li><p>{p["intent"]}</p><div class="chunks">{p["chunks"]}</div><small>{p["usage"]}</small></li>'''
            for p in pars
        )
        para_html = f'''<details class="paraphrase">
        <summary>Paraphrase &amp; Chunks <span>{len(pars)} 组表达</span></summary>
        <ol>
          {items}
        </ol>
      </details>'''

    scene_speak_btn = (
        f'<button class="speak-btn scene-speak" type="button" data-audio="{audio_base}.mp3" aria-label="朗读整个场景"><span aria-hidden="true">▶</span><span>朗读整个场景</span></button>'
        if scene.get("speak") else ""
    )

    return f'''<section class="scene-card" id="{sid}" data-scene>
      <div class="scene-topline">
        <div><span class="scene-id">{sid.upper()}</span><span class="time">{scene.get("time", "")}</span></div>
        {scene_speak_btn}
      </div>
      <h2>{scene["title_cn"]}</h2>
      <p class="scene-title-en">{scene["title_en"]}</p>
      <p class="context"><b>情境</b>{scene["context"]}</p>
      <div class="sentence-list">
        {''.join(sent_html)}
      </div>
      {para_html}
    </section>'''


def render_practice(items: list[dict], slug: str) -> str:
    cards = []
    for i, it in enumerate(items):
        cards.append(f'''<article>
          <p>{it["cn"]}</p>
          <div class="practice-en">
            {it["en"]}
            <button class="speak-btn icon-only" type="button" data-audio="audio/en/{slug}/practice-{i}.mp3" aria-label="朗读练习句"><span aria-hidden="true">▶</span><span>朗读练习句</span></button>
          </div>
        </article>''')
    return f'''<section class="study-section" id="practice">
      <h2 class="section-heading">今日可练 <small>PRACTICE TODAY</small></h2>
      <div class="study-grid">
        {''.join(cards)}
      </div>
    </section>'''


def render_pitfalls(items: list[dict]) -> str:
    cards = []
    for it in items:
        cards.append(f'''<article>
          <div class="wrong">✕ {it["wrong"]}</div>
          <div class="right">✓ {it["right"]}</div>
          <p>{it["why"]}</p>
        </article>''')
    return f'''<section class="study-section pitfalls" id="pitfalls">
      <h2 class="section-heading">避坑 <small>PITFALLS</small></h2>
      <div class="study-grid">
        {''.join(cards)}
      </div>
    </section>'''


def render_shifts(items: list[dict]) -> str:
    cards = []
    for it in items:
        cards.append(f'''<article>
          <span>{it["before"]}</span>
          <b aria-hidden="true">→</b>
          <strong>{it["after"]}</strong>
        </article>''')
    return f'''<section class="study-section shifts" id="mindset">
      <h2 class="section-heading">认知转变 <small>MINDSET SHIFTS</small></h2>
      <div class="study-grid">
        {''.join(cards)}
      </div>
    </section>'''


def build_html(data: dict) -> str:
    slug = data["slug"]
    title = data["title"]
    title_en = data["title_en"]
    scenes = data["scenes"]

    # 中文语音讲解：复用已有 audio/{slug}.mp3（若有）
    narration_mp3 = data.get("narration_mp3") or ""
    if not narration_mp3:
        cand = DOCS / "audio" / f"{slug}.mp3"
        if cand.exists():
            narration_mp3 = f"audio/{slug}.mp3"

    map_links = "\n".join(
        f'''<a class="map-link" href="#{s["id"]}">
          <span class="map-id">{s["id"].upper()}</span>
          <span><b>{esc(s["title_cn"])}</b><small>{s.get("time", "")} · {esc(s["title_en"])}</small></span>
        </a>'''
        for s in scenes
    )

    scene_cards = "\n".join(render_scene(s, slug) for s in scenes)
    practice_html = render_practice(data.get("practice", []), slug)
    pitfalls_html = render_pitfalls(data.get("pitfalls", []))
    shifts_html = render_shifts(data.get("shifts", []))
    summary_en = data.get("summary_en", "")

    lang_switch = (
        f'<div class="lang-switch">'
        f'<a href="{cn_html_name(slug)}">中文</a>'
        f'<a class="active" href="{slug}-en.html" aria-current="page">EN</a>'
        f'</div>'
    )

    narration = ""
    if narration_mp3:
        narration = f'''<div class="narration-player">
      <p class="audio-label">🎧 中文语音讲解</p>
      <button class="speak-btn" type="button" data-audio="{narration_mp3}" aria-label="播放语音讲解"><span aria-hidden="true">▶</span><span>播放语音讲解</span></button>
    </div>'''

    summary_html = ""
    if summary_en:
        summary_html = f'''<p class="summary-en" style="margin:0 0 14px;padding:14px 16px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.22);border-radius:12px;font-size:.95rem;line-height:1.7">{summary_en}</p>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{esc(title)} — Bilingual Learning Edition" />
  <title>{esc(title)}｜EN 双语学习版</title>
  <style>{CSS}</style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <div class="hero-flex">
        <div class="hero-text">
          <p class="eyebrow">{esc(data.get("eyebrow", "Bilingual Learning"))}</p>
          <h1>{esc(title)}</h1>
          <p class="hero-en">{esc(title_en)}</p>
          {summary_html}
          <div class="hero-meta">
            <span class="chip">{esc(data.get("date", ""))}</span>
            <span class="chip">{esc(data.get("platform", ""))}</span>
            <span class="chip">{esc(data.get("duration", ""))}</span>
            <span class="chip">{len(scenes)} Scenes</span>
            <span class="chip">Click underlined words to hear them</span>
            <a class="source-link" href="{esc(data.get("source_url", "#"))}" target="_blank" rel="noopener">原播客 ↗</a>
          </div>
        </div>
      </div>
      <div class="toolbar">
        <div class="lang-switch">{lang_switch}</div>
        <label for="speech-rate">朗读速度</label>
        <select id="speech-rate">
          <option value="0.85">慢速 0.85×</option>
          <option value="1" selected>正常 1×</option>
          <option value="1.15">快速 1.15×</option>
        </select>
        <button id="stop-speech" class="stop-btn" type="button">■ 停止朗读</button>
        <span id="speech-status" class="speech-status" role="status" aria-live="polite"></span>
      </div>
      {narration}
    </div>
  </header>
  <main class="page">
    <aside class="sidebar" aria-label="场景地图">
      <div class="sidebar-box">
        <h2>场景地图 · SCENE MAP</h2>
        <nav class="map-nav">
          {map_links}
        </nav>
      </div>
    </aside>
    <div class="content">
      {scene_cards}
      {practice_html}
      {pitfalls_html}
      {shifts_html}
      <footer>
        双语学习版 · 场景/句子朗读使用 edge-tts（en-US） · 单词发音使用浏览器 Web Speech API
        <div class="footer-note">中文版：<a href="{cn_html_name(slug)}">{cn_html_name(slug)}</a> · SVG 版：<a href="viewer.html?f={svg_name(slug)}" target="_blank">{svg_name(slug)}</a></div>
      </footer>
    </div>
  </main>
  <script>{JS}</script>
</body>
</html>'''


def generate(slug: str) -> Path:
    json_path = CONTENT_DIR / f"{slug}.json"
    if not json_path.exists():
        raise FileNotFoundError(f"缺少内容文件: {json_path}")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    out = DOCS / f"{slug}-en.html"
    out.write_text(build_html(data), encoding="utf-8")
    print(f"✓ {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return out


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    if args[0] == "--all":
        slugs = sorted(p.stem for p in CONTENT_DIR.glob("*.json"))
    else:
        slugs = args
    ok = 0
    for slug in slugs:
        try:
            generate(slug)
            ok += 1
        except Exception as e:
            print(f"✗ {slug}: {e}")
    print(f"\n完成: {ok}/{len(slugs)}")
    sys.exit(0 if ok == len(slugs) else 1)


if __name__ == "__main__":
    main()
