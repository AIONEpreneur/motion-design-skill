// Figuren und Objekte in der Handschrift des Originals.
// Papierwelt: dicke warme Tusche (4–5 px), Fläche + dünne Schraffur auf der Schattenseite, Glanzpunkt oben links,
// Knopfaugen mit zwei Lichtpunkten, rosa Wangen. Blaupause: dieselben Figuren als leuchtende Lavendel-Linie.

function eyes(x, y, sp, rx, ry, blink = 0, mood = 'happy', col = '#1d1718') {
  for (const s of [-1, 1]) {
    const ex = x + s * sp;
    if (mood === 'x') { X.strokeStyle = P.ink; X.lineWidth = 4.2; X.lineCap = 'round'; X.beginPath(); X.moveTo(ex - rx, y - rx); X.lineTo(ex + rx, y + rx); X.moveTo(ex + rx, y - rx); X.lineTo(ex - rx, y + rx); X.stroke(); continue; }
    if (mood === 'closed' || blink > .85) { X.strokeStyle = col; X.lineWidth = 3.6; X.lineCap = 'round'; X.beginPath(); X.arc(ex, y - 2, rx * .9, .15 * Math.PI, .85 * Math.PI); X.stroke(); continue; }
    const k = 1 - blink;
    X.fillStyle = col; X.beginPath(); X.ellipse(ex, y, rx, ry * k, 0, 0, 7); X.fill();
    if (k > .4) { X.fillStyle = '#fff'; X.beginPath(); X.arc(ex - rx * .3, y - ry * .35 * k, rx * .38, 0, 7); X.fill(); X.beginPath(); X.arc(ex + rx * .32, y + ry * .3 * k, rx * .18, 0, 7); X.fill(); }
  }
}
function cheeks(x, y, sp, rx, a = .8) { X.save(); X.globalAlpha *= a; X.fillStyle = P.blush; for (const s of [-1, 1]) { X.beginPath(); X.ellipse(x + s * sp, y, rx, rx * .52, 0, 0, 7); X.fill(); } X.restore(); }
function mouth(x, y, w, mood, col = P.ink) {
  X.strokeStyle = col; X.lineWidth = 3.4; X.lineCap = 'round'; X.beginPath();
  if (mood === 'happy') X.arc(x, y - w * .45, w * .6, .22 * Math.PI, .78 * Math.PI);
  else if (mood === 'sad') X.arc(x, y + w * .55, w * .55, 1.25 * Math.PI, 1.75 * Math.PI);
  else if (mood === 'wavy') { X.moveTo(x - w * .6, y); for (let i = 1; i <= 6; i++) X.lineTo(x - w * .6 + i * w * .2, y + (i % 2 ? -4 : 3)); }
  else if (mood === 'o') { X.arc(x, y, w * .18, 0, 7); }
  else { X.moveTo(x - w * .35, y); X.lineTo(x + w * .35, y); }
  X.stroke();
}
function sweat(x, y, s = 1, a = 1) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y); X.scale(s, s); const p = S('sweat', () => [...ellP(0, 8, 8, 9, 3, -.2, Math.PI + .2), [0, -12]], .4); ink(p, '#bfe0f5', 2.4); X.restore(); }

