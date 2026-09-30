// Grundwerkzeuge im Strich des Originals („How browsers work“): Tusche-Kontur mit Handzittern,
// Schraffur als Muster, Papier mit Diagonalstreifen und Korn, Blaupause mit Raster, Glühen, Funkeln.
// Alles deterministisch: jedes Bild ist reine Funktion von t.
const W = 1920, H = 1080;
const cv = document.getElementById('c'), X = cv.getContext('2d');
const P = {
  paper: '#efe5cd', sBlue: '#c9d2cf', sMint: '#d8e3c8', sYel: '#ebdba3', win: '#f8f4ec', winD: '#e9e0cb',
  ink: '#2b211c', ink2: '#4a3f37', guide: '#8b8373',
  red: '#dc6a52', redD: '#b9493a', redL: '#f39b83', gold: '#e8c04e', goldD: '#a8841f',
  srv: '#7b889e', srvD: '#5d687f', srvF: '#aeb9ca', slot: '#4a5470', slotL: '#c9d1e2', led: '#8fd06f', amber: '#f0a53c',
  blush: '#f09b9b', dash: '#3f86d8', under: '#e4bb45', wood: '#a8784c', woodD: '#7d5634', woodL: '#c89a68',
  grass: '#79a152', soil: '#d6c7a4',
  navy0: '#0a0d26', navy1: '#1b214b', lav: '#cdd1f3', lavS: 'rgba(205,209,243,', mint: '#7de6c9', mag: '#ff3fa0', salmon: '#f39579', cream: '#f4ead3',
  lil: '#b8a2e3', sky: '#9fc3ee', teal: '#8fd6c6', yel: '#f2cf6c', pink: '#f2a7b8'
};
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v)), lin = (t, a, b) => clamp((t - a) / (b - a)), mix = (a, b, k) => a + (b - a) * k;
const eo = x => 1 - Math.pow(1 - x, 3), e4 = x => 1 - Math.pow(1 - x, 4), eio = x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
const back = x => { const c1 = 1.9, c3 = c1 + 1; return x <= 0 ? 0 : x >= 1 ? 1 : 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
// Einblendung, die spätestens bei k fertig ist: beginnt d vor k
const tin = (t, k, d = .32) => lin(t, k - d, k);
function hash(n) { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function n1(x) { const i = Math.floor(x), f = x - i, u = f * f * (3 - 2 * f); return mix(hash(i), hash(i + 1), u) * 2 - 1; }
function hstr(s) { let h = 7; for (const c of s) h = (h * 31 + c.charCodeAt(0)) % 100003; return h; }
function rng(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
function mk(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
function hexA(h, a) { const p = [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16)); return `rgba(${p.join(',')},${a})`; }
function mixCol(a, b, k) { const p = h => [1, 3, 5].map(i => parseInt(h.substr(i, 2), 16)); const A = p(a), B = p(b); return '#' + A.map((v, i) => Math.round(mix(v, B[i], k)).toString(16).padStart(2, '0')).join(''); }

// ---------- Formen mit Handzittern ----------
function rrP(x, y, w, h, r, st = 5) {
  r = Math.min(r, w / 2, h / 2); const pts = [];
  const edge = (x0, y0, x1, y1) => { const L = Math.hypot(x1 - x0, y1 - y0), n = Math.max(1, Math.ceil(L / st)); for (let i = 0; i < n; i++) pts.push([mix(x0, x1, i / n), mix(y0, y1, i / n)]); };
  const arc = (cx, cy, a0) => { const n = Math.max(3, Math.ceil(r * Math.PI / 2 / st)); for (let i = 0; i < n; i++) { const a = a0 + i / n * Math.PI / 2; pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
  edge(x + r, y, x + w - r, y); arc(x + w - r, y + r, -Math.PI / 2); edge(x + w, y + r, x + w, y + h - r); arc(x + w - r, y + h - r, 0);
  edge(x + w - r, y + h, x + r, y + h); arc(x + r, y + h - r, Math.PI / 2); edge(x, y + h - r, x, y + r); arc(x + r, y + r, Math.PI);
  return pts;
}
function ellP(cx, cy, rx, ry, st = 5, a0 = 0, a1 = Math.PI * 2) { const n = Math.max(8, Math.ceil(Math.abs(a1 - a0) * Math.max(rx, ry) / st)), pts = []; for (let i = 0; i <= n; i++) { const a = mix(a0, a1, i / n); pts.push([cx + Math.cos(a) * rx, cy + Math.sin(a) * ry]); } return pts; }
function polyP(q, closed = true, st = 5) { const pts = [], m = closed ? q.length : q.length - 1; for (let k = 0; k < m; k++) { const a = q[k], b = q[(k + 1) % q.length], n = Math.max(1, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / st)); for (let i = 0; i < n; i++) pts.push([mix(a[0], b[0], i / n), mix(a[1], b[1], i / n)]); } if (!closed) pts.push(q[q.length - 1]); return pts; }
function bezP(p0, p1, p2, p3, n = 30) { const pts = []; for (let i = 0; i <= n; i++) { const u = i / n, v = 1 - u; pts.push([v * v * v * p0[0] + 3 * v * v * u * p1[0] + 3 * v * u * u * p2[0] + u * u * u * p3[0], v * v * v * p0[1] + 3 * v * v * u * p1[1] + 3 * v * u * u * p2[1] + u * u * u * p3[1]]); } return pts; }
function wob(pts, closed, amp, seed, fq = .045) {
  const p = new Path2D(); let s = 0;
  pts.forEach((q, i) => { if (i) s += Math.hypot(q[0] - pts[i - 1][0], q[1] - pts[i - 1][1]); const x = q[0] + amp * n1(seed + s * fq), y = q[1] + amp * n1(seed + 91.3 + s * fq); i ? p.lineTo(x, y) : p.moveTo(x, y); });
  if (closed) p.closePath(); return p;
}
const CACHE = new Map();
// S(key, Punkte-Erzeuger, Zitter-Amplitude, geschlossen) -> Path2D (gecacht)
function S(key, gen, amp = 1.1, closed = true) { let p = CACHE.get(key); if (!p) { p = wob(gen(), closed, amp, hstr(key) % 997); CACHE.set(key, p); } return p; }

// ---------- Tusche ----------
function ink(p, fill, lw = 4.5, col = P.ink) {
  if (fill) { X.fillStyle = fill; X.fill(p); }
  if (lw) { X.lineJoin = 'round'; X.lineCap = 'round'; X.strokeStyle = col; X.lineWidth = lw; X.stroke(p);
    // zweiter, dünner Zug leicht versetzt: ungleichmäßige Tusche
    X.save(); X.globalAlpha *= .45; X.lineWidth = lw * .45; X.translate(.7, -.5); X.stroke(p); X.restore(); }
}
function line(pts, lw = 3, col = P.ink, key = null, amp = .8) { const p = key ? S(key, () => pts, amp, false) : wob(pts, false, amp, 3); X.lineJoin = 'round'; X.lineCap = 'round'; X.strokeStyle = col; X.lineWidth = lw; X.stroke(p); return p; }

// ---------- Schraffur ----------
const PAT = new Map();
// Linien 3x+2y=c (≈56° steigend) nahtlos auf 240er Kachel; c = Abstand-Schritt
function hatchTile(col, c, lw, jit = .5) {
  const key = col + c + lw; if (PAT.has(key)) return PAT.get(key);
  const T = 240, cvs = mk(T, T), g = cvs.getContext('2d'); g.strokeStyle = col; g.lineCap = 'round';
  for (let k = -60; k < 60; k++) { const cc = k * c; // Linie 3x+2y=cc
    for (const ox of [-T, 0, T]) for (const oy of [-T, 0, T]) {
      const id = ((k % (720 / c)) + 720 / c) % (720 / c);
      const x0 = (cc - 2 * (T + 20)) / 3, y0 = T + 20, x1 = (cc + 40) / 3, y1 = -20;
      g.lineWidth = lw * (.75 + .5 * hash(id * 3.1)); g.globalAlpha = .55 + .45 * hash(id * 7.7);
      g.beginPath(); g.moveTo(x0 + ox, y0 + oy); g.lineTo(x1 + ox + jit * n1(id), y1 + oy); g.stroke(); }
  }
  const pat = X.createPattern(cvs, 'repeat'); PAT.set(key, pat); return pat;
}
// Schraffiert Fläche p (optional nur innerhalb region)
function hatch(p, col, c = 20, lw = 1.2, alpha = 1, region = null) {
  X.save(); X.clip(p); if (region) X.clip(region); X.globalAlpha *= alpha; X.fillStyle = hatchTile(col, c, lw); X.fillRect(-4000, -4000, 8000, 8000); X.restore();
}
// Schattenseite: Halbebene rechts/unten einer schrägen Kante durch (x,y)
function sideRegion(x, y, ang = -1.1) { const c = Math.cos(ang), sn = Math.sin(ang), L = 3000, nx = -sn, ny = c, p = new Path2D(); p.moveTo(x - c * L, y - sn * L); p.lineTo(x + c * L, y + sn * L); p.lineTo(x + c * L + nx * L, y + sn * L + ny * L); p.lineTo(x - c * L + nx * L, y - sn * L + ny * L); p.closePath(); return p; }
// Schraffierter Schlagschatten am Boden
function castShadow(cx, cy, w, h = 16, a = .7) { const p = S('cs' + w + '_' + h, () => ellP(0, 0, w / 2, h / 2, 6), .8); X.save(); X.translate(cx, cy); hatch(p, P.ink, 12, 1.1, a); X.restore(); }
// Schraffierter Versatzschatten für Tafeln/Fenster
function dropHatch(p, dx = 12, dy = 14, a = .55) { X.save(); X.translate(dx, dy); hatch(p, P.ink2, 12, 1.1, a); X.restore(); }

// ---------- Papierwelt ----------
let GRAIN_P, GRAIN_B, SPECK_P, SPECK_B;
function makeGrain() {
  const mkN = (amp, seed) => { const w = 1920, h = 1080, c = mk(w, h), g = c.getContext('2d'), im = g.createImageData(w, h), d = im.data, R = rng(seed);
    for (let i = 0; i < w * h; i++) { const v = 128 + (R() + R() + R() - 1.5) * amp; d[i * 4] = d[i * 4 + 1] = d[i * 4 + 2] = v; d[i * 4 + 3] = 255; } g.putImageData(im, 0, 0); return c; };
  GRAIN_P = mkN(60, 11); GRAIN_B = mkN(70, 12);
  const sp = (dark, seed, n) => { const c = mk(1920, 1080), g = c.getContext('2d'), R = rng(seed);
    for (let i = 0; i < n; i++) { const x = R() * 1920, y = R() * 1080, r = .5 + R() * R() * 1.6; g.fillStyle = dark ? `rgba(70,55,40,${.18 + R() * .35})` : `rgba(210,215,255,${.05 + R() * .18})`; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); }
    // Fasern
    if (dark) for (let i = 0; i < 260; i++) { const x = R() * 1920, y = R() * 1080, a = R() * 7, l = 3 + R() * 9; g.strokeStyle = `rgba(90,70,50,${.06 + R() * .1})`; g.lineWidth = .7; g.beginPath(); g.moveTo(x, y); g.quadraticCurveTo(x + Math.cos(a) * l, y + Math.sin(a) * l * .3, x + Math.cos(a + .4) * l * 1.6, y + Math.sin(a + .4) * l); g.stroke(); }
    return c; };
  SPECK_P = sp(true, 21, 2600); SPECK_B = sp(false, 22, 1800);
}
function paperBG(t, stripe, drift = 38) {
  X.fillStyle = P.paper; X.fillRect(0, 0, W, H);
  X.save(); X.translate(W / 2, H / 2); X.rotate(-29.8 * Math.PI / 180);
  const per = 280, off = ((t * drift) % per + per) % per; X.fillStyle = stripe;
  for (let k = -9; k <= 9; k++) { X.fillRect(-1600, k * per + off - 70, 3200, 140); }
  X.restore();
}
function paperGrain() { X.save(); X.globalCompositeOperation = 'overlay'; X.globalAlpha = .32; X.drawImage(GRAIN_P, 0, 0); X.restore(); X.drawImage(SPECK_P, 0, 0); }
// Konstruktionskreis mit Skalenstrichen und Fadenkreuz (grau, fein)
function constr(cx, cy, r, rot = 0, a = .4, col = '#8b8373') {
  X.save(); X.translate(cx, cy); X.strokeStyle = col; X.globalAlpha *= a; X.lineWidth = 1.2;
  X.beginPath(); X.arc(0, 0, r, 0, 7); X.stroke();
  X.rotate(rot); X.beginPath();
  for (let i = 0; i < 120; i++) { const an = i / 120 * Math.PI * 2, l = i % 10 === 0 ? 16 : 7; X.moveTo(Math.cos(an) * r, Math.sin(an) * r); X.lineTo(Math.cos(an) * (r + l), Math.sin(an) * (r + l)); }
  X.stroke(); X.rotate(-rot);
  X.globalAlpha *= .6; X.beginPath(); X.moveTo(-r * 1.3, 0); X.lineTo(r * 1.3, 0); X.moveTo(0, -r * 1.3); X.lineTo(0, r * 1.3); X.stroke();
  X.setLineDash([6, 8]); X.beginPath(); X.arc(0, 0, r * .62, 0, 7); X.stroke(); X.setLineDash([]);
  X.restore();
}
// Boden: Tuschelinie, Grasbüschel, Kiesel, Punktierung
function ground(y, x0, x1, seed = 1, grassEvery = 140, soil = 0) {
  if (soil) { const p = S('soil' + x0 + '_' + y, () => polyP([[x0, y], [x1, y], [x1, y + soil], [x0, y + soil]], true, 30), 2); X.save(); X.fillStyle = hexA('#dcc9a2', .55); X.fill(p); hatch(p, P.ink2, 20, 1, .18); X.restore(); }
  line(polyP([[x0, y], [x1, y]], false, 12), 2.6, P.ink, 'gr' + x0 + '_' + x1 + '_' + y, 1.2);
  const R = rng(seed); X.save();
  for (let x = x0 + 30; x < x1; x += grassEvery * (.6 + R() * .8)) { // Grasbüschel
    const n = 3 + (R() * 3 | 0); X.strokeStyle = P.grass; X.lineWidth = 2; X.lineCap = 'round'; X.beginPath();
    for (let i = 0; i < n; i++) { const dx = (i - n / 2) * 4, h = 10 + R() * 12; X.moveTo(x + dx, y); X.quadraticCurveTo(x + dx + (R() - .5) * 6, y - h * .6, x + dx + (i - n / 2) * 3, y - h); }
    X.stroke(); X.strokeStyle = hexA(P.ink, .55); X.lineWidth = 1; X.stroke(); }
  for (let x = x0 + 20; x < x1; x += 60 + R() * 160) { const yy = y + 8 + R() * 30, rx = 4 + R() * 6; X.beginPath(); X.ellipse(x, yy, rx, rx * .55, 0, 0, 7); X.fillStyle = P.soil; X.fill(); X.strokeStyle = hexA(P.ink, .8); X.lineWidth = 1.4; X.stroke(); }
  X.fillStyle = hexA(P.ink, .35); for (let i = 0; i < (x1 - x0) / 5; i++) { const x = x0 + R() * (x1 - x0), yy = y + 4 + Math.pow(R(), 2) * 70; X.fillRect(x, yy, 1.6, 1.6); }
  X.strokeStyle = hexA(P.ink, .28); X.lineWidth = 1.4; X.beginPath(); for (let i = 0; i < (x1 - x0) / 90; i++) { const x = x0 + R() * (x1 - x0), yy = y + 60 + R() * 140, l = 14 + R() * 40; X.moveTo(x, yy); X.lineTo(x + l, yy); } X.stroke();
  X.restore();
}
// Wolke mit Tuschekontur und Schraffur unten
function cloud(x, y, s, key) {
  X.save(); X.translate(x, y); X.scale(s, s);
  const p = S('cl' + key, () => { const pts = []; const bumps = [[-70, 0, 30], [-35, -22, 34], [8, -30, 38], [50, -14, 30], [78, 2, 22]];
    pts.push(...ellP(-70, 4, 30, 24, 5, Math.PI * .5, Math.PI * 1.5)); pts.push(...ellP(-30, -12, 36, 34, 5, Math.PI * 1.1, Math.PI * 1.75)); pts.push(...ellP(12, -14, 42, 36, 5, Math.PI * 1.2, Math.PI * 1.85));
    pts.push(...ellP(58, 0, 30, 26, 5, Math.PI * 1.3, Math.PI * 2.4)); pts.push(...polyP([[70, 26], [-70, 28]], false, 8)); return pts; }, 1.2);
  ink(p, '#fbf8f1', 3.2); hatch(p, P.ink2, 10, 1, .5, sideRegion(0, 8, -.08)); X.restore();
}

// ---------- Blaupause ----------
function bpBG(t, cx = W / 2, cy = H * .55, rot = 0) {
  const g = X.createRadialGradient(cx, cy, 40, cx, cy, 1250); g.addColorStop(0, '#20275a'); g.addColorStop(.45, '#151a40'); g.addColorStop(1, P.navy0);
  X.fillStyle = g; X.fillRect(0, 0, W, H);
  X.save(); X.lineWidth = 1; X.strokeStyle = 'rgba(160,170,235,.055)'; X.beginPath();
  for (let x = 0; x <= W; x += 40) { X.moveTo(x + .5, 0); X.lineTo(x + .5, H); } for (let y = 0; y <= H; y += 40) { X.moveTo(0, y + .5); X.lineTo(W, y + .5); } X.stroke();
  X.strokeStyle = 'rgba(160,170,235,.09)'; X.beginPath(); for (let x = 0; x <= W; x += 200) { X.moveTo(x + .5, 0); X.lineTo(x + .5, H); } for (let y = 0; y <= H; y += 200) { X.moveTo(0, y + .5); X.lineTo(W, y + .5); } X.stroke();
  X.restore();
  for (const [r, a] of [[330, .1], [520, .08], [760, .06], [1000, .05]]) constr(cx, cy, r, rot * (r > 500 ? -1 : 1), a, '#aeb6f0');
  // Rahmenwinkel und Lineal wie im Original
  X.save(); X.strokeStyle = 'rgba(200,205,240,.3)'; X.lineWidth = 1.5; X.beginPath();
  for (const [x, y, sx, sy] of [[34, 34, 1, 1], [W - 34, 34, -1, 1], [34, H - 34, 1, -1], [W - 34, H - 34, -1, -1]]) { X.moveTo(x, y + sy * 22); X.lineTo(x, y); X.lineTo(x + sx * 22, y); }
  X.stroke(); X.strokeStyle = 'rgba(200,205,240,.16)'; X.beginPath(); X.moveTo(50, 60); X.lineTo(50, H - 60);
  for (let y = 60; y < H - 60; y += 20) { X.moveTo(50, y); X.lineTo(y % 100 === 0 ? 62 : 56, y); } X.moveTo(180, H - 42); X.lineTo(W - 180, H - 42); X.stroke(); X.restore();
}
function bpGrain() { X.save(); X.globalCompositeOperation = 'overlay'; X.globalAlpha = .22; X.drawImage(GRAIN_B, 0, 0); X.restore(); X.drawImage(SPECK_B, 0, 0); }
// leuchtende Linie
function glow(p, col, lw = 2, blur = 14, a = 1) { X.save(); X.globalAlpha *= a; X.lineJoin = 'round'; X.lineCap = 'round'; X.shadowColor = col; X.shadowBlur = blur; X.strokeStyle = col; X.lineWidth = lw; X.stroke(p); X.shadowBlur = 0; X.restore(); }
function bpStroke(p, a = 1, lw = 2) { X.save(); X.globalAlpha *= a; X.lineJoin = 'round'; X.lineCap = 'round'; X.strokeStyle = P.lav; X.lineWidth = lw; X.shadowColor = 'rgba(190,200,255,.55)'; X.shadowBlur = 6; X.stroke(p); X.restore(); }
// Funkeln (4-Strahl-Stern mit Hof)
function spark(x, y, s, a = 1, col = '#ffffff') {
  if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y);
  const g = X.createRadialGradient(0, 0, 0, 0, 0, s * 1.4); g.addColorStop(0, 'rgba(255,255,255,.9)'); g.addColorStop(.25, hexA('#c9d4ff', .35)); g.addColorStop(1, 'rgba(160,180,255,0)'); X.fillStyle = g; X.fillRect(-s * 1.5, -s * 1.5, s * 3, s * 3);
  X.fillStyle = col; X.beginPath(); const w = s * .13; X.moveTo(0, -s); X.quadraticCurveTo(w, -w, s, 0); X.quadraticCurveTo(w, w, 0, s); X.quadraticCurveTo(-w, w, -s, 0); X.quadraticCurveTo(-w, -w, 0, -s); X.fill(); X.restore();
}
// Punkt entlang eines Polylinienzugs (für Lichtpakete und Zeichnen-Animation)
function polyLen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
function polyAt(pts, k) { const L = polyLen(pts) * clamp(k); let s = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); if (s + d >= L) { const u = d ? (L - s) / d : 0; return [mix(pts[i - 1][0], pts[i][0], u), mix(pts[i - 1][1], pts[i][1], u), Math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])]; } s += d; } const q = pts[pts.length - 1]; return [q[0], q[1], 0]; }
function polySub(pts, k0, k1) { const L = polyLen(pts), a = L * clamp(k0), b = L * clamp(k1), out = []; let s = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (s + d >= a && s <= b) { const u0 = clamp((a - s) / (d || 1)), u1 = clamp((b - s) / (d || 1)); if (!out.length) out.push([mix(pts[i - 1][0], pts[i][0], u0), mix(pts[i - 1][1], pts[i][1], u0)]); out.push([mix(pts[i - 1][0], pts[i][0], u1), mix(pts[i - 1][1], pts[i][1], u1)]); }
    s += d; } return out; }
