// Rendert eine Film-Seite Frame für Frame zu MP4 (oder zu Standbildern / Kontaktbogen).
//
// Vertrag der Seite (index.html):
//   window.FILM = { duration, width = 1920, height = 1080, ready: Promise|true, seek(t) }
//   seek(t) zeichnet exakt das Bild zur Zeit t (Sekunden), synchron oder als Promise.
//   Jedes Frame ist eine reine Funktion von t: kein Math.random, kein Date, keine laufenden Animationen.
//
// Nutzung (aus dem Projektordner):
//   node render.mjs index.html --out=out/video.mp4 [--fps=30] [--workers=4] [--audio=out/mix.wav]
//   node render.mjs index.html --stills=1.5,4,9.2 --out=out/stills        (PNG je Zeitpunkt)
//   node render.mjs index.html --sheet=0.5,3,6,9 --out=out/sheet.jpg     (Kontaktbogen)
//   node render.mjs index.html --strip=4:5.5 --out=out/strip.jpg          (jedes Frame eines Abschnitts)
//   Option --range=a:b begrenzt das Video auf einen Abschnitt.
//
// Untertitel: Liegt im Projektordner eine untertitel.json, wird sie automatisch über jedes Bild gelegt
// (abschalten mit --ohne-untertitel, andere Datei mit --untertitel=pfad). Format:
//   { "vo": "out/vo.json",                       // Wortzeiten von vo_kie.py
//     "stil": { "font": "fonts/<eigene Schrift>.ttf", "size": 52, "y": 992,
//               "bg": "#FFC526", "fg": "#0E1A30",     // Kasten und Schrift: muss sich klar vom Filmhintergrund abheben
//               "hiBg": "#0E1A30", "hiFg": "#FFC526", // gerade gesprochenes Wort
//               "upper": false, "radius": 14, "maxWords": 6, "maxChars": 34 },
//     "ersetzen": { "einundsiebzig": "71" } }     // Schreibweise im Untertitel (Zahlen als Ziffern)
//   Der Film muss den Streifen y > 930 (bei 1080 px Höhe) frei von wichtigen Inhalten halten.
import puppeteer from 'puppeteer-core';
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'fs';
import { homedir } from 'os';
import path from 'path';
import { spawnSync } from 'child_process';

const [, , pageArg, ...rest] = process.argv;
if (!pageArg) { console.error('Nutzung: node render.mjs <index.html> --out=... [Optionen]'); process.exit(1); }
const A = Object.fromEntries(rest.map(a => { const [k, v] = a.replace(/^--/, '').split('='); return [k, v ?? true]; }));
const fps = +(A.fps || 30);

function findChrome() {
  if (process.env.CHROME && existsSync(process.env.CHROME)) return process.env.CHROME;
  const base = path.join(homedir(), '.cache/puppeteer/chrome-headless-shell');
  if (existsSync(base)) for (const v of readdirSync(base).sort().reverse()) {
    for (const sub of readdirSync(path.join(base, v)).filter(d => d.startsWith('chrome-headless-shell-'))) {
      for (const exe of ['chrome-headless-shell', 'chrome-headless-shell.exe']) { const p = path.join(base, v, sub, exe); if (existsSync(p)) return p; }
    }
  }
  for (const g of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome', '/usr/bin/chromium', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'])
    if (existsSync(g)) return g;
  throw new Error('Kein Chrome gefunden (CHROME=... setzen)');
}