// ---------- Server-Figur (wie der Server im Original: Gesicht im Display, Schubfächer, grüne LED) ----------
// o: {on 0..1, mood 'happy'|'x'|'sick', blink, slot:{i, out(px), weak}, ledOff:[...], smoke}
function server(x, y, s, t, o = {}) {
  X.save(); X.translate(x, y); X.scale(s, s);
  const on = o.on ?? 1;
  castShadow(0, 4, 330, 22, .75);
  // Kabel
  line(bezP([118, -40], [190, -30], [170, 2], [330, 0], 24), 7, '#2f3546', 'cable');
  // Füße
  for (const fx of [-100, -35, 35, 100]) ink(S('sfoot' + fx, () => rrP(fx - 17, -22, 34, 24, 7)), '#3b4257', 3.2);
  const body = S('sbody', () => rrP(-130, -490, 260, 474, 26), 1.3);
  ink(body, P.srv, 5.2);
  hatch(body, '#4a556c', 20, 1.6, .9, sideRegion(62, -250, -1.2));
  // Glanzkanten
  X.fillStyle = 'rgba(255,255,255,.55)'; rr(X, -118, -440, 9, 150, 4.5); X.fill(); rr(X, -100, -478, 120, 8, 4); X.fill();
  // Gesichtsfeld
  const face = S('sface', () => rrP(-104, -462, 208, 128, 16), 1);
  const fc = mixCol('#565f76', P.srvF, on); ink(face, fc, 4);
  hatch(face, '#7c889f', 20, 1.3, .8, sideRegion(20, -380, -1.15));
  X.fillStyle = '#39404f'; for (const [sx, sy] of [[-92, -450], [92, -450], [-92, -346], [92, -346]]) { X.beginPath(); X.arc(sx, sy, 4.2, 0, 7); X.fill(); }
  const mood = o.mood || 'happy', bl = o.blink || 0;
  if (mood === 'x') { eyes(0, -408, 44, 12, 12, 0, 'x'); mouth(0, -372, 34, 'wavy'); }
  else if (mood === 'sick') { eyes(0, -404, 44, 12, 16, bl); cheeks(0, -378, 68, 17, .5); mouth(0, -370, 30, 'wavy');
    X.strokeStyle = P.ink; X.lineWidth = 3.4; X.beginPath(); X.moveTo(-60, -436); X.lineTo(-30, -428); X.moveTo(60, -436); X.lineTo(30, -428); X.stroke(); sweat(92, -430, 1, o.sweat ?? 1); }
  else { eyes(0, -404, 44, 12, 16, bl); cheeks(0, -376, 68, 17); mouth(0, -372, 30, 'happy'); }
  line([[-122, -320], [122, -320]], 2.6, hexA(P.ink, .6), 'sdiv');
  // Schubfächer
  for (let i = 0; i < 5; i++) {
    const yy = -300 + i * 58; let dx = 0, weak = false;
    if (o.slot && o.slot.i === i) { dx = -o.slot.out; weak = o.slot.weak; }
    X.save(); X.translate(dx, 0);
    const sl = S('slot', () => rrP(-104, 0, 208, 44, 9), .8); X.translate(0, yy);
    ink(sl, weak ? '#a4493d' : P.slot, 3.2);
    line([[-86, 22], [0, 22]], 2.2, P.slotL, 'sll'); X.fillStyle = P.slotL; X.beginPath(); X.arc(0, 22, 3.4, 0, 7); X.fill();
    X.strokeStyle = '#262c3a'; X.lineWidth = 2.4; X.beginPath(); for (let v = 0; v < 5; v++) { X.moveTo(34 + v * 8, 12); X.lineTo(34 + v * 8, 32); } X.stroke();
    const ledOn = on * (o.ledOff && o.ledOff[i] != null ? 1 - o.ledOff[i] : 1);
    let lc = weak ? (Math.floor(t * 4) % 2 ? '#ff5d4d' : '#7a2a22') : mixCol('#687086', P.led, ledOn);
    if (o.ledCol && o.ledCol[i]) lc = o.ledCol[i];
    X.save(); if (ledOn > .5 || weak) { X.shadowColor = lc; X.shadowBlur = 14; } X.fillStyle = lc; X.beginPath(); X.arc(84, 22, 9, 0, 7); X.fill(); X.restore();
    X.strokeStyle = P.ink; X.lineWidth = 2.2; X.beginPath(); X.arc(84, 22, 9, 0, 7); X.stroke();
    X.fillStyle = 'rgba(255,255,255,.7)'; X.beginPath(); X.arc(81, 19, 2.6, 0, 7); X.fill();
    X.restore();
  }
  if (o.lamp) statusLamp(t, o.lamp);
  if (o.smoke) smoke(165, -470, o.smoke, t);
  X.restore();
}
// Statuslampe auf dem Server: Leuchtkasten mit einem Wort (ONLINE grün / OFFLINE rot). lamp: {on, t0 = Umschaltzeit}
function statusLamp(t, L) {
  let on = L.on; if (L.t0 != null && t > L.t0 && t < L.t0 + .2) on = Math.floor((t - L.t0) * 30) % 2 === 0 ? !on : on;
  X.save(); line([[0, -490], [0, -512]], 5, P.ink, 'lpost');
  const box = S('lamp', () => rrP(-122, -584, 244, 72, 14), 1); dropHatch(box, 8, 9, .45); ink(box, '#2f3546', 4.4);
  const col = on ? '#8fe07a' : '#ff5d4d';
  X.font = '38px PM'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillStyle = col; X.shadowColor = col; X.shadowBlur = 18; X.fillText(on ? 'ONLINE' : 'OFFLINE', 0, -546); X.shadowBlur = 0;
  X.fillStyle = 'rgba(255,255,255,.25)'; rr(X, -110, -577, 60, 6, 3); X.fill();
  X.restore();
}
function smoke(x, y, a, t) { X.save(); X.globalAlpha *= clamp(a); for (let i = 0; i < 3; i++) { const k = ((t * .7 + i / 3) % 1), r = 16 + k * 26; X.globalAlpha = clamp(a) * (1 - k) * .9; const p = S('smk' + i, () => { const pts = []; for (let j = 0; j < 7; j++) pts.push(...ellP(Math.cos(j / 7 * 6.28) * .55, Math.sin(j / 7 * 6.28) * .55, .5, .5, .05, j / 7 * 6.28 - 1.2, j / 7 * 6.28 + 1.2)); return pts; }, .02);
    X.save(); X.translate(x + n1(i * 9 + t) * 14 + k * 30, y - k * 110); X.scale(r, r); X.fillStyle = '#d9d6cf'; X.fill(p); X.lineWidth = 2.6 / r; X.strokeStyle = P.ink2; X.stroke(p); X.restore(); } X.restore(); }

