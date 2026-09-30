// Grundwerkzeuge im Strich von „A short story about a watermelon“ (Claude/Kevin Ngo):
// feine dunkle Kontur (2,5–3,5 px), Flächen mit Textur (Kritzel, Zellen, Schraffur), Querschnitt durch die Erde,
// blaue Konstruktionslinien, Creme-Papier mit breiten, fein schraffierten Diagonalstreifen. Deterministisch.
const W = 1920, H = 1080;
const cv = document.getElementById('c'), X = cv.getContext('2d');
const P = {
  paper: '#f3efe0', stripe: '#eedfc2', ink: '#1b1a22', inkS: '#3a3540',
  soil: '#997558', soilD: '#6f4f3a', soilL: '#ad9076', pebble: '#c9a878', strata: '#6b4630', compact: '#7a6353', compactD: '#56443a',
  topsoil: '#4b3326', topsoilL: '#6a4a36', gravel: '#c4b9a6', gravelD: '#8f8575',
  lawn: '#b8da9c', lawnD: '#86b86a', grass: '#5c8f48', dry: '#d6bf7c', dryD: '#a8894a',
  blue: '#4f78d0', blueL: '#9db4ea', sun: '#eba84f', sunS: '#e2703a', ray: '#d99a2c',
  navy: '#333571', navyD: '#25274e', navyH: '#2a2c63', rainL: '#bfc4f2', water: '#5d7fd6', waterL: '#b3c8f4',
  ant: '#5b3527', antD: '#3a2119', antL: '#7a4a35', leaf: '#8fbc6b', leafD: '#4f7d33', red: '#c9443a', skin: '#f2c9a4', skinD: '#d9a27c',
  wood: '#b98a5a', woodD: '#7e5634', metal: '#a4adb8', metalD: '#6d7682', worm: '#e79d98', wormD: '#b86a6a'
};
// Nacht-/Regenmodus: Flächen dunkler ins Blau, Konturen hell (wie das Gewitter im Original)
let NIGHT = 0;
const F = c => NIGHT ? mixCol(c, '#2b2d62', .62 * NIGHT) : c;
const OL = () => NIGHT ? '#e9e7f4' : P.ink;
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

