#!/usr/bin/env node
/**
 * 重新测量 SVG 高度并修正 foreignObject 过高/过低问题。
 *
 * 用法：
 *   node scripts/fix-svg-heights.mjs              # 扫描 docs/ 下全部 SVG
 *   node scripts/fix-svg-heights.mjs docs/foo.svg # 单文件
 *   node scripts/fix-svg-heights.mjs --dry-run    # 只报告不写入
 *   node scripts/fix-svg-heights.mjs --sync-index # 同步 index.json / topics.json 中的 svg_height
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import {
  resolveSvgHeight,
  wrapForeignObjectSvg,
  fixSvgXml,
  computeSvgHeight,
} from '../svg-auto-height.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(ROOT, 'docs');
const dryRun = process.argv.includes('--dry-run');
const syncIndex = process.argv.includes('--sync-index');
const args = process.argv.slice(2).filter((a) => !a.startsWith('--'));

function collectSvgs() {
  if (args.length) {
    return args.map((p) => path.resolve(ROOT, p));
  }
  const out = [];
  function walk(dir) {
    for (const ent of fs.readdirSync(dir, { withFileTypes: true })) {
      const fp = path.join(dir, ent.name);
      if (ent.isDirectory()) walk(fp);
      else if (ent.name.endsWith('.svg')) out.push(fp);
    }
  }
  walk(DOCS);
  return out.sort();
}

function parseSvgParts(text) {
  const width = Number(text.match(/width="(\d+)"/)?.[1]) || 1320;
  const declared = Number(text.match(/height="(\d+)"/)?.[1]) || 0;
  const inner = text.match(
    /<div xmlns="http:\/\/www\.w3\.org\/1999\/xhtml">([\s\S]*?)<\/div>\s*<\/foreignObject>/,
  )?.[1];
  if (!inner) return { width, declared, css: '', body: '' };
  const css = inner.match(/<style>([\s\S]*?)<\/style>/)?.[1] ?? '';
  const body = inner.replace(/<style>[\s\S]*?<\/style>\s*/, '').trim();
  return { width, declared, css, body };
}

function needsFix(declared, needed) {
  if (!declared || !needed) return false;
  const diff = Math.abs(declared - needed);
  return diff > Math.max(24, needed * 0.03);
}

async function fixOne(fp) {
  const text = fs.readFileSync(fp, 'utf8');
  const { width, declared, css, body } = parseSvgParts(text);
  if (!body) {
    console.warn('SKIP (no body):', fp);
    return null;
  }

  const measured = await resolveSvgHeight(`<style>${css}</style>${body}`, width);
  const needed = computeSvgHeight(measured);

  if (!needsFix(declared, needed)) {
    return { fp, declared, needed, changed: false };
  }

  let svg = wrapForeignObjectSvg({ css, body, width, height: needed });
  svg = fixSvgXml(svg);

  if (!dryRun) {
    fs.writeFileSync(fp, svg, 'utf8');
  }

  const rel = path.relative(DOCS, fp).replace(/\\/g, '/');
  return { fp, rel, declared, needed, changed: true };
}

function syncIndexHeights(heightMap) {
  for (const jsonPath of ['index.json', 'topics.json']) {
    const full = path.join(DOCS, jsonPath);
    if (!fs.existsSync(full)) continue;
    const data = JSON.parse(fs.readFileSync(full, 'utf8'));
    let touched = 0;

    function patchItem(item) {
      if (!item?.filename || item.svg_height == null) return;
      const h = heightMap.get(item.filename);
      if (h && item.svg_height !== h) {
        item.svg_height = h;
        touched += 1;
      }
    }

    if (Array.isArray(data)) {
      const first = data[0];
      if (first?.items) {
        data.forEach((topic) => topic.items?.forEach(patchItem));
      } else {
        data.forEach(patchItem);
      }
    } else if (data?.topics) {
      for (const topic of data.topics) {
        topic.items?.forEach(patchItem);
      }
    }

    if (touched && !dryRun) {
      fs.writeFileSync(full, `${JSON.stringify(data, null, 2)}\n`, 'utf8');
    }
    console.log(`${jsonPath}: updated ${touched} svg_height entries`);
  }
}

const files = collectSvgs();
let changed = 0;
const heightMap = new Map();

for (const fp of files) {
  const result = await fixOne(fp);
  if (!result) continue;
  const rel = result.rel ?? path.relative(DOCS, result.fp).replace(/\\/g, '/');
  heightMap.set(rel, result.needed);
  if (result.changed) {
    changed += 1;
    const dir = result.declared > result.needed ? 'SHRINK' : 'GROW';
    console.log(`${dir} ${rel}: ${result.declared} -> ${result.needed}`);
  }
}

console.log(`\nScanned ${files.length} SVGs, ${changed} ${dryRun ? 'would be ' : ''}updated.`);

if (syncIndex || changed) {
  syncIndexHeights(heightMap);
}