// ---------- Roboter (Maskottchen von Netzwerk Nord IT, gezeichnet wie der rote Roboter des Originals) ----------
// o: {mood, blink, look, armL, armR (Winkel), hold(fn), squash}
function robot(x, y, s, t, o = {}) {
  X.save(); X.translate(x, y); X.scale(s, s);
  castShadow(0, 2, 150, 16, .7);
  const sq = o.squash || 0; X.scale(1 + sq * .12, 1 - sq * .12);
  // Füße
  for (const fx of [-32, 32]) { const p = S('rfoot' + fx, () => ellP(fx, -12, 21, 13, 3), .6); ink(p, '#221a17', 2); }
  const lx = o.look || 0, bob = Math.sin(t * 6.3) * 2.5 * (o.bobA ?? 1);
  X.translate(0, bob);
  // Arme
  const arm = (side, ang) => { const sx = side * 82, sy = -92; const ex = sx + Math.cos(ang) * 58 * side, ey = sy + Math.sin(ang) * 58;
    X.strokeStyle = P.ink; X.lineWidth = 5; X.lineCap = 'round'; X.beginPath(); X.moveTo(sx, sy); X.quadraticCurveTo(sx + side * 24, sy + 4, ex, ey); X.stroke();
    X.fillStyle = P.red; X.beginPath(); X.arc(ex, ey, 10, 0, 7); X.fill(); X.lineWidth = 3.4; X.stroke(); return [ex, ey]; };
  const hL = arm(-1, o.armL ?? .9), hR = arm(1, o.armR ?? .9);
  // Antenne
  line(bezP([2, -186], [0, -205], [10, -220], [12, -236], 10), 4.6, P.ink, 'rant');
  const ab = S('rball', () => ellP(12, -246, 11, 11, 3), .5); X.save(); if (o.glowAnt) { X.shadowColor = P.gold; X.shadowBlur = 18; } ink(ab, P.gold, 3.8); X.restore();
  const body = S('rbody', () => rrP(-86, -190, 172, 158, 42), 1.3);
  ink(body, P.red, 5.4);
  hatch(body, P.redD, 20, 1.5, .55, sideRegion(20, -60, -.9));
  X.fillStyle = 'rgba(255,240,230,.85)'; rr(X, -66, -172, 28, 20, 7); X.fill(); X.fillStyle = 'rgba(255,255,255,.9)'; rr(X, -62, -169, 10, 8, 3); X.fill();
  eyes(lx, -118, 33, 12, 15.5, o.blink || 0, o.mood === 'closed' ? 'closed' : 'happy');
  cheeks(lx, -92, 56, 16, .75);
  mouth(lx, -86, 22, o.mouth || 'happy');
  if (o.brow) { X.strokeStyle = P.ink; X.lineWidth = 4; X.beginPath(); X.moveTo(lx - 50, -146); X.lineTo(lx - 20, -138); X.moveTo(lx + 50, -146); X.lineTo(lx + 20, -138); X.stroke(); }
  if (o.hold) o.hold(hL, hR);
  X.restore();
}