function pathOf(pts) { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); return p; }
function arrowHead(x, y, ang, s, col, lw = 2) { X.save(); X.translate(x, y); X.rotate(ang); X.strokeStyle = col; X.lineWidth = lw; X.lineCap = 'round'; X.beginPath(); X.moveTo(-s, -s * .6); X.lineTo(0, 0); X.lineTo(-s, s * .6); X.stroke(); X.restore(); }

// ---------- Schrift ----------
function rr(g, x, y, w, h, r) { r = Math.max(0, Math.min(r, w / 2, h / 2)); g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
// Getippte Schlagzeile im Stil der Original-Titel (Inter SemiBold, Unterstrich-Marker).
// segs: [{s, k}] – jedes Segment ist spätestens bei k vollständig getippt (Tippen beginnt dur vor k).
// o: {x, y, size, col, ul:[i0,i1] Zeichenbereich für Unterstrich, ulCol, hi:{i0,i1,col}, out: Zeit zum Löschen, caret}
function headline(t, segs, o) {
  const full = segs.map(s => s.s).join(''); let shown = 0, acc = 0, start = 1e9;
  for (const sg of segs) { const n = sg.s.length, d = sg.d ?? Math.min(.34, .045 * n + .08), p = lin(t, sg.k - d, sg.k); start = Math.min(start, sg.k - d); shown = p > 0 ? acc + Math.round(n * p) : shown; acc += n; }
  if (t < start) return; let vis = shown;
  if (o.out != null && t > o.out) { vis = Math.round(shown * (1 - lin(t, o.out, o.out + .16))); if (vis <= 0) return; }
  X.save(); X.font = `600 ${o.size}px IN`; X.letterSpacing = (o.ls ?? -1) + 'px'; X.textBaseline = 'alphabetic';
  const txt = full.slice(0, vis), x = o.x, y = o.y;
  if (o.ul && vis >= o.ul[1]) { const a = X.measureText(full.slice(0, o.ul[0])).width, b = X.measureText(full.slice(0, o.ul[1])).width, k = eo(lin(t, (o.ulK ?? segs[segs.length - 1].k) - .18, o.ulK ?? segs[segs.length - 1].k));
    X.fillStyle = o.ulCol || P.under; rr(X, x + a - 2, y + o.size * .2, (b - a + 4) * k, o.size * .085 + 2, 3); X.fill(); }
  if (o.hi) { const a = X.measureText(full.slice(0, o.hi[0])).width; X.fillStyle = o.col; X.fillText(full.slice(0, Math.min(vis, o.hi[0])), x, y); if (vis > o.hi[0]) { X.fillStyle = o.hi[2]; X.fillText(full.slice(o.hi[0], vis), x + a, y); } }
  else { X.fillStyle = o.col; X.fillText(txt, x, y); }
  const tl = segs[segs.length - 1].k; if (o.caret !== false && ((vis < full.length && (o.out == null || t < o.out)) || (t < tl + .5 && Math.floor(t * 4) % 2 === 0))) { const w = X.measureText(txt).width; X.fillStyle = o.caretCol || P.dash; X.fillRect(x + w + 6, y - o.size * .76, 3.5, o.size * .9); }
  X.restore();
}
function mono(s, x, y, size, col, align = 'left', a = 1) { X.save(); X.globalAlpha *= a; X.font = `${size}px PM`; X.textAlign = align; X.fillStyle = col; X.fillText(s, x, y); X.restore(); }
// Etikett wie die Tag-Pillen des Originals (<body>): Papier = Creme mit Tusche, Blaupause = Linie
function tagP(s, x, y, size, a = 1, n = null) { if (a <= 0) return; const txt = n == null ? s : s.slice(0, n); X.save(); X.globalAlpha *= clamp(a); X.font = `${size}px PM`; const w = X.measureText(s).width + size * 1.1, h = size * 1.55;
  const p = S('tag' + s + size, () => rrP(-w / 2, -h / 2, w, h, h / 2, 4), .7); X.translate(x, y); ink(p, P.win, 2.6); X.fillStyle = P.ink; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText(txt.padEnd(s.length, ' '), 0, 1); X.restore(); }
function tagB(s, x, y, size, a = 1, col = P.lav, n = null) { if (a <= 0) return; const txt = n == null ? s : s.slice(0, n); X.save(); X.globalAlpha *= clamp(a); X.font = `${size}px PM`; const w = X.measureText(s).width + size * 1.1, h = size * 1.6;
  X.translate(x, y); rr(X, -w / 2, -h / 2, w, h, h / 2); X.fillStyle = 'rgba(14,17,44,.75)'; X.fill(); X.strokeStyle = col; X.lineWidth = 1.6; X.shadowColor = col; X.shadowBlur = 8; X.stroke(); X.shadowBlur = 0;
  X.fillStyle = '#eef0ff'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText(txt.padEnd(s.length, ' '), 0, 1); X.restore(); }
// Aufmerksamkeitsring (dünner Kreis, der sich ausdehnt)
function ring(x, y, t, t0, r0 = 20, r1 = 140, col = P.mag, dur = .7, lw = 2) { const k = lin(t, t0, t0 + dur); if (k <= 0 || k >= 1) return; X.save(); X.globalAlpha = (1 - k) * .9; X.strokeStyle = col; X.lineWidth = lw; X.beginPath(); X.arc(x, y, mix(r0, r1, eo(k)), 0, 7); X.stroke(); X.restore(); }
function cam(s, cx, cy, sx = W / 2, sy = H / 2) { X.translate(sx, sy); X.scale(s, s); X.translate(-cx, -cy); }
// Blaupausen-Details wie im Original: Skalenring um Symbole, Knotenpunkte, Maßlinien
function tickRing(x, y, r, a = 1, rot = 0, col = P.lav) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y); X.rotate(rot); X.strokeStyle = col; X.lineWidth = 1.3; X.globalAlpha *= .75;
  X.beginPath(); X.arc(0, 0, r, 0, 7); X.stroke(); X.beginPath(); for (let i = 0; i < 48; i++) { const an = i / 48 * Math.PI * 2, l = i % 4 ? 5 : 10; X.moveTo(Math.cos(an) * (r + 3), Math.sin(an) * (r + 3)); X.lineTo(Math.cos(an) * (r + 3 + l), Math.sin(an) * (r + 3 + l)); } X.stroke(); X.restore(); }
