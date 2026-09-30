// Rendert eine Canvas-HTML-Seite als PNG. Nutzung:
// node still.mjs <seite.html> <out.png> [--t=Sekunden] [--crop=x,y,w,h] [--scale=1]
import puppeteer from 'puppeteer-core';
import { readdirSync, existsSync } from 'fs';
import { homedir } from 'os';
import path from 'path';
function findChrome() {
  if (process.env.CHROME && existsSync(process.env.CHROME)) return process.env.CHROME;
  const base = path.join(homedir(), '.cache/puppeteer/chrome-headless-shell');
  if (existsSync(base)) for (const v of readdirSync(base).sort().reverse()) {
    const p = path.join(base, v, 'chrome-headless-shell-mac-arm64/chrome-headless-shell');
    if (existsSync(p)) return p;
  }
  const g = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  if (existsSync(g)) return g;
  throw new Error('Kein Chrome gefunden (CHROME=... setzen)');
}
const [,, page, out, ...rest] = process.argv;
const opt = Object.fromEntries(rest.map(a => a.replace(/^--/, '').split('=')));
const browser = await puppeteer.launch({ executablePath: findChrome(), headless: true,
  args: ['--allow-file-access-from-files', '--enable-webgl', '--ignore-gpu-blocklist'] });
const tab = await browser.newPage();
await tab.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
const errors = [];
tab.on('pageerror', e => errors.push(String(e)));
tab.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
const url = 'file://' + path.resolve(page) + (opt.t ? `?t=${opt.t}` : '');
await tab.goto(url);
await tab.waitForFunction(() => document.title === 'done', { timeout: 120000 });
const canvas = await tab.$('canvas');
const t0 = Date.now();
const clip = opt.crop ? (([x, y, w, h]) => ({ x, y, width: w, height: h }))(opt.crop.split(',').map(Number)) : undefined;
await (clip ? tab.screenshot({ path: out, clip }) : canvas.screenshot({ path: out }));
await browser.close();
if (errors.length) { console.error('Seitenfehler:\n' + errors.join('\n')); process.exit(2); }
console.log('ok', out);