// ---------- Kolleg:innen als Knubbel-Figuren (wie die Speicher-Objekte im Original) ----------
function blob(x, y, s, col, mood, t, seed, o = {}) {
  X.save(); X.translate(x, y); X.scale(s, s);
  const b = o.tap ? Math.abs(Math.sin(t * 13 + seed)) * 12 : Math.abs(Math.sin(t * (o.hop ? 9 : 2.2) + seed)) * (o.hop ? 10 : 1.6);
  if (o.tap) { // ungeduldiges Wippen: kleine Bewegungsstriche am Boden
    X.save(); X.strokeStyle = hexA(P.ink, .7 * Math.abs(Math.sin(t * 13 + seed))); X.lineWidth = 3.4; X.lineCap = 'round'; X.beginPath();
    for (const s of [-1, 1]) { X.moveTo(s * 46, -6); X.lineTo(s * 64, -16); X.moveTo(s * 48, 6); X.lineTo(s * 68, 4); } X.stroke(); X.restore(); }
  X.translate(0, -b);
  const p = S('blob' + (seed % 4), () => { const w = 76 + (seed % 3) * 6, h = 72 + (seed % 2) * 8; return [...ellP(0, -h + w / 2, w / 2, w / 2, 4, Math.PI, Math.PI * 2), ...polyP([[w / 2, -h + w / 2], [w / 2 + 2, -6], [w / 2 - 6, 0], [-w / 2 + 6, 0], [-w / 2 - 2, -6]], false, 6)]; }, 1.2);
  ink(p, col, 3.6); hatch(p, P.ink2, 20, 1.1, .35, sideRegion(10, -20, -.9));
  X.fillStyle = 'rgba(255,255,255,.75)'; X.beginPath(); X.ellipse(-20, -58, 8, 5, -.5, 0, 7); X.fill();
  const bl = ((t + seed * .37) % 3.1) < .12 ? 1 : 0;
  const lk = o.look || 0; eyes(lk * 7, -41 - Math.abs(lk) * 2, 13, 4.8, 6.2, bl, 'happy'); cheeks(0, -30, 24, 7, .8);
  mouth(0, -28, 12, mood);
  X.restore();
}
// Schreibtisch mit Bildschirm; screen: 'wait' | 'work' | 'off'
function desk(x, y, s, t, screen, seed, mx = 0) {
  X.save(); X.translate(x, y); X.scale(s, s);
  // Monitor
  X.save(); X.translate(mx, 0);
  const mon = S('mon', () => rrP(-48, -150, 96, 66, 8), .8);
  ink(S('monst', () => polyP([[-8, -86], [8, -86], [12, -62], [-12, -62]])), '#6e6a66', 2.6);
  ink(mon, '#3a3f4f', 3.4);
  const scr = S('scr', () => rrP(-40, -143, 80, 51, 5), .5); X.fillStyle = screen === 'off' ? '#4a5064' : P.win; X.fill(scr);
  X.save(); X.clip(scr);
  if (screen === 'wait') { const a = t * 7 + seed; X.strokeStyle = P.dash; X.lineWidth = 4; X.lineCap = 'round'; X.beginPath(); X.arc(0, -117, 12, a, a + 4.2); X.stroke(); X.strokeStyle = hexA(P.ink, .2); X.lineWidth = 4; X.beginPath(); X.arc(0, -117, 12, a + 4.4, a + 6.1); X.stroke(); }
  if (screen === 'work') { const cols = [P.dash, P.red, P.grass, P.gold]; for (let i = 0; i < 5; i++) { const yy = -136 + ((i * 9 + t * 30 + seed * 7) % 45); X.fillStyle = hexA(cols[(i + seed) % 4], .8); rr(X, -32, yy, 20 + ((i * 13 + seed * 5) % 40), 4, 2); X.fill(); } }
  X.restore(); X.restore();
  // Tischplatte und Beine
  ink(S('dleg', () => polyP([[-56, -60], [-50, 0], [-44, 0], [-48, -60]])), P.woodD, 2.4);
  ink(S('dleg2', () => polyP([[56, -60], [50, 0], [44, 0], [48, -60]])), P.woodD, 2.4);
  const top = S('dtop', () => rrP(-70, -66, 140, 14, 4), .7); ink(top, P.wood, 3.2);
  X.strokeStyle = hexA(P.woodD, .7); X.lineWidth = 1.2; X.beginPath(); X.moveTo(-60, -59); X.lineTo(-10, -59); X.moveTo(10, -58); X.lineTo(52, -58); X.stroke();
  X.restore();
}

// ---------- Brief und Rechnung ----------
function envelope(x, y, s, rot = 0) { X.save(); X.translate(x, y); X.rotate(rot); X.scale(s, s);
  const p = S('env', () => rrP(-48, -32, 96, 64, 4), .8); dropHatch(p, 7, 8, .45); ink(p, '#fbf8f2', 4);
  line(polyP([[-46, -28], [0, 6], [46, -28]], false, 6), 3.4, P.ink, 'envf'); X.fillStyle = '#c7372f'; X.beginPath(); X.arc(0, 6, 7, 0, 7); X.fill(); X.strokeStyle = P.ink; X.lineWidth = 2; X.stroke(); X.restore(); }
function invoice(x, y, s, rot = 0) { X.save(); X.translate(x, y); X.rotate(rot); X.scale(s, s);
  const p = S('inv', () => polyP([[-40, -54], [26, -54], [40, -40], [40, 54], [-40, 54]]), .8); dropHatch(p, 7, 8, .45); ink(p, '#fbf8f2', 3.8);
  X.strokeStyle = hexA(P.ink, .75); X.lineWidth = 3; X.lineCap = 'round'; X.beginPath(); for (let i = 0; i < 4; i++) { X.moveTo(-26, -30 + i * 14); X.lineTo(i === 0 ? 0 : 22 - i * 4, -30 + i * 14); } X.stroke();
  X.font = '700 26px IN'; X.fillStyle = P.redD; X.textAlign = 'right'; X.fillText('€', 28, 42); X.strokeStyle = hexA(P.ink, .7); X.lineWidth = 2.2; X.beginPath(); X.moveTo(-26, 34); X.lineTo(4, 34); X.stroke(); X.restore(); }