// ---------- Schraffur ----------
// ---------- Tusche ----------
function ink(p, fill, lw = 3, col = null) {
  if (fill) { X.fillStyle = F(fill); X.fill(p); }
  if (lw) { X.lineJoin = 'round'; X.lineCap = 'round'; X.strokeStyle = col || OL(); X.lineWidth = lw; X.stroke(p); }
}
function line(pts, lw = 3, col = null, key = null, amp = .6) { const p = key ? S(key, () => pts, amp, false) : wob(pts, false, amp, 3); X.lineJoin = 'round'; X.lineCap = 'round'; X.strokeStyle = col || OL(); X.lineWidth = lw; X.stroke(p); return p; }
// ---------- Schraffur ----------
const PAT = new Map();
// Linien a*x+b*y=c nahtlos auf 240er Kachel (240a und 240b müssen Vielfache von c sein)
function hatchTile(col, c, lw, a = 3, b = 2) {
  const key = [col, c, lw, a, b].join('|'); if (PAT.has(key)) return PAT.get(key);
  const T = 240, cvs = mk(T, T), g = cvs.getContext('2d'); g.strokeStyle = col; g.lineCap = 'round';
  const n = Math.round(T * (Math.abs(a) + Math.abs(b)) / c) + 4;
  for (let k = -n; k <= n; k++) { const cc = k * c; g.lineWidth = lw * (.8 + .4 * hash(((k % 97) + 97) % 97)); g.globalAlpha = .6 + .4 * hash(((k % 89) + 89) % 89 + 7);
    for (const ox of [-T, 0, T]) for (const oy of [-T, 0, T]) { g.beginPath();
      if (Math.abs(b) > Math.abs(a)) { const y0 = (cc - a * -20) / b, y1 = (cc - a * (T + 20)) / b; g.moveTo(-20 + ox, y0 + oy); g.lineTo(T + 20 + ox, y1 + oy); }
      else { const x0 = (cc - b * -20) / a, x1 = (cc - b * (T + 20)) / a; g.moveTo(x0 + ox, -20 + oy); g.lineTo(x1 + ox, T + 20 + oy); }
      g.stroke(); } }
  const pat = X.createPattern(cvs, 'repeat'); PAT.set(key, pat); return pat;
}
function hatch(p, col, c = 20, lw = 1.2, alpha = 1, region = null, a = 3, b = 2) {
  X.save(); X.clip(p); if (region) X.clip(region); X.globalAlpha *= alpha; X.fillStyle = hatchTile(col, c, lw, a, b); X.fillRect(-6000, -6000, 12000, 12000); X.restore();
}
function sideRegion(x, y, ang = -1.1) { const c = Math.cos(ang), sn = Math.sin(ang), L = 4000, nx = -sn, ny = c, p = new Path2D(); p.moveTo(x - c * L, y - sn * L); p.lineTo(x + c * L, y + sn * L); p.lineTo(x + c * L + nx * L, y + sn * L + ny * L); p.lineTo(x - c * L + nx * L, y - sn * L + ny * L); p.closePath(); return p; }
function polyLen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
function polyAt(pts, k) { const L = polyLen(pts) * clamp(k); let s = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); if (s + d >= L) { const u = d ? (L - s) / d : 0; return [mix(pts[i - 1][0], pts[i][0], u), mix(pts[i - 1][1], pts[i][1], u), Math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])]; } s += d; } const q = pts[pts.length - 1]; return [q[0], q[1], 0]; }
function polySub(pts, k0, k1) { const L = polyLen(pts), a = L * clamp(k0), b = L * clamp(k1), out = []; let s = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (s + d >= a && s <= b) { const u0 = clamp((a - s) / (d || 1)), u1 = clamp((b - s) / (d || 1)); if (!out.length) out.push([mix(pts[i - 1][0], pts[i][0], u0), mix(pts[i - 1][1], pts[i][1], u0)]); out.push([mix(pts[i - 1][0], pts[i][0], u1), mix(pts[i - 1][1], pts[i][1], u1)]); }
    s += d; } return out; }
function pathOf(pts) { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); return p; }
function arrowHead(x, y, ang, s, col, lw = 2) { X.save(); X.translate(x, y); X.rotate(ang); X.strokeStyle = col; X.lineWidth = lw; X.lineCap = 'round'; X.beginPath(); X.moveTo(-s, -s * .6); X.lineTo(0, 0); X.lineTo(-s, s * .6); X.stroke(); X.restore(); }

function rr(g, x, y, w, h, r) { r = Math.max(0, Math.min(r, w / 2, h / 2)); g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function cam(s, cx, cy, sx = W / 2, sy = H / 2) { X.translate(sx, sy); X.scale(s, s); X.translate(-cx, -cy); }
function spark(x, y, s, a = 1, col = '#ffffff') {
  if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y);
  const g = X.createRadialGradient(0, 0, 0, 0, 0, s * 1.4); g.addColorStop(0, 'rgba(255,255,255,.9)'); g.addColorStop(.25, hexA('#c9d4ff', .35)); g.addColorStop(1, 'rgba(160,180,255,0)'); X.fillStyle = g; X.fillRect(-s * 1.5, -s * 1.5, s * 3, s * 3);
  X.fillStyle = col; X.beginPath(); const w = s * .13; X.moveTo(0, -s); X.quadraticCurveTo(w, -w, s, 0); X.quadraticCurveTo(w, w, 0, s); X.quadraticCurveTo(-w, w, -s, 0); X.quadraticCurveTo(-w, -w, 0, -s); X.fill(); X.restore();
}

