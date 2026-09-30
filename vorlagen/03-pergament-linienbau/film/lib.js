const W = 1920, H = 1080;
const cv = document.getElementById('c'), X = cv.getContext('2d');
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

function polyLen(pts) { let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); return L; }
function polyAt(pts, k) { const L = polyLen(pts) * clamp(k); let s = 0; for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); if (s + d >= L) { const u = d ? (L - s) / d : 0; return [mix(pts[i - 1][0], pts[i][0], u), mix(pts[i - 1][1], pts[i][1], u), Math.atan2(pts[i][1] - pts[i - 1][1], pts[i][0] - pts[i - 1][0])]; } s += d; } const q = pts[pts.length - 1]; return [q[0], q[1], 0]; }
function polySub(pts, k0, k1) { const L = polyLen(pts), a = L * clamp(k0), b = L * clamp(k1), out = []; let s = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (s + d >= a && s <= b) { const u0 = clamp((a - s) / (d || 1)), u1 = clamp((b - s) / (d || 1)); if (!out.length) out.push([mix(pts[i - 1][0], pts[i][0], u0), mix(pts[i - 1][1], pts[i][1], u0)]); out.push([mix(pts[i - 1][0], pts[i][0], u1), mix(pts[i - 1][1], pts[i][1], u1)]); }
    s += d; } return out; }
function pathOf(pts) { const p = new Path2D(); pts.forEach((q, i) => i ? p.lineTo(q[0], q[1]) : p.moveTo(q[0], q[1])); return p; }
function arrowHead(x, y, ang, s, col, lw = 2) { X.save(); X.translate(x, y); X.rotate(ang); X.strokeStyle = col; X.lineWidth = lw; X.lineCap = 'round'; X.beginPath(); X.moveTo(-s, -s * .6); X.lineTo(0, 0); X.lineTo(-s, s * .6); X.stroke(); X.restore(); }

function rr(g, x, y, w, h, r) { r = Math.max(0, Math.min(r, w / 2, h / 2)); g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function spark(x, y, s, a = 1, col = '#ffffff') {
  if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y);
  const g = X.createRadialGradient(0, 0, 0, 0, 0, s * 1.4); g.addColorStop(0, 'rgba(255,255,255,.9)'); g.addColorStop(.25, hexA('#c9d4ff', .35)); g.addColorStop(1, 'rgba(160,180,255,0)'); X.fillStyle = g; X.fillRect(-s * 1.5, -s * 1.5, s * 3, s * 3);
  X.fillStyle = col; X.beginPath(); const w = s * .13; X.moveTo(0, -s); X.quadraticCurveTo(w, -w, s, 0); X.quadraticCurveTo(w, w, 0, s); X.quadraticCurveTo(-w, w, -s, 0); X.quadraticCurveTo(-w, -w, 0, -s); X.fill(); X.restore();
}