// rotes Kreuz im Ring (wie „cache miss“ im Original)
function missX(x, y, r, k, t) { if (k <= 0) return; X.save(); X.translate(x, y); X.strokeStyle = '#e0356f'; X.lineWidth = 3; X.lineCap = 'round';
  X.globalAlpha = clamp(k * 2); X.beginPath(); X.arc(0, 0, r, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * eo(clamp(k * 1.4))); X.stroke();
  const a = eo(lin(k, .35, .7)), b = eo(lin(k, .6, 1)); X.lineWidth = 6.5; X.beginPath(); X.moveTo(-r * .5, -r * .5); X.lineTo(mix(-r * .5, r * .5, a), mix(-r * .5, r * .5, a)); if (b > 0) { X.moveTo(r * .5, -r * .5); X.lineTo(mix(r * .5, -r * .5, b), mix(-r * .5, r * .5, b)); } X.stroke(); X.restore(); }

// ---------- Festplatte als Figur ----------
function hdd(x, y, s, rot, mood, t, o = {}) {
  X.save(); X.translate(x, y); X.rotate(rot); X.scale(s, s);
  const p = S('hdd', () => rrP(-70, -48, 140, 96, 12), 1); dropHatch(p, 8, 9, .4);
  ink(p, mood === 'new' ? '#bfe0a6' : '#e9a290', 4.2);
  hatch(p, mood === 'new' ? '#5e8f45' : '#b0503c', 12, 1.1, .6, sideRegion(30, 20, -1.1));
  X.strokeStyle = hexA(P.ink, .7); X.lineWidth = 2.2; X.beginPath(); X.arc(-18, 0, 32, 0, 7); X.stroke(); X.beginPath(); X.arc(-18, 0, 20, 0, 7); X.stroke();
  X.fillStyle = '#e7ebf1'; X.beginPath(); X.arc(-18, 0, 7, 0, 7); X.fill(); X.stroke();
  X.lineWidth = 4; X.beginPath(); X.moveTo(46, -30); X.lineTo(4, 8); X.stroke();
  for (const [sx, sy] of [[-60, -38], [60, -38], [-60, 38], [60, 38]]) { X.fillStyle = '#4c5364'; X.beginPath(); X.arc(sx, sy, 3.2, 0, 7); X.fill(); }
  // Gesicht auf dem Etikett
  X.fillStyle = mood === 'new' ? '#f7f1df' : '#e8e0cc'; rr(X, 20, 6, 42, 32, 5); X.fill(); X.lineWidth = 2; X.strokeStyle = P.ink; X.stroke();
  if (mood === 'new') { eyes(41, 18, 9, 3, 4, 0); mouth(41, 28, 8, 'happy'); if (o.shine) spark(-40, -34, 18 * o.shine, o.shine, '#fff');
    if (o.check !== false) { X.save(); X.translate(62, -46); const c = S('chk', () => ellP(0, 0, 22, 22, 4), .5); ink(c, '#79b857', 3.2); X.strokeStyle = '#fff'; X.lineWidth = 5; X.lineCap = 'round'; X.lineJoin = 'round'; X.beginPath(); X.moveTo(-10, 1); X.lineTo(-3, 9); X.lineTo(11, -8); X.stroke(); X.restore(); } }
  else if (mood === 'dead') { X.strokeStyle = P.ink; X.lineWidth = 2.4; X.lineCap = 'round'; X.beginPath(); for (const ex of [33, 49]) { X.moveTo(ex - 4, 13); X.lineTo(ex + 4, 21); X.moveTo(ex + 4, 13); X.lineTo(ex - 4, 21); } X.stroke(); mouth(41, 30, 8, 'wavy');
    X.strokeStyle = P.ink; X.lineWidth = 2.6; X.beginPath(); X.moveTo(-60, -20); X.lineTo(-44, -8); X.lineTo(-50, 6); X.lineTo(-36, 18); X.stroke(); }
  else { X.lineWidth = 2.4; X.beginPath(); X.moveTo(33, 16); X.lineTo(38, 20); X.moveTo(49, 16); X.lineTo(44, 20); X.stroke(); mouth(41, 30, 8, 'wavy'); sweat(64, -2, .7, 1);
    X.strokeStyle = P.ink; X.lineWidth = 2.6; X.beginPath(); X.moveTo(-60, -20); X.lineTo(-44, -8); X.lineTo(-50, 6); X.lineTo(-36, 18); X.stroke(); }
  X.restore();
}

