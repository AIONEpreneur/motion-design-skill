// Bildwelt im Stil von „Western Civilization in Motion“ (vittorio, X):
// Pergament mit Vignette und starkem Korn, saubere Tuschelinien (2–4 px), schraffierte Seitenflächen,
// perspektivische Linien-Architektur, Versal-Antiqua schwarz + rotes Schlüsselwort.
// Dunkle Welt: Schwarzbraun mit Strahlenkranz, goldene glühende Linien, leichte Farbsäume (chromatische Aberration).
const P = {
  parC: '#dcc9a8', parM: '#bfab8b', parE: '#77664f', ink: '#1a0f08', ink2: '#3b2c20', red: '#a8301d', redL: '#c9533a',
  gold: '#e2bd62', goldD: '#9a7430', goldL: '#f6e2a4', blue: '#2e4a6b', wood: '#b48a58', woodD: '#7a5532', plaster: '#e8dcc3',
  mold: '#2c3325', water: '#4f7596', dark0: '#060504', dark1: '#2b1d10', cream: '#efe3c6'
};
let GR = [], MOTTLE;
function makeTex() {
  for (let k = 0; k < 4; k++) { const w = 960, h = 540, c = mk(w, h), g = c.getContext('2d'), im = g.createImageData(w, h), d = im.data, R = rng(50 + k);
    for (let i = 0; i < w * h; i++) { const v = 128 + (R() + R() + R() - 1.5) * 95; d[i * 4] = d[i * 4 + 1] = d[i * 4 + 2] = v; d[i * 4 + 3] = 255; } g.putImageData(im, 0, 0); GR.push(c); }
  // Fleckigkeit des Pergaments (niedrige Frequenz)
  const c = mk(480, 270), g = c.getContext('2d'), R = rng(9);
  for (let i = 0; i < 90; i++) { const x = R() * 480, y = R() * 270, r = 20 + R() * 90, gg = g.createRadialGradient(x, y, 0, x, y, r), dark = R() > .5;
    gg.addColorStop(0, dark ? 'rgba(90,60,30,.05)' : 'rgba(255,245,220,.06)'); gg.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gg; g.fillRect(x - r, y - r, 2 * r, 2 * r); }
  MOTTLE = c;
}
function parchment(t, cx = 960, cy = 520) {
  const g = X.createRadialGradient(cx, cy, 60, cx, cy, 1150); g.addColorStop(0, '#e6d3b0'); g.addColorStop(.4, '#d3bd98'); g.addColorStop(.78, '#ad9573'); g.addColorStop(1, P.parE);
  X.fillStyle = g; X.fillRect(0, 0, W, H); X.drawImage(MOTTLE, 0, 0, W, H);
  // zarte senkrechte Hilfslinien wie auf Zeichenpapier
  X.save(); X.strokeStyle = 'rgba(90,70,50,.07)'; X.lineWidth = 1; X.beginPath(); for (let x = 240; x < W; x += 240) { X.moveTo(x + .5, 0); X.lineTo(x + .5, H); } X.stroke(); X.restore();
}
function darkBG(t, cx = 960, cy = 480, warm = 1, rays = 1) {
  X.fillStyle = P.dark0; X.fillRect(0, 0, W, H);
  const g = X.createRadialGradient(cx, cy, 20, cx, cy, 900); g.addColorStop(0, hexA('#8a6a44', .75 * warm)); g.addColorStop(.35, hexA('#3a2814', .7 * warm)); g.addColorStop(1, 'rgba(0,0,0,0)'); X.fillStyle = g; X.fillRect(0, 0, W, H);
  if (rays > 0) { X.save(); X.translate(cx, cy); X.rotate(t * .02); for (let i = 0; i < 150; i++) { const a = hash(i * 1.7) * Math.PI * 2, w = .004 + hash(i * 3.1) * .01, r0 = 260 + hash(i * 5.3) * 300; X.fillStyle = `rgba(215,190,150,${(.05 + hash(i) * .12) * rays})`; X.beginPath(); X.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); X.lineTo(Math.cos(a - w) * 2400, Math.sin(a - w) * 2400); X.lineTo(Math.cos(a + w) * 2400, Math.sin(a + w) * 2400); X.closePath(); X.fill(); } X.restore(); }
}
function finish(t, dark = false) {
  // Vignette
  const g = X.createRadialGradient(960, 540, 380, 960, 540, 1180); g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, dark ? 'rgba(0,0,0,.7)' : 'rgba(60,35,12,.32)'); X.fillStyle = g; X.fillRect(0, 0, W, H);
  // Korn, flackernd wie Film (12 Bilder/s)
  X.save(); X.globalCompositeOperation = 'overlay'; X.globalAlpha = dark ? .32 : .3; X.drawImage(GR[Math.floor(t * 12) % 4], 0, 0, W, H); X.restore();
}