function nodeDot(x, y, a = 1, col = P.lav) { X.save(); X.globalAlpha *= a; X.strokeStyle = col; X.lineWidth = 1.6; X.fillStyle = P.navy0; X.beginPath(); X.arc(x, y, 5, 0, 7); X.fill(); X.stroke(); X.restore(); }
function dimLine(x1, y1, x2, y2, a = 1, col = 'rgba(205,209,243,.55)') { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.strokeStyle = col; X.lineWidth = 1.3; const ang = Math.atan2(y2 - y1, x2 - x1), nx = -Math.sin(ang) * 10, ny = Math.cos(ang) * 10;
  X.beginPath(); X.moveTo(x1 - nx, y1 - ny); X.lineTo(x1 + nx, y1 + ny); X.moveTo(x2 - nx, y2 - ny); X.lineTo(x2 + nx, y2 + ny); X.moveTo(x1, y1); X.lineTo(x2, y2);
  const L = Math.hypot(x2 - x1, y2 - y1); for (let s = 20; s < L; s += 20) { const px = x1 + Math.cos(ang) * s, py = y1 + Math.sin(ang) * s; X.moveTo(px, py); X.lineTo(px + nx * .4, py + ny * .4); } X.stroke();
  arrowHead(x1, y1, ang + Math.PI, 8, col, 1.3); arrowHead(x2, y2, ang, 8, col, 1.3); X.restore(); }