// ---------- Wanduhr ----------
function wallClock(x, y, r, t, spin, arcK, lab = null) {
  X.save(); X.translate(x, y);
  const p = S('clock' + r, () => ellP(0, 0, r, r, 5), 1.2); dropHatch(p, 12, 14, .5);
  ink(p, '#fbf7ee', 5.2); const p2 = S('clock2' + r, () => ellP(0, 0, r * .86, r * .86, 5), .8); X.strokeStyle = hexA(P.ink, .5); X.lineWidth = 2; X.stroke(p2);
  hatch(p, P.ink2, 12, 1, .3, sideRegion(r * .35, r * .3, -1.0));
  X.strokeStyle = P.ink; X.lineCap = 'round';
  for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2, l = i % 5 ? 7 : 18; X.lineWidth = i % 5 ? 1.6 : 4; X.beginPath(); X.moveTo(Math.cos(a) * (r * .8 - l), Math.sin(a) * (r * .8 - l)); X.lineTo(Math.cos(a) * r * .8, Math.sin(a) * r * .8); X.stroke(); }
  if (arcK > 0) { X.save(); X.strokeStyle = P.dash; X.lineWidth = 9; X.globalAlpha = .9; X.beginPath(); X.arc(0, 0, r * .93, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * arcK); X.stroke(); X.restore(); }
  // Beschriftung im Zifferblatt (V7: „24/7“), unter den Zeigern
  if (lab && lab.a > 0) { X.save(); X.globalAlpha *= lab.a; const sc = mix(1.25, 1, eo(lab.a)); X.translate(0, r * .52); X.scale(sc, sc); X.font = `600 ${Math.round(r * .3)}px IN`; X.letterSpacing = '-1px'; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillStyle = P.dash; X.fillText(lab.s, 0, 0); X.restore(); }
  const hr = spin / 12 * Math.PI * 2 - Math.PI / 2, mn = spin * Math.PI * 2 - Math.PI / 2;
  X.lineWidth = 8; X.beginPath(); X.moveTo(0, 0); X.lineTo(Math.cos(hr) * r * .45, Math.sin(hr) * r * .45); X.stroke();
  X.lineWidth = 5; X.beginPath(); X.moveTo(0, 0); X.lineTo(Math.cos(mn) * r * .68, Math.sin(mn) * r * .68); X.stroke();
  X.fillStyle = P.red; X.beginPath(); X.arc(0, 0, 9, 0, 7); X.fill(); X.lineWidth = 3; X.stroke();
  X.restore();
}
function sun(x, y, r, t, a = 1) { X.save(); X.globalAlpha *= a; X.translate(x, y); X.strokeStyle = P.goldD; X.lineWidth = 3.2; X.lineCap = 'round';
  for (let i = 0; i < 12; i++) { const an = i / 12 * Math.PI * 2 + t * .3; X.beginPath(); X.moveTo(Math.cos(an) * r * 1.3, Math.sin(an) * r * 1.3); X.lineTo(Math.cos(an) * r * 1.62, Math.sin(an) * r * 1.62); X.stroke(); }
  const p = S('sun' + r, () => ellP(0, 0, r, r, 4), .8); ink(p, P.gold, 3.8); hatch(p, P.goldD, 12, 1, .45, sideRegion(r * .2, r * .2, -1)); X.restore(); }
function moonP(x, y, r, a = 1) { X.save(); X.globalAlpha *= a; X.translate(x, y); const p = S('moon' + r, () => ellP(0, 0, r, r, 4), .6); ink(p, '#f4e7b8', 3.4); hatch(p, P.goldD, 12, 1, .5, sideRegion(r * .25, 0, -1.2)); X.strokeStyle = hexA(P.ink, .55); X.lineWidth = 1.8; for (const [cx, cy, cr] of [[-r * .3, -r * .25, r * .2], [r * .2, r * .3, r * .14], [-r * .1, r * .45, r * .09]]) { X.beginPath(); X.arc(cx, cy, cr, 0, 7); X.stroke(); } X.restore(); }