// ---------- Untertitel ----------
let CAP = null;
const capFile = A['ohne-untertitel'] ? null : (A.untertitel || (existsSync('untertitel.json') ? 'untertitel.json' : null));
if (capFile) {
  const cfg = JSON.parse(readFileSync(capFile, 'utf8')); const base = path.dirname(path.resolve(capFile));
  const vo = JSON.parse(readFileSync(path.resolve(base, cfg.vo || 'out/vo.json'), 'utf8'));
  const st = Object.assign({ size: 52, y: 992, bg: '#FFC526', fg: '#0E1A30', hiBg: '#0E1A30', hiFg: '#FFC526', upper: false, radius: 14, maxWords: 6, maxChars: 34, padX: 26, padY: 14 }, cfg.stil || {});
  const rep = cfg.ersetzen || {};
  const ws = vo.words.filter(w => w.text).map(w => { const core = w.text.replace(/[.,:;!?„“"()]/g, ''); const r = rep[core.toLowerCase()] || rep[core];
    return { t: r ? w.text.replace(core, r) : w.text, s: w.start, e: w.end }; });
  const chunks = []; let cur = [];
  ws.forEach((w, i) => { cur.push(w); const nx = ws[i + 1]; const len = cur.map(x => x.t).join(' ').length;
    if (!nx || /[.?!:]$/.test(w.t) || cur.length >= st.maxWords || len + 1 + nx.t.length > st.maxChars || nx.s - w.e > .45) { chunks.push(cur); cur = []; } });
  CAP = { st, fontUrl: st.font ? 'file://' + path.resolve(base, st.font) : null,
    chunks: chunks.map((c, i) => ({ words: c.map(w => ({ t: st.upper ? w.t.toUpperCase() : w.t, s: w.s })), a: c[0].s - .08,
      b: Math.min(chunks[i + 1] ? chunks[i + 1][0].s - .04 : 1e9, c[c.length - 1].e + .7) })) };
  console.log(`Untertitel: ${capFile} (${CAP.chunks.length} Zeilen)`);
}
async function installCaptions(page, W, H) {
  if (!CAP) return;
  await page.evaluate(async (CAP, W, H) => {
    if (CAP.fontUrl) { const f = new FontFace('__capfont', `url("${CAP.fontUrl}")`); await f.load(); document.fonts.add(f); }
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    c.style.cssText = `position:fixed;left:0;top:0;width:${W}px;height:${H}px;z-index:2147483647;pointer-events:none`;
    document.body.appendChild(c); const g = c.getContext('2d'); const st = CAP.st;
    const font = `${st.size}px ${CAP.fontUrl ? '__capfont' : 'Helvetica Neue, Arial'}`;
    const rr = (x, y, w, h, r) => { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); };
    window.__cap = t => {
      g.clearRect(0, 0, W, H);
      const ch = CAP.chunks.find(k => t >= k.a && t < k.b); if (!ch) return;
      const pin = Math.min(1, (t - ch.a) / .14), pout = Math.min(1, Math.max(0, (ch.b - t) / .1)), k = Math.min(pin, pout);
      g.font = font; const sp = g.measureText(' ').width + st.size * .22, ww = ch.words.map(w => g.measureText(w.t).width);
      const tw = ww.reduce((a, b) => a + b, 0) + sp * (ww.length - 1), bw = tw + st.padX * 2, bh = st.size * 1.05 + st.padY * 2;
      const e = 1 - Math.pow(1 - k, 3), sc = .94 + .06 * e;
      g.save(); g.globalAlpha = e; g.translate(W / 2, st.y); g.scale(sc, sc);
      g.shadowColor = 'rgba(0,0,0,.35)'; g.shadowBlur = 18; g.shadowOffsetY = 6; rr(-bw / 2, -bh / 2, bw, bh, st.radius); g.fillStyle = st.bg; g.fill();
      g.shadowColor = 'transparent'; g.textBaseline = 'middle'; g.textAlign = 'left';
      let x = -tw / 2; const act = ch.words.reduce((a, w, i) => t >= w.s - .03 ? i : a, -1);
      ch.words.forEach((w, i) => {
        if (i === act) { g.fillStyle = st.hiBg; rr(x - 8, -st.size * .56, ww[i] + 16, st.size * 1.08, 8); g.fill(); g.fillStyle = st.hiFg; }
        else g.fillStyle = st.fg;
        g.fillText(w.t, x, st.size * .04); x += ww[i] + sp; });
      g.restore(); };
    return 0;
  }, CAP, W, H);
}

const browser = await puppeteer.launch({
  executablePath: findChrome(), headless: true, protocolTimeout: 0,
  args: ['--allow-file-access-from-files', '--ignore-gpu-blocklist', '--use-angle=metal', '--enable-gpu-rasterization',
    '--disable-renderer-backgrounding', '--disable-background-timer-throttling', '--autoplay-policy=no-user-gesture-required'],
});

const errors = [];
async function openPage() {
  const page = await browser.newPage();
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(pageArg), { waitUntil: 'load' });
  await page.waitForFunction(() => window.FILM, { timeout: 60000 });
  await page.evaluate(async () => { const r = window.FILM.ready; if (r instanceof Promise) await r; await document.fonts.ready; return 0; });
  const dim = await page.evaluate(() => [window.FILM.width || 1920, window.FILM.height || 1080]);
  if (dim[0] !== 1920 || dim[1] !== 1080) await page.setViewport({ width: dim[0], height: dim[1], deviceScaleFactor: 1 });
  await installCaptions(page, dim[0], dim[1]);
  return { page, W: dim[0], H: dim[1] };
}
async function shot(p, t, file, type = 'jpeg') {
  // Nur echte Promises abwarten: GSAP-Timelines sind 'thenable' und würden sonst ewig hängen.
  await p.page.evaluate(async t => { const r = window.FILM.seek(t); if (r instanceof Promise) await r; if (window.__cap) window.__cap(t); return 0; }, t);
  await p.page.screenshot({ path: file, type, ...(type === 'jpeg' ? { quality: 93 } : {}), clip: { x: 0, y: 0, width: p.W, height: p.H } });
}
const nums = s => String(s).split(',').map(Number);
const span = s => String(s).split(':').map(Number);
function done(code = 0) {
  if (errors.length) { console.error('Seitenfehler:\n' + [...new Set(errors)].slice(0, 20).join('\n')); code = code || 2; }
  return browser.close().then(() => process.exit(code));
}
function tile(files, out, cols, w) {
  const n = files.length, list = files.map(f => ['-i', f]).flat();
  const h = Math.round(w * 9 / 16), rows = Math.ceil(n / cols);
  const filt = files.map((_, i) => `[${i}:v]scale=${w}:${h}[s${i}]`).join(';') + ';' +
    files.map((_, i) => `[s${i}]`).join('') + `xstack=inputs=${n}:layout=` +
    files.map((_, i) => `${(i % cols) * w}_${Math.floor(i / cols) * h}`).join('|') + `:fill=white[o]`;
  if (n === 1) { spawnSync('ffmpeg', ['-loglevel', 'error', '-y', '-i', files[0], '-vf', `scale=${w}:${h}`, out]); return; }
  const r = spawnSync('ffmpeg', ['-loglevel', 'error', '-y', ...list, '-filter_complex', filt, '-map', '[o]', '-frames:v', '1', out]);
  if (r.status) console.error(String(r.stderr));
}