// ---------- Papier ----------
let GRAIN, SPECK;
function makeGrain() {
  const w = 1920, h = 1080, c = mk(w, h), g = c.getContext('2d'), im = g.createImageData(w, h), d = im.data, R = rng(31);
  for (let i = 0; i < w * h; i++) { const v = 128 + (R() + R() + R() - 1.5) * 34; d[i * 4] = d[i * 4 + 1] = d[i * 4 + 2] = v; d[i * 4 + 3] = 255; } g.putImageData(im, 0, 0); GRAIN = c;
  const s = mk(w, h), q = s.getContext('2d'), R2 = rng(32); for (let i = 0; i < 1500; i++) { q.fillStyle = `rgba(120,100,80,${.08 + R2() * .18})`; q.beginPath(); q.arc(R2() * w, R2() * h, .6 + R2() * 1.1, 0, 7); q.fill(); } SPECK = s;
}
// Creme-Papier mit breiten, fein schraffierten Streifen (fallend, ca. 40°)
function paperBG(t, drift = 30, tint = null) {
  X.fillStyle = tint || P.paper; X.fillRect(0, 0, W, H);
  X.save(); X.translate(W / 2, H / 2); X.rotate(40 * Math.PI / 180);
  const per = 330, off = ((t * drift) % per + per) % per;
  for (let k = -8; k <= 8; k++) { X.fillStyle = hexA('#efdcbb', .55); X.fillRect(-1800, k * per + off - 70, 3600, 140); }
  X.save(); X.beginPath(); for (let k = -8; k <= 8; k++) X.rect(-1800, k * per + off - 70, 3600, 140); X.clip();
  X.strokeStyle = hexA('#e3c9a0', .55); X.lineWidth = 1.3; X.beginPath(); for (let y = -1400; y < 1400; y += 5) { X.moveTo(-1800, y + off % 5); X.lineTo(1800, y + off % 5); } X.stroke(); X.restore();
  X.restore();
}
function grain(a = .22) { X.save(); X.globalCompositeOperation = 'overlay'; X.globalAlpha = a; X.drawImage(GRAIN, 0, 0); X.restore(); X.drawImage(SPECK, 0, 0); }
// Nacht mit Regen: Nachtblau mit feiner Diagonalschraffur + Regenstriche
function nightBG(t) {
  X.fillStyle = P.navy; X.fillRect(0, 0, W, H);
  X.save(); X.strokeStyle = hexA('#1e2050', .7); X.lineWidth = 1.6; X.beginPath(); for (let x = -1200; x < W + 200; x += 26) { X.moveTo(x, 0); X.lineTo(x + 1100, H); } X.stroke(); X.restore();
}
function rain(t, a = 1, dens = 1, col = P.rainL) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.strokeStyle = col; X.lineWidth = 2; X.lineCap = 'round'; X.beginPath();
  for (let i = 0; i < 170 * dens; i++) { const x0 = hash(i * 1.3) * 2300 - 200, sp = 1300 + hash(i * 2.7) * 500, y = ((hash(i * 5.1) * 1300 + t * sp) % 1300) - 100, l = 18 + hash(i) * 26; X.moveTo(x0 - y * .18, y); X.lineTo(x0 - (y + l) * .18, y + l); }
  X.stroke(); X.restore(); }

// ---------- Erde im Querschnitt ----------
// Erdfläche p: Grundfarbe, flache Diagonalschraffur, Sprenkel, dunkle Klumpen, Kiesel mit Kontur und Glanzpunkt
function soilFill(p, base, seed, box, o = {}) {
  X.save(); X.fillStyle = F(base); X.fill(p); X.clip(p);
  X.globalAlpha = o.hatchA ?? .55; X.fillStyle = hatchTile(mixCol(base, '#2a1a10', .35), o.hc ?? 48, 1.4, 1, 3); X.fillRect(-6000, -6000, 12000, 12000); X.globalAlpha = 1;
  const [x0, y0, x1, y1] = box, R = rng(seed), A = (x1 - x0) * (y1 - y0);
  X.fillStyle = hexA(mixCol(base, '#1a0f08', .45), .55); for (let i = 0; i < A / 900; i++) { X.fillRect(x0 + R() * (x1 - x0), y0 + R() * (y1 - y0), 1.8, 1.8); }
  X.fillStyle = hexA(mixCol(base, '#1a0f08', .25), .8); for (let i = 0; i < A / (o.clumpEvery ?? 16000); i++) { const x = x0 + R() * (x1 - x0), y = y0 + R() * (y1 - y0), r = 5 + R() * 12; X.beginPath(); X.ellipse(x, y, r, r * (.7 + R() * .3), R() * 3, 0, 7); X.fill(); }
  if (o.pebbles !== false) for (let i = 0; i < A / (o.pebEvery ?? 30000); i++) { const x = x0 + R() * (x1 - x0), y = y0 + R() * (y1 - y0), r = 12 + R() * 12, fl = o.flat ?? 1; pebble(x, y, r, r * .8 * fl, R() * .6 - .3); }
  X.restore();
}
function pebble(x, y, rx, ry, rot = 0, col = P.pebble) { X.save(); X.translate(x, y); X.rotate(rot); X.beginPath(); X.ellipse(0, 0, rx, ry, 0, 0, 7); X.fillStyle = F(col); X.fill(); X.strokeStyle = OL(); X.lineWidth = 2.6; X.stroke();
  X.fillStyle = 'rgba(255,255,255,.75)'; X.beginPath(); X.arc(-rx * .35, -ry * .35, Math.max(2, rx * .16), 0, 7); X.fill(); X.restore(); }