// ---------- Blaupausen-Versionen ----------
// Server als leuchtende Linienzeichnung. st: {col, alarm 0..1, ok 0..1}
function bpServer(x, y, s, t, st = {}) {
  X.save(); X.translate(x, y); X.scale(s, s);
  const col = st.alarm ? mixCol(P.lav, P.mag, st.alarm) : P.lav;
  const body = S('bps', () => rrP(-130, -490, 260, 474, 26), .6);
  X.fillStyle = 'rgba(40,48,100,.35)'; X.fill(body);
  hatch(body, 'rgba(205,209,243,.18)', 12, 1, 1, sideRegion(70, -250, -1.2));
  glow(body, col, 2.4, 10);
  const face = S('bpf', () => rrP(-104, -462, 208, 128, 16), .5); glow(face, col, 1.8, 6);
  X.save(); X.strokeStyle = col; X.fillStyle = col; X.lineWidth = 2.2;
  // Gesicht als Linie
  if (st.alarm > .5) { for (const sx of [-44, 44]) { X.beginPath(); X.moveTo(sx - 10, -418); X.lineTo(sx + 10, -398); X.moveTo(sx + 10, -418); X.lineTo(sx - 10, -398); X.stroke(); } }
  else for (const sx of [-44, 44]) { X.beginPath(); X.ellipse(sx, -405, 9, 12, 0, 0, 7); X.stroke(); X.beginPath(); X.arc(sx - 2, -409, 3, 0, 7); X.fill(); }
  X.beginPath(); if (st.alarm > .5) { X.moveTo(-14, -370); X.lineTo(14, -370); } else X.arc(0, -384, 14, .25 * Math.PI, .75 * Math.PI); X.stroke();
  X.strokeStyle = P.salmon; X.globalAlpha = .7; for (const sx of [-70, 70]) { X.beginPath(); X.ellipse(sx, -376, 11, 5.5, 0, 0, 7); X.stroke(); } X.restore();
  for (let i = 0; i < 5; i++) { const yy = -300 + i * 58; const sl = S('bpsl', () => rrP(-104, 0, 208, 44, 9), .4); X.save(); X.translate(0, yy); glow(sl, col, 1.6, 4, .85);
    X.strokeStyle = hexA(P.lav, .6); X.lineWidth = 1.5; X.beginPath(); X.moveTo(-86, 22); X.lineTo(0, 22); for (let v = 0; v < 5; v++) { X.moveTo(34 + v * 8, 12); X.lineTo(34 + v * 8, 32); } X.stroke();
    const lc = st.ledCol ? st.ledCol(i) : (st.alarm > .5 ? P.mag : P.mint); X.fillStyle = lc; X.shadowColor = lc; X.shadowBlur = 14; X.beginPath(); X.arc(84, 22, 7, 0, 7); X.fill(); X.restore(); }
  X.restore();
}
// Roboter als Linienfigur (wie der Blaupausen-Roboter im Original)
function bpRobot(x, y, s, t, o = {}) {
  X.save(); X.translate(x, y + Math.sin(t * 4) * 5); X.scale(s, s); X.rotate(o.tilt || 0);
  const dr = o.draw ?? 1, dA = eo(lin(dr, 0, .55)), dB = lin(dr, .45, 1);
  const body = S('bpr', () => rrP(-60, -110, 120, 100, 28), .5), inner = S('bpri', () => rrP(-48, -98, 96, 76, 20), .4);
  X.save(); X.globalAlpha *= dB; X.fillStyle = 'rgba(12,15,40,.9)'; X.fill(body); X.restore();
  X.save(); X.setLineDash([400 * dA, 1000]); glow(body, P.lav, 2.6, 10); X.setLineDash([300 * eo(lin(dr, .15, .7)), 1000]); glow(inner, P.salmon, 1.8, 6, .9); X.restore();
  if (dB <= 0) { X.restore(); return; }
  X.globalAlpha *= dB;
  X.strokeStyle = P.lav; X.lineWidth = 2.4; X.beginPath(); X.moveTo(0, -110); X.quadraticCurveTo(-2, -130, 6, -146); X.stroke();
  spark(8, -152, 14 + Math.sin(t * 6) * 3, 1, '#ffe7d8');
  X.fillStyle = '#eef0ff'; for (const sx of [-20, 20]) { X.beginPath(); X.ellipse(sx, -64, 7.5, 10, 0, 0, 7); X.fill(); } X.fillStyle = P.navy0; for (const sx of [-18, 22]) { X.beginPath(); X.arc(sx, -62, 3, 0, 7); X.fill(); }
  X.strokeStyle = '#eef0ff'; X.lineWidth = 2.4; X.beginPath(); X.arc(0, -48, 7, .2 * Math.PI, .8 * Math.PI); X.stroke();
  X.save(); X.strokeStyle = P.salmon; X.globalAlpha *= .6; for (const sx of [-34, 34]) { X.beginPath(); X.ellipse(sx, -46, 7, 3.5, 0, 0, 7); X.stroke(); } X.restore();
  // Beine und Arme
  X.strokeStyle = P.lav; X.lineWidth = 2.4; for (const sx of [-26, 26]) { X.beginPath(); X.moveTo(sx, -10); X.lineTo(sx, 8); X.stroke(); X.beginPath(); X.arc(sx, 14, 7, 0, 7); X.stroke(); }
  const wv = o.wave ? Math.sin(t * 9) * .5 : 0;
  X.beginPath(); X.moveTo(-60, -56); X.lineTo(-80, -40); X.stroke(); X.beginPath(); X.arc(-84, -36, 6, 0, 7); X.stroke();
  X.beginPath(); X.moveTo(60, -56); X.lineTo(60 + Math.cos(-.9 + wv) * 30, -56 + Math.sin(-.9 + wv) * 30); X.stroke(); X.beginPath(); X.arc(60 + Math.cos(-.9 + wv) * 36, -56 + Math.sin(-.9 + wv) * 36, 6, 0, 7); X.stroke();
  X.restore();
}
// Vorhängeschloss (für verschlüsselte Pakete)
function lock(x, y, s, a = 1, col = P.gold) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y); X.scale(s, s);
  X.strokeStyle = col; X.lineWidth = 3.2; X.shadowColor = col; X.shadowBlur = 10; X.beginPath(); X.arc(0, -10, 9, Math.PI, 0); X.lineTo(9, -2); X.moveTo(-9, -2); X.lineTo(-9, -10); X.stroke();
  X.fillStyle = col; rr(X, -14, -3, 28, 22, 4); X.fill(); X.shadowBlur = 0; X.fillStyle = P.navy0; X.beginPath(); X.arc(0, 6, 3.2, 0, 7); X.fill(); X.fillRect(-1.2, 7, 2.4, 6); X.restore(); }