// ---------- 3D ----------
const CAM = { x: 0, y: 4, z: -30, yaw: 0, pitch: 0, f: 1400, cx: 960, cy: 560 };
function prj(p) { let x = p[0] - CAM.x, y = p[1] - CAM.y, z = p[2] - CAM.z; const cy = Math.cos(CAM.yaw), sy = Math.sin(CAM.yaw); [x, z] = [x * cy - z * sy, x * sy + z * cy];
  const cp = Math.cos(CAM.pitch), sp = Math.sin(CAM.pitch); [y, z] = [y * cp - z * sp, y * sp + z * cp]; z = Math.max(z, .1); return [CAM.cx + CAM.f * x / z, CAM.cy - CAM.f * y / z, z]; }
function camLook(tx, ty, tz, dist, yaw, pitch, f = 1400, sx = 960, sy = 560) { CAM.yaw = yaw; CAM.pitch = pitch; CAM.f = f; CAM.cx = sx; CAM.cy = sy;
  const cp = Math.cos(pitch), d = [Math.sin(yaw) * cp, Math.sin(pitch), Math.cos(yaw) * cp]; CAM.x = tx - d[0] * dist; CAM.y = ty - d[1] * dist; CAM.z = tz - d[2] * dist; }
function poly3(pts) { const p = new Path2D(); pts.forEach((q, i) => { const s = prj(q); i ? p.lineTo(s[0], s[1]) : p.moveTo(s[0], s[1]); }); p.closePath(); return p; }
function seg3(a, b) { const p = new Path2D(), A = prj(a), B = prj(b); p.moveTo(A[0], A[1]); p.lineTo(B[0], B[1]); return p; }
function sub3(a, b, k) { return [mix(a[0], b[0], k), mix(a[1], b[1], k), mix(a[2], b[2], k)]; }
// Muster: feine Schraffur (Bildschirm-Raum) für Seitenflächen
const PAT = new Map();
function hatchPat(col, sp, lw, ang = 1) { const key = col + sp + lw + ang; if (PAT.has(key)) return PAT.get(key); const T = sp * 12, c = mk(T, T), g = c.getContext('2d'); g.strokeStyle = col; g.lineWidth = lw; g.beginPath();
  for (let i = -T; i < 2 * T; i += sp) { if (ang > 0) { g.moveTo(i, T); g.lineTo(i + T, 0); } else { g.moveTo(i, 0); g.lineTo(i + T, T); } } g.stroke(); const pt = X.createPattern(c, 'repeat'); PAT.set(key, pt); return pt; }
function hatchPath(p, col, sp = 7, lw = 1.1, a = 1, ang = 1) { X.save(); X.clip(p); X.globalAlpha *= a; X.fillStyle = hatchPat(col, sp, lw, ang); X.fillRect(0, 0, W, H); X.restore(); }
// Linie mit Modus: Tusche (hell) oder Gold mit Glühen und Farbsäumen (dunkel)
let DARK = 0;
function stroke(p, lw = 2.6, col = null, glow = 12) {
  X.lineJoin = 'round'; X.lineCap = 'round';
  if (!DARK) { X.strokeStyle = col || P.ink; X.lineWidth = lw; X.stroke(p); return; }
  const c = col || P.gold;
  X.save(); X.globalAlpha *= .45; X.lineWidth = lw; X.strokeStyle = '#ff5a4a'; X.translate(-2.2, 0); X.stroke(p); X.strokeStyle = '#4ad6ff'; X.translate(4.4, 0); X.stroke(p); X.restore();
  X.save(); X.shadowColor = c; X.shadowBlur = glow; X.strokeStyle = c; X.lineWidth = lw; X.stroke(p); X.restore();
}