function strata(y, x0, x1, seed, col = P.strata, a = .85) { const pts = []; for (let x = x0; x <= x1; x += 20) pts.push([x, y + Math.sin(x * .004 + seed) * 12 + Math.sin(x * .011 + seed * 2) * 5]); X.save(); X.globalAlpha *= a; X.strokeStyle = F(col); X.lineWidth = 3.2; X.lineCap = 'round'; X.stroke(pathOf(pts)); X.restore(); }
// Grasnarbe: Linie + einzelne feine Halme
function grassLine(y, x0, x1, t, col = P.grass, h = 30, dens = 1, wilt = 0, seed = 1) {
  X.save(); X.lineCap = 'round';
  for (let i = 0; i < (x1 - x0) / 7 * dens; i++) { const x = x0 + hash(i * 3.1 + seed) * (x1 - x0), hh = h * (.5 + hash(i * 1.7 + seed) * .7), lean = (hash(i * 9.3) - .5) * .5 + Math.sin(t * 2 + x * .01) * .06;
    const bend = wilt * (.6 + hash(i) * .6); X.strokeStyle = F(mixCol(col, P.dryD, wilt)); X.lineWidth = 1.8; X.beginPath(); X.moveTo(x, y);
    X.quadraticCurveTo(x + lean * hh * .5, y - hh * .6, x + lean * hh + bend * hh * .9, y - hh * (1 - bend * .75)); X.stroke(); }
  X.strokeStyle = OL(); X.lineWidth = 3; X.beginPath(); X.moveTo(x0, y); X.lineTo(x1, y); X.stroke(); X.restore();
}
// Blaue Konstruktionslinien
function bArc(x, y, r, a0, a1, a = 1, dash = null, lw = 2) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.strokeStyle = NIGHT ? P.blueL : P.blue; X.lineWidth = lw; if (dash) X.setLineDash(dash); X.beginPath(); X.arc(x, y, r, a0, a1); X.stroke(); X.restore(); }
function bLine(pts, a = 1, dash = null, lw = 2) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.strokeStyle = NIGHT ? P.blueL : P.blue; X.lineWidth = lw; X.lineCap = 'round'; if (dash) X.setLineDash(dash); X.stroke(pathOf(pts)); X.restore(); }
function bCross(x, y, s = 10, a = 1) { bLine([[x - s, y], [x + s, y]], a, null, 1.6); bLine([[x, y - s], [x, y + s]], a, null, 1.6); }
// Stoßlinien (kurze schwarze Striche wie beim Aufprall im Original)
function burst(x, y, r0, r1, n, a = 1, rot = 0, col = null) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.strokeStyle = col || OL(); X.lineWidth = 2.6; X.lineCap = 'round'; X.beginPath(); for (let i = 0; i < n; i++) { const an = rot + i / n * Math.PI * 2; X.moveTo(x + Math.cos(an) * r0, y + Math.sin(an) * r0); X.lineTo(x + Math.cos(an) * r1, y + Math.sin(an) * r1); } X.stroke(); X.restore(); }
// Strichliste in Blau
function tally(x, y, n, a = 1) { X.save(); X.globalAlpha *= a; X.strokeStyle = P.blue; X.lineWidth = 3; X.lineCap = 'round'; X.beginPath(); for (let i = 0; i < n; i++) { const g = Math.floor(i / 5), k = i % 5, gx = x + g * 64; if (k < 4) { X.moveTo(gx + k * 11, y); X.lineTo(gx + k * 11 + 2, y + 44); } else { X.moveTo(gx - 6, y + 34); X.lineTo(gx + 44, y + 8); } } X.stroke(); X.restore(); }