// ---------- Rankpflanze (wie die Hängepflanze im Original) ----------
function leaf(x, y, ang, s) { X.save(); X.translate(x, y); X.rotate(ang); X.scale(s, s);
  const p = S('leaf', () => [...bezP([0, 0], [8, -12], [26, -12], [38, 0], 10), ...bezP([38, 0], [26, 12], [8, 12], [0, 0], 10)], .5);
  ink(p, '#8cc063', 2.4); hatch(p, '#4f7d33', 8, 1, .5, sideRegion(0, 2, 0)); X.strokeStyle = hexA('#3d5f28', .8); X.lineWidth = 1.4; X.beginPath(); X.moveTo(3, 0); X.lineTo(30, 0); X.stroke(); X.restore(); }
function vine(x, y, len, sway, seed, t) {
  const pts = []; for (let i = 0; i <= 30; i++) { const u = i / 30; pts.push([x + Math.sin(u * 3 + seed) * 18 * u + Math.sin(t * 1.3 + seed) * sway * u * u, y + u * len]); }
  X.strokeStyle = '#5b4632'; X.lineWidth = 3.4; X.lineCap = 'round'; X.stroke(pathOf(pts)); X.strokeStyle = P.ink; X.lineWidth = 1.2; X.stroke(pathOf(pts));
  for (let i = 3; i < 30; i += 3) { const [lx, ly] = pts[i]; const side = (i / 3) % 2 ? 1 : -1; leaf(lx, ly, side > 0 ? -.5 + Math.sin(t * 2 + i) * .08 : Math.PI + .5, .8 + hash(seed + i) * .3); }
  const e = pts[30]; X.fillStyle = '#8cc063'; X.beginPath(); X.arc(e[0], e[1], 4, 0, 7); X.fill(); X.strokeStyle = P.ink; X.lineWidth = 1.6; X.stroke();
}
function hangingPlant(x, y, t, s = 1) { X.save(); X.translate(x, y); X.scale(s, s);
  X.strokeStyle = hexA(P.ink, .8); X.lineWidth = 1.6; X.beginPath(); X.moveTo(0, -120); X.lineTo(-44, 0); X.moveTo(0, -120); X.lineTo(44, 0); X.moveTo(0, -120); X.lineTo(0, 0); X.stroke();
  vine(-36, 10, 170, 10, 1, t); vine(34, 10, 230, 12, 2, t); vine(-10, 16, 120, 8, 3, t); vine(12, 14, 300, 14, 4, t);
  const b = S('basket', () => [...polyP([[-56, 0], [56, 0]], false, 6), ...bezP([56, 0], [52, 30], [30, 44], [0, 44], 10), ...bezP([0, 44], [-30, 44], [-52, 30], [-56, 0], 10)], .8);
  ink(b, '#b07a4a', 3.6); hatch(b, '#6e4526', 8, 1.1, .6); X.strokeStyle = hexA(P.ink, .6); X.lineWidth = 1.4; X.beginPath(); for (let i = 1; i < 4; i++) { X.moveTo(-54 + i * 3, i * 10); X.lineTo(54 - i * 3, i * 10); } X.stroke();
  for (let i = 0; i < 5; i++) leaf(-40 + i * 20, -4, -Math.PI / 2 + (i - 2) * .45, .75);
  X.restore(); }
function pottedPlant(x, y, t, s = 1) { X.save(); X.translate(x, y); X.scale(s, s);
  vine(-16, -50, 150, 6, 7, t); vine(18, -50, 110, 6, 8, t);
  for (let i = 0; i < 7; i++) leaf(0, -56, -Math.PI / 2 + (i - 3) * .42 + Math.sin(t * 1.5 + i) * .05, .95);
  const p = S('pot', () => polyP([[-40, -60], [40, -60], [30, 0], [-30, 0]]), .8); ink(p, '#c9714f', 3.6); hatch(p, '#8a4630', 12, 1.1, .55, sideRegion(10, -30, -1.2)); line([[-42, -50], [42, -50]], 3, P.ink, 'potrim');
  X.restore(); }