// ---------- Schrift: Versal-Antiqua (Cinzel), Überschrift als Ganzes ----------
// lines: [{s, size, y, red, gold}] – alle Zeilen erscheinen zusammen per Maske von unten, fertig bei k.
function headline(t, lines, k, o = {}) {
  const d = o.d ?? .32, p = e4(lin(t, k - d, k)); if (p <= 0) return;
  const oa = o.out != null ? 1 - lin(t, o.out, o.out + .2) : 1; if (oa <= 0) return;
  X.save(); X.globalAlpha = oa; X.textBaseline = 'alphabetic';
  for (const L of lines) { X.font = `800 ${L.size}px CZ`; X.letterSpacing = (L.ls ?? L.size * .06) + 'px';
    const segs = L.segs || [{ s: L.s, red: L.red, gold: L.gold }]; const ws = segs.map(g => X.measureText(g.s).width), total = ws.reduce((a, b) => a + b, 0);
    let x = o.align === 'center' ? 960 - total / 2 : (o.x ?? 130);
    X.save(); X.beginPath(); X.rect(x - 40, L.y - L.size * 1.02, total + 80, L.size * 1.3); X.clip();
    const dy = (1 - p) * L.size * 1.15;
    segs.forEach((g, i) => { const col = g.red ? (DARK ? '#ff6a4a' : P.red) : (g.gold ? P.goldL : (DARK ? '#f1e6cc' : P.ink));
      X.save(); if (DARK) { X.shadowColor = g.red ? '#ff5030' : '#e8c070'; X.shadowBlur = g.red || g.gold ? 30 : 14; }
      X.fillStyle = col; X.fillText(g.s, x, L.y + dy); X.restore(); x += ws[i]; });
    X.restore(); }
  X.restore();
}
function mono(s, x, y, size, col, align = 'left', a = 1, ls = 4) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.font = `500 ${size}px PM`; X.letterSpacing = ls + 'px'; X.textAlign = align; X.fillStyle = col; if (DARK) { X.shadowColor = col; X.shadowBlur = 10; } X.fillText(s, x, y); X.restore(); }
// rote Maßkette mit Pfeilspitzen und Zahl
function dim(ax, ay, bx, by, k, label, col = P.red, off = 0) { if (k <= 0) return; const ex = mix(ax, bx, eo(k)), ey = mix(ay, by, eo(k)), ang = Math.atan2(by - ay, bx - ax), nx = -Math.sin(ang), ny = Math.cos(ang);
  X.save(); X.strokeStyle = col; X.fillStyle = col; X.lineWidth = 2.2; X.beginPath(); X.moveTo(ax + nx * 14, ay + ny * 14); X.lineTo(ax - nx * 14, ay - ny * 14); X.moveTo(ax, ay); X.lineTo(ex, ey); X.stroke();
  const head = (x, y, a) => { X.beginPath(); X.moveTo(x, y); X.lineTo(x - Math.cos(a - .35) * 16, y - Math.sin(a - .35) * 16); X.lineTo(x - Math.cos(a + .35) * 16, y - Math.sin(a + .35) * 16); X.closePath(); X.fill(); };
  head(ax, ay, ang + Math.PI); if (k >= 1) { head(bx, by, ang); X.beginPath(); X.moveTo(bx + nx * 14, by + ny * 14); X.lineTo(bx - nx * 14, by - ny * 14); X.stroke(); }
  if (label && k > .6) { X.globalAlpha = lin(k, .6, 1); X.font = '500 26px PM'; X.letterSpacing = '2px'; X.textAlign = 'center'; const mx = (ax + bx) / 2 + nx * (22 + off), my = (ay + by) / 2 + ny * (22 + off); X.translate(mx, my); let a = ang; if (a > Math.PI / 2 || a < -Math.PI / 2) a += Math.PI; X.rotate(a); X.fillText(label, 0, 9); }
  X.restore(); }
function ringPulse(x, y, t, t0, r0, r1, col, dur = .6, lw = 2.4) { const k = lin(t, t0, t0 + dur); if (k <= 0 || k >= 1) return; X.save(); X.globalAlpha = 1 - k; X.strokeStyle = col; X.lineWidth = lw; X.beginPath(); X.arc(x, y, mix(r0, r1, eo(k)), 0, 7); X.stroke(); X.restore(); }