// ---------- Schrift: Handschrift wie das „claude“-Signet, erscheint wie geschrieben ----------
// segs [{s, k, d}] – jedes Segment ist bei k vollständig; o: {x, y, size, col, ul:[i0,i1], ulK, hi:[i0,i1,col], out}
function headline(t, segs, o) {
  let start = 1e9; for (const sg of segs) start = Math.min(start, sg.k - (sg.d ?? .3)); if (t < start) return;
  const full = segs.map(s => s.s).join(''); X.save(); X.font = `700 ${o.size}px KA`; X.textBaseline = 'alphabetic';
  const oa = o.out != null ? 1 - lin(t, o.out, o.out + .2) : 1; if (oa <= 0) { X.restore(); return; } X.globalAlpha = oa;
  let acc = 0; const wAll = X.measureText(full).width; let revealW = 0;
  for (const sg of segs) { const d = sg.d ?? .3, p = eo(lin(t, sg.k - d, sg.k)), a = X.measureText(full.slice(0, acc)).width, b = X.measureText(full.slice(0, acc + sg.s.length)).width; if (p > 0) revealW = a + (b - a) * p; acc += sg.s.length; }
  X.save(); X.beginPath(); X.rect(o.x - 20, o.y - o.size * 1.2, revealW + 22, o.size * 1.7); X.clip();
  const col = o.col || OL();
  if (o.hi) { const a = X.measureText(full.slice(0, o.hi[0])).width; X.fillStyle = col; X.fillText(full.slice(0, o.hi[0]), o.x, o.y); X.fillStyle = o.hi[2]; X.fillText(full.slice(o.hi[0], o.hi[1]), o.x + a, o.y); const b2 = X.measureText(full.slice(0, o.hi[1])).width; X.fillStyle = col; X.fillText(full.slice(o.hi[1]), o.x + b2, o.y); }
  else { X.fillStyle = col; X.fillText(full, o.x, o.y); }
  X.restore();
  if (o.ul) { const a = X.measureText(full.slice(0, o.ul[0])).width, b = X.measureText(full.slice(0, o.ul[1])).width, k = eo(lin(t, (o.ulK ?? segs[segs.length - 1].k) - .2, o.ulK ?? segs[segs.length - 1].k));
    if (k > 0) { const pts = []; for (let i = 0; i <= 24 * k; i++) { const u = i / 24; pts.push([o.x + a + (b - a) * u, o.y + o.size * .22 + Math.sin(u * 5 + 1) * 3 - u * 4]); } X.strokeStyle = o.ulCol || (NIGHT ? P.blueL : P.blue); X.lineWidth = o.size * .07; X.lineCap = 'round'; X.lineJoin = 'round'; X.stroke(pathOf(pts)); } }
  X.restore();
}
function hand(s, x, y, size, col, align = 'left', a = 1) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.font = `700 ${size}px KA`; X.textAlign = align; X.fillStyle = col; X.fillText(s, x, y); X.restore(); }
function ring(x, y, t, t0, r0 = 20, r1 = 140, col = P.blue, dur = .7, lw = 2) { const k = lin(t, t0, t0 + dur); if (k <= 0 || k >= 1) return; X.save(); X.globalAlpha = (1 - k) * .9; X.strokeStyle = col; X.lineWidth = lw; X.beginPath(); X.arc(x, y, mix(r0, r1, eo(k)), 0, 7); X.stroke(); X.restore(); }
