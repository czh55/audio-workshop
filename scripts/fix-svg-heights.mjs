#!/usr/bin/env node
/**
 * 重新测量 SVG 高度并修正 foreignObject 截断问题。
 *
 * 用法：
 *   node scripts/fix-svg-heights.mjs              # 扫描 docs/ 下全部 SVG
 *   node scripts/fix-svg-heights.mjs docs/foo.svg # 单文件
 *   node scripts/fix-svg-heights.mjs --dry-run    # 只报告不写入
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { resolveSvgHeight, wrapForeignObjectSvg, fixSvgXml } from '../svg-auto-height.mjs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const DOCS = path.join(ROOT, 'docs');
const dryRun = process.argv.includes('--dry-run');
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
  const css = text.match(/<style>([\s\S]*?)<\/style>/)?.[1] ?? '';
  const body = text.match(/<style>[\s\S]*?<\/style>\s*([\s\S]*?)<\/div>\s*<\/div>\s*<\/foreignObject>/)?.[1]?.trim() ?? '';
  return { width, declared, css, body };
}

async function fixOne(fp) {
  const text = fs.readFileSync(fp, 'utf8');
  const { width, declared, css, body } = parseSvgParts(text);
  if (!body) {
    console.warn('SKIP (no body):', fp);
    return null;
  }

  const measured = await resolveSvgHeight(`<style>${css}</style>${body}`, width);
  const needed = Math.ceil(measured * 1.5);
  const ratio = declared / needed;

  if (ratio >= 0.98) {
    return { fp, declared, needed, ratio, changed: false };
  }

  let svg = wrapForeignObjectSvg({ css, body, width, height: needed });
  svg = fixSvgXml(svg);

  if (!dryRun) {
    fs.writeFileSync(fp, svg, 'utf8');
  }

  return { fp, declared, needed, ratio, changed: true };
}

const files = collectSvgs();
let changed = 0;

for (const fp of files) {
  const result = await fixOne(fp);
  if (!result) continue;
  const rel = path.relative(ROOT, result.fp);
  if (result.changed) {
    changed += 1;
    console.log(`FIX ${rel}: ${result.declared} -> ${result.needed} (ratio ${result.ratio.toFixed(3)})`);
  }
}

console.log(`\nScanned ${files.length} SVGs, ${changed} ${dryRun ? 'would be ' : ''}updated.`);