const p0 = await openPage();
const duration = await p0.page.evaluate(() => window.FILM.duration);

if (A.stills) {
  const out = A.out || 'out/stills'; mkdirSync(out, { recursive: true });
  for (const t of nums(A.stills)) { const f = path.join(out, `t_${t.toFixed(2)}.png`); await shot(p0, t, f, 'png'); console.log(f); }
  await done();
} else if (A.sheet || A.strip) {
  let ts;
  if (A.strip) { const [a, b] = span(A.strip); ts = []; for (let i = Math.round(a * fps); i <= Math.round(b * fps); i += +(A.step || 1)) ts.push(i / fps); }
  else ts = nums(A.sheet);
  const tmp = path.join('out', '.sheet_tmp'); rmSync(tmp, { recursive: true, force: true }); mkdirSync(tmp, { recursive: true });
  const files = [];
  for (const [i, t] of ts.entries()) { const f = path.join(tmp, `${String(i).padStart(4, '0')}.jpg`); await shot(p0, t, f); files.push(f); }
  const out = A.out || 'out/sheet.jpg'; mkdirSync(path.dirname(out), { recursive: true });
  tile(files, out, +(A.cols || (A.strip ? 6 : 4)), +(A.w || (A.strip ? 320 : 480)));
  writeFileSync(out + '.txt', ts.map((t, i) => `${i + 1}: ${t.toFixed(3)}s`).join('\n'));
  console.log(out, `(${ts.length} Bilder, Zeiten in ${out}.txt)`);
  await done();
} else {
  const [a, b] = A.range ? span(A.range) : [0, duration];
  const n = Math.round((b - a) * fps), workers = Math.max(1, +(A.workers || 4));
  const frames = path.join('out', '.frames'); rmSync(frames, { recursive: true, force: true }); mkdirSync(frames, { recursive: true });
  const pages = [p0]; for (let w = 1; w < workers; w++) pages.push(await openPage());
  const t0 = Date.now(); let doneN = 0;
  await Promise.all(pages.map(async (p, w) => {
    for (let i = w; i < n; i += workers) {
      await shot(p, a + i / fps, path.join(frames, `${String(i).padStart(6, '0')}.jpg`));
      if (++doneN % 60 === 0) process.stdout.write(`\r${doneN}/${n} Frames, ${((Date.now() - t0) / doneN).toFixed(0)} ms/Frame   `);
    }
  }));
  console.log(`\r${n}/${n} Frames in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
  const out = A.out || 'out/video.mp4'; mkdirSync(path.dirname(out), { recursive: true });
  const audio = A.audio && existsSync(A.audio) ? ['-ss', String(a), '-i', A.audio] : [];
  const r = spawnSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', String(fps), '-i', path.join(frames, '%06d.jpg'), ...audio,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    ...(audio.length ? ['-c:a', 'aac', '-b:a', '192k', '-shortest'] : []), '-movflags', '+faststart', out], { stdio: 'inherit' });
  if (r.status) { console.error('ffmpeg fehlgeschlagen'); await done(1); }
  rmSync(frames, { recursive: true, force: true });
  console.log('fertig:', out);
  await done();
}
