#!/usr/bin/env node
/**
 * Serializes audio CDN requests across local automation runs.
 * Invoke immediately before every curl download from Xiaoyuzhou FM CDN.
 *
 * Configurable via environment variables:
 *   RATE_LIMIT_INTERVAL_MS  - minimum interval between requests (default 30_000)
 *   RATE_LIMIT_STATE_FILE   - path to timestamp state file (default /tmp/audio-workshop-last-request)
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const intervalMs = Number(process.env.RATE_LIMIT_INTERVAL_MS) || 30_000;
const stateFile = process.env.RATE_LIMIT_STATE_FILE ||
  path.join(os.tmpdir(), 'audio-workshop-last-request');
const lockFile = `${stateFile}.lock`;

const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

async function acquireLock() {
  while (true) {
    try {
      return fs.openSync(lockFile, 'wx');
    } catch (error) {
      if (error.code !== 'EEXIST') throw error;
      await sleep(100);
    }
  }
}

const lockFd = await acquireLock();
try {
  const lastRequest = Number(
    fs.existsSync(stateFile) ? fs.readFileSync(stateFile, 'utf8') : 0
  );
  const waitMs = Math.max(0, intervalMs - (Date.now() - lastRequest));
  if (waitMs > 0) {
    console.log(`音频CDN请求限流：等待 ${Math.ceil(waitMs / 1000)} 秒`);
    await sleep(waitMs);
  }

  // Reserve the slot while holding the lock. The following request must start now.
  fs.writeFileSync(stateFile, String(Date.now()));
} finally {
  fs.closeSync(lockFd);
  fs.unlinkSync(lockFile);
}
