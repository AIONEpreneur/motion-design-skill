// Figuren und Objekte in der Handschrift des Melonen-Films: glänzende Ameise mit Maserung und Borsten,
// kritzel-texturierte Sonne mit blau/ocker Strahlen, Kiesel mit Glanzpunkt, Pflanzen mit Blattadern.

// ---------- Ameise (Seitenansicht, schaut nach rechts; Ursprung am Boden unter der Mitte) ----------
function ant(x, y, s, t, o = {}) {
  X.save(); X.translate(x, y); X.scale(s * (o.flip ? -1 : 1), s);
  const walk = o.walk ?? 0, ph = t * 11;
  if (!o.noShadow) { X.save(); const sp = S('antsh', () => ellP(0, 0, 170, 10, 6), .5); X.translate(-10, 2); hatch(sp, OL(), 8, 1, .45, null, 3, 2); X.restore(); }
  const legs = [[12, -74, -58, -118, -125], [36, -76, -8, -128, -30], [58, -80, 44, -126, 70]];
  const legPath = (hx, hy, kx, ky, fx, i, far) => { const sw = walk * Math.sin(ph + i * 2.1 + (far ? Math.PI : 0)) * 16, lift = walk * Math.max(0, Math.cos(ph + i * 2.1 + (far ? Math.PI : 0))) * 10;
    return [[hx, hy], [kx + sw * .5, ky - lift * .3], [fx + sw, -lift]]; };
  // ferne Beine (grau, versetzt – wie der Schatten-Zug im Original)
  X.strokeStyle = NIGHT ? '#9aa0c8' : '#9b9aa3'; X.lineWidth = 3; X.lineCap = 'round'; X.lineJoin = 'round';
  legs.forEach(([hx, hy, kx, ky, fx], i) => { const q = legPath(hx + 14, hy, kx + 18, ky + 4, fx + 22, i, true); X.stroke(pathOf(q)); });
  // Hinterleib
  const gas = S('antg', () => ellP(-95, -80, 72, 54, 5), .8);
  ink(gas, P.ant, 3.2);
  X.save(); X.clip(gas); X.strokeStyle = F(P.antD); X.globalAlpha = .7; X.lineWidth = 1.4;
  for (let k = 1; k < 8; k++) { X.beginPath(); X.ellipse(-140 + k * 3, -80, k * 11, k * 9.5, 0, -1.3, 1.3); X.stroke(); }
  X.globalAlpha = .25; X.fillStyle = hatchTile(P.antD, 12, 1, 3, 2); X.fillRect(-200, -160, 200, 160); X.restore();
  X.strokeStyle = 'rgba(255,255,255,.8)'; X.lineWidth = 3; X.lineCap = 'round'; X.beginPath(); X.arc(-95, -80, 50, -2.5, -1.9); X.stroke(); X.lineWidth = 2; X.beginPath(); X.arc(-95, -80, 38, -2.55, -2.1); X.stroke();
  // Borsten
  X.strokeStyle = OL(); X.lineWidth = 1.2; X.beginPath(); for (let i = 0; i < 12; i++) { const a = 2.2 + i * .12, r0 = 72; X.moveTo(-95 + Math.cos(a) * r0, -80 + Math.sin(a) * r0 * .75); X.lineTo(-95 + Math.cos(a) * (r0 + 9), -80 + Math.sin(a) * (r0 + 9) * .75); } X.stroke();
  // Stielchen, Brust, Kopf
  ink(S('antp', () => ellP(-16, -80, 14, 17, 4), .5), P.ant, 3);
  const th = S('antt', () => [...ellP(16, -82, 27, 18, 4, Math.PI * .5, Math.PI * 1.6), ...ellP(52, -92, 25, 22, 4, Math.PI * 1.1, Math.PI * 2.4)], .6); ink(th, P.ant, 3);
  X.save(); X.clip(th); X.globalAlpha = .35; X.fillStyle = hatchTile(P.antD, 12, 1, 3, 2); X.fillRect(-20, -130, 110, 80); X.restore();
  const hd = S('anth', () => ellP(106, -102, 37, 32, 4), .6); ink(hd, P.ant, 3.2);
  X.save(); X.clip(hd); X.strokeStyle = F(P.antD); X.globalAlpha = .6; X.lineWidth = 1.3; for (let k = 1; k < 5; k++) { X.beginPath(); X.ellipse(80, -102, k * 11, k * 10, 0, -1.2, 1.2); X.stroke(); } X.restore();
  X.strokeStyle = 'rgba(255,255,255,.8)'; X.lineWidth = 2.6; X.beginPath(); X.arc(106, -102, 26, -2.4, -1.7); X.stroke();
  X.fillStyle = '#0d0b10'; X.beginPath(); X.ellipse(120, -106, 10, 11, 0, 0, 7); X.fill(); X.fillStyle = '#fff'; X.beginPath(); X.arc(117, -110, 3.4, 0, 7); X.fill();
  if (o.sweat) { X.save(); X.translate(78, -150); const p = S('asw', () => [...ellP(0, 8, 7, 8, 3, -.2, Math.PI + .2), [0, -10]], .3); ink(p, P.waterL, 2); X.restore(); }
  // Kiefer und Fühler
  X.strokeStyle = OL(); X.lineWidth = 3; X.beginPath(); X.moveTo(136, -90); X.quadraticCurveTo(152, -86, 148, -74); X.stroke();
  const aw = Math.sin(t * 3.1) * .12 + (o.antUp || 0);
  X.lineWidth = 2.6; X.beginPath(); X.moveTo(110, -132); X.lineTo(118 + aw * 10, -176); X.lineTo(150 + aw * 30, -200 - aw * 20); X.stroke();
  X.strokeStyle = NIGHT ? '#9aa0c8' : '#9b9aa3'; X.beginPath(); X.moveTo(100, -130); X.lineTo(100 - aw * 8, -172); X.lineTo(126 - aw * 20, -194); X.stroke();
  // nahe Beine (schwarz, über dem Körper)
  X.strokeStyle = OL(); X.lineWidth = 3.4;
  legs.forEach(([hx, hy, kx, ky, fx], i) => { X.stroke(pathOf(legPath(hx, hy, kx, ky, fx, i, false))); });
  if (o.hold) o.hold();
  X.restore();
}

// ---------- Sonne mit Kritzel-Textur und abwechselnd blauen/ockerfarbenen Strahlen ----------
function sun(x, y, r, t, hot = 0) {
  X.save(); X.translate(x, y);
  for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2 + t * .1, long = i % 2 === 0;
    X.strokeStyle = long ? (hot ? mixCol(P.blue, '#e0452f', hot) : P.blue) : P.ray; X.lineWidth = long ? 2.6 : 5; X.lineCap = 'round';
    const r0 = r * (long ? 1.25 : 1.2), r1 = r * (long ? 2.3 + hot * .6 + Math.sin(t * 5 + i) * .08 : 1.55); X.beginPath(); X.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); X.lineTo(Math.cos(a) * r1, Math.sin(a) * r1); X.stroke(); }
  const p = S('sun' + r, () => ellP(0, 0, r, r, 4), .8); X.fillStyle = F(P.sun); X.fill(p);
  X.save(); X.clip(p); X.strokeStyle = F(P.sunS); X.lineWidth = 3.2; X.lineCap = 'round'; X.beginPath();
  for (let i = 0; i < 70; i++) { const cx = (hash(i * 3.3) - .5) * 2 * r, cy = (hash(i * 7.7) - .5) * 2 * r, l = 10 + hash(i) * 22; X.moveTo(cx - l * .8, cy + l * .45); X.lineTo(cx + l * .8, cy - l * .45); } X.stroke(); X.restore();
  X.strokeStyle = OL(); X.lineWidth = 3.2; X.stroke(p); X.restore();
}
// Wolke: grau, schraffiert, Kontur
function cloud(x, y, s, key, col = '#c9cad6') { X.save(); X.translate(x, y); X.scale(s, s);
  const p = S('cl' + key, () => { const pts = []; pts.push(...ellP(-110, 10, 44, 34, 5, Math.PI * .5, Math.PI * 1.5)); pts.push(...ellP(-50, -22, 56, 50, 5, Math.PI * 1.05, Math.PI * 1.8)); pts.push(...ellP(30, -30, 62, 54, 5, Math.PI * 1.15, Math.PI * 1.9)); pts.push(...ellP(100, 4, 44, 38, 5, Math.PI * 1.3, Math.PI * 2.5)); pts.push(...polyP([[100, 42], [-110, 44]], false, 8)); return pts; }, 1);
  ink(p, col, 3); hatch(p, OL(), 10, 1.1, .35, null, 3, 2); X.restore(); }
function drop(x, y, s, a = 1) { if (a <= 0) return; X.save(); X.globalAlpha *= a; X.translate(x, y); X.scale(s, s); const p = S('drop', () => [...ellP(0, 10, 14, 15, 3, -.3, Math.PI + .3), [0, -22]], .4); ink(p, P.waterL, 2.6); X.fillStyle = 'rgba(255,255,255,.85)'; X.beginPath(); X.ellipse(-5, 8, 3, 5, .3, 0, 7); X.fill(); X.restore(); }
function ball(x, y, r, rot, t) { X.save(); X.translate(x, y); X.rotate(rot); const p = S('ball' + r, () => ellP(0, 0, r, r, 4), .5); X.fillStyle = F('#f7f3ea'); X.fill(p);
  X.save(); X.clip(p); const cols = [P.red, '#f0c348', '#4f78d0']; for (let i = 0; i < 3; i++) { X.fillStyle = F(cols[i]); X.beginPath(); X.moveTo(0, 0); X.arc(0, 0, r, i * 2.09, i * 2.09 + 1.05); X.fill(); } X.restore();
  X.strokeStyle = OL(); X.lineWidth = 3; X.stroke(p); X.fillStyle = 'rgba(255,255,255,.85)'; X.beginPath(); X.ellipse(-r * .35, -r * .4, r * .22, r * .13, -.6, 0, 7); X.fill(); X.restore(); }
function leaf(x, y, ang, s, col = P.leaf) { X.save(); X.translate(x, y); X.rotate(ang); X.scale(s, s);
  const p = S('leaf', () => [...bezP([0, 0], [10, -16], [34, -16], [48, 0], 10), ...bezP([48, 0], [34, 16], [10, 16], [0, 0], 10)], .5);
  ink(p, col, 2.4); hatch(p, P.leafD, 8, 1, .45, sideRegion(0, 2, 0)); X.strokeStyle = F(P.leafD); X.lineWidth = 1.5; X.beginPath(); X.moveTo(3, 0); X.lineTo(40, 0); for (let i = 1; i < 4; i++) { X.moveTo(i * 10, 0); X.lineTo(i * 10 + 7, -7); X.moveTo(i * 10, 0); X.lineTo(i * 10 + 7, 7); } X.stroke(); X.restore(); }
function flower(x, y, s) { X.save(); X.translate(x, y); X.scale(s, s); for (let i = 0; i < 5; i++) { const a = i / 5 * Math.PI * 2; X.beginPath(); X.ellipse(Math.cos(a) * 9, Math.sin(a) * 9, 8, 6, a, 0, 7); X.fillStyle = F('#ffffff'); X.fill(); X.strokeStyle = OL(); X.lineWidth = 1.6; X.stroke(); } X.fillStyle = F('#e9b43c'); X.beginPath(); X.arc(0, 0, 5, 0, 7); X.fill(); X.stroke(); X.restore(); }

// ---------- Haus mit Fenster und Kindern ----------
function kidHead(x, y, s, hair, mood, t, seed) { X.save(); X.translate(x, y); X.scale(s, s);
  const hd = S('kh' + seed, () => ellP(0, 0, 46, 50, 4), .6); ink(hd, P.skin, 3);
  hatch(hd, P.skinD, 10, 1, .35, sideRegion(18, 10, -1.2));
  const hr = S('khair' + seed, () => seed % 2 ? [...ellP(0, -6, 52, 50, 5, Math.PI * .95, Math.PI * 2.05), [40, -18], [10, -30], [-20, -20], [-44, -10]] : [...ellP(0, -4, 50, 52, 5, Math.PI * .9, Math.PI * 2.1), [46, 20], [30, -24], [-30, -24], [-46, 20]], .9);
  ink(hr, hair, 3); X.save(); X.clip(hr); X.strokeStyle = F(mixCol(hair, '#000', .35)); X.lineWidth = 1.4; X.globalAlpha = .7; for (let i = 0; i < 9; i++) { X.beginPath(); X.moveTo(-50 + i * 12, -60); X.quadraticCurveTo(-44 + i * 12, -30, -40 + i * 11, -14); X.stroke(); } X.restore();
  const bl = ((t + seed) % 2.7) < .12;
  for (const sx of [-16, 16]) { if (bl) { X.strokeStyle = OL(); X.lineWidth = 3; X.beginPath(); X.moveTo(sx - 6, 8); X.lineTo(sx + 6, 8); X.stroke(); continue; } X.fillStyle = '#141018'; X.beginPath(); X.ellipse(sx, 8, 6, 7, 0, 0, 7); X.fill(); X.fillStyle = '#fff'; X.beginPath(); X.arc(sx - 2, 5, 2.2, 0, 7); X.fill(); }
  X.fillStyle = hexA('#e98b8b', .6); X.beginPath(); X.ellipse(-28, 22, 9, 5, 0, 0, 7); X.ellipse(28, 22, 9, 5, 0, 0, 7); X.fill();
  X.strokeStyle = OL(); X.lineWidth = 3; X.lineCap = 'round'; X.beginPath(); if (mood === 'happy') X.arc(0, 22, 12, .2 * Math.PI, .8 * Math.PI); else if (mood === 'sad') X.arc(0, 38, 10, 1.25 * Math.PI, 1.75 * Math.PI); else { X.moveTo(-8, 30); X.lineTo(8, 30); } X.stroke();
  X.restore(); }
function house(t, o = {}) {
  // Fassade rechts: x 1300–2100, Boden y 300, Traufe y -480
  const wall = S('wall', () => polyP([[1300, 300], [1300, -470], [2100, -470], [2100, 300]]), 1.2);
  ink(wall, '#f1e6d2', 3.2); X.save(); X.clip(wall); X.strokeStyle = F('#dbc9ad'); X.lineWidth = 1.4; X.beginPath(); for (let y = -440; y < 300; y += 34) { X.moveTo(1300, y); X.lineTo(2100, y); } X.stroke(); X.restore();
  hatch(wall, OL(), 10, 1, .18, sideRegion(1300, 0, -1.4));
  const roof = S('roof', () => polyP([[1260, -470], [2140, -470], [2140, -520], [1300, -520]]), 1); ink(roof, '#8a4a3a', 3.2); hatch(roof, OL(), 8, 1, .4);
  // Fenster
  const win = S('win', () => rrP(1420, -340, 380, 310, 8), .8);
  ink(win, o.lit ? '#f4d98a' : '#dfeaf2', 3.4);
  X.save(); X.clip(win);
  X.fillStyle = F(o.lit ? '#e8c46a' : '#c8d8e6'); X.fillRect(1420, -150, 380, 130);
  if (o.kids) { kidHead(1530, -120 + Math.sin(t * 2.3) * 6, .95, '#6b4a2e', o.mood || 'sad', t, 1); kidHead(1690, -110 + Math.sin(t * 2.3 + 2) * 6, .85, '#e0b458', o.mood || 'sad', t, 2);
    X.fillStyle = F('#c9443a'); rr(X, 1470, -70, 120, 60, 20); X.fill(); X.fillStyle = F('#4f78d0'); rr(X, 1640, -62, 110, 60, 20); X.fill(); }
  X.strokeStyle = 'rgba(255,255,255,.7)'; X.lineWidth = 5; X.beginPath(); X.moveTo(1440, -200); X.lineTo(1520, -320); X.moveTo(1470, -150); X.lineTo(1580, -320); X.stroke();
  if (o.fog) { X.fillStyle = hexA('#ffffff', .5 * o.fog); X.beginPath(); X.ellipse(1532, -86, 40 * o.fog, 26 * o.fog, 0, 0, 7); X.fill(); }
  X.restore();
  X.strokeStyle = OL(); X.lineWidth = 3.4; X.beginPath(); X.moveTo(1610, -340); X.lineTo(1610, -30); X.stroke();
  const sill = S('sill', () => rrP(1400, -34, 420, 24, 4), .6); ink(sill, P.wood, 3); hatch(sill, P.woodD, 8, 1, .5);
  if (o.kids && o.hands) { for (const hx of [1490, 1560, 1660, 1720]) { X.save(); X.translate(hx, -36); const hp = S('hand', () => ellP(0, 0, 14, 10, 3), .4); ink(hp, P.skin, 2.4); X.restore(); } }
  // Tür-Stufe und Pflanzkübel
  const pot = S('pot', () => polyP([[1340, 300], [1330, 220], [1420, 220], [1410, 300]]), .8); ink(pot, '#c9714f', 3); hatch(pot, OL(), 10, 1, .3, sideRegion(1390, 260, -1.2));
  for (let i = 0; i < 6; i++) leaf(1375, 222, -Math.PI / 2 + (i - 2.5) * .4 + Math.sin(t * 1.4 + i) * .04, .9);
}
function swing(t, amp = .05, dx = 660, ang = null) { X.save(); X.translate(dx, 300); X.scale(1, .85); X.translate(0, -300); const p1 = S('sw1', () => polyP([[240, 300], [330, -260], [346, -260], [262, 300]]), .8), p2 = S('sw2', () => polyP([[600, 300], [510, -260], [494, -260], [578, 300]]), .8);
  ink(p1, P.wood, 3); ink(p2, P.wood, 3); hatch(p1, P.woodD, 8, 1, .45); hatch(p2, P.woodD, 8, 1, .45);
  const beam = S('swb', () => rrP(300, -280, 240, 26, 5), .6); ink(beam, P.wood, 3); hatch(beam, P.woodD, 8, 1, .45);
  const a = ang ?? Math.sin(t * 1.6) * amp; X.save(); X.translate(420, -266); X.rotate(a); X.strokeStyle = OL(); X.lineWidth = 2.4; X.beginPath(); X.moveTo(-50, 0); X.lineTo(-50, 380); X.moveTo(50, 0); X.lineTo(50, 380); X.stroke();
  const seat = S('sws', () => rrP(-66, 376, 132, 18, 4), .5); ink(seat, '#c9443a', 3); X.restore(); X.restore(); }

// ---------- Kind (ganzer Körper) für die Schluss-Szene im Garten ----------
function kid(x, y, s, t, kick) {
  X.save(); X.translate(x, y); X.scale(s, s);
  X.save(); const sp = S('kidsh', () => ellP(0, 0, 70, 8, 6), .5); hatch(sp, OL(), 8, 1, .45); X.restore();
  const k = kick; // 0..1..0
  X.strokeStyle = OL(); X.lineWidth = 7; X.lineCap = 'round';
  // Standbein
  X.beginPath(); X.moveTo(-12, -110); X.lineTo(-18, -4); X.stroke(); X.fillStyle = '#1c1a22'; X.beginPath(); X.ellipse(-12, -4, 18, 9, 0, 0, 7); X.fill();
  // Schussbein
  const a = -.1 - k * 1.2 + (1 - k) * .1, kx = 14 + Math.sin(-a) * 55, ky = -110 + Math.cos(a) * 55, fx = kx + Math.sin(-a * .6) * 55, fy = ky + Math.cos(a * .6) * 55;
  X.beginPath(); X.moveTo(14, -110); X.lineTo(kx, ky); X.lineTo(fx, fy); X.stroke(); X.beginPath(); X.ellipse(fx + 8, fy, 18, 9, a * .5, 0, 7); X.fill();
  const shorts = S('kshorts', () => rrP(-34, -140, 68, 40, 10), .6); ink(shorts, '#4f78d0', 3);
  const shirt = S('kshirt', () => rrP(-40, -230, 80, 100, 22), .8); ink(shirt, '#e9b43c', 3); hatch(shirt, OL(), 10, 1, .3, sideRegion(10, -170, -1.2));
  X.lineWidth = 6; X.beginPath(); X.moveTo(-36, -210); X.lineTo(-70, -160 - k * 30); X.moveTo(36, -210); X.lineTo(74, -250 + k * 20); X.stroke();
  X.fillStyle = F(P.skin); for (const [hx, hy] of [[-70, -160 - k * 30], [74, -250 + k * 20]]) { X.beginPath(); X.arc(hx, hy, 9, 0, 7); X.fill(); X.lineWidth = 2.4; X.stroke(); }
  kidHead(0, -280, .9, '#6b4a2e', 'happy', t, 1);
  X.restore();
}

// ---------- Werkzeug und Bodenleben ----------
function fork(x, y, rot, t) { // y = Spitze der Zinken
  X.save(); X.translate(x, y); X.rotate(rot);
  for (let i = 0; i < 4; i++) { const tx = -54 + i * 36; const p = S('tine' + i, () => polyP([[tx - 7, -540], [tx + 7, -540], [tx + 5, -20], [tx, 0], [tx - 5, -20]]), .4); ink(p, P.metal, 2.6); X.fillStyle = 'rgba(255,255,255,.6)'; X.fillRect(tx - 4, -530, 2.4, 480); }
  const cb = S('cross', () => rrP(-78, -590, 156, 54, 14), .6); ink(cb, P.metal, 3); hatch(cb, P.metalD, 8, 1, .5, sideRegion(0, -560, -1.3));
  const sh = S('shaft', () => rrP(-14, -1500, 28, 920, 10), .8); ink(sh, P.wood, 3); X.save(); X.clip(sh); X.strokeStyle = F(P.woodD); X.lineWidth = 1.3; for (let i = 0; i < 4; i++) { X.beginPath(); X.moveTo(-8 + i * 5, -1500); X.bezierCurveTo(-4 + i * 5, -1200, -10 + i * 5, -900, -6 + i * 5, -590); X.stroke(); } X.restore();
  const tag = S('ftag', () => rrP(-155, -770, 310, 92, 14), .6); ink(tag, '#3f7a3a', 3.4); X.save(); X.clip(tag); X.globalAlpha = .25; X.fillStyle = hatchTile('#1f4a1d', 10, 1, 3, 2); X.fillRect(-160, -780, 320, 100); X.restore(); leaf(-138, -724, -.7, .75, '#8fbc6b'); hand('Grünwerk', 16, -707, 60, '#f4f0dc', 'center');
  X.restore();
}
function worm(x, y, s, t, len = 1) { X.save(); X.translate(x, y); X.scale(s, s);
  const pts = []; for (let i = 0; i <= 40; i++) { const u = i / 40; pts.push([-u * 180 * len, Math.sin(u * 7 - t * 6) * 12]); }
  X.lineCap = 'round'; X.lineJoin = 'round'; X.strokeStyle = OL(); X.lineWidth = 24; X.stroke(pathOf(pts)); X.strokeStyle = F(P.worm); X.lineWidth = 18; X.stroke(pathOf(pts));
  X.strokeStyle = F(P.wormD); X.lineWidth = 1.6; for (let i = 3; i < 40; i += 3) { const [px, py] = pts[i]; X.beginPath(); X.moveTo(px, py - 8); X.lineTo(px, py + 8); X.stroke(); }
  X.fillStyle = '#141018'; X.beginPath(); X.arc(6, pts[0][1] - 3, 2.6, 0, 7); X.fill(); X.restore(); }
function root(pts, k, w = 6) { if (k <= 0) return; const sub = polySub(pts, 0, k); if (sub.length < 2) return; const p = pathOf(sub); X.lineCap = 'round'; X.lineJoin = 'round'; X.strokeStyle = OL(); X.lineWidth = w + 3; X.stroke(p); X.strokeStyle = F('#f0e4c6'); X.lineWidth = w; X.stroke(p); }
function magnifier(cx, cy, r, k, t, tx, ty) { if (k <= 0) return; X.save(); X.globalAlpha = clamp(k * 1.5);
  bLine([[tx, ty], [cx - r * .7, cy + r * .7]], 1, [6, 6]);
  X.translate(cx, cy); X.scale(eo(k), eo(k)); const c = S('mag' + r, () => ellP(0, 0, r, r, 4), .5);
  X.fillStyle = F('#7c6a60'); X.fill(c); X.save(); X.clip(c); X.globalAlpha = .4; X.fillStyle = hatchTile('#4a3a30', 12, 1, 1, 3); X.fillRect(-r, -r, 2 * r, 2 * r); X.globalAlpha = 1;
  const rp = bezP([-r * 1.2, r * .35], [-r * .35, -r * .25], [r * .3, r * .45], [r * 1.2, -r * .25], 40);
  X.lineCap = 'round'; X.strokeStyle = OL(); X.lineWidth = 44; X.stroke(pathOf(rp)); X.strokeStyle = F('#efe2c4'); X.lineWidth = 38; X.stroke(pathOf(rp));
  X.strokeStyle = F('#d9c7a0'); X.lineWidth = 1.4; X.beginPath(); for (let i = 2; i < 40; i += 3) { const [px, py] = rp[i]; X.moveTo(px - 6, py - 12); X.lineTo(px + 6, py + 12); } X.stroke();
  X.strokeStyle = F('#fbf6e8'); X.lineWidth = 1.2; X.beginPath();
  for (let i = 1; i < 40; i++) for (let j = 0; j < 3; j++) { const [px, py] = rp[i], [qx, qy] = rp[i - 1], ang = Math.atan2(py - qy, px - qx), side = (i + j) % 2 ? 1 : -1, nx = -Math.sin(ang) * side, ny = Math.cos(ang) * side, l = 16 + hash(i * 7 + j) * 34, wv = Math.sin(t * 2 + i + j) * 3;
    const ox = px + (j - 1) * 4, oy = py; X.moveTo(ox + nx * 19, oy + ny * 19); X.quadraticCurveTo(ox + nx * (19 + l * .5) + wv, oy + ny * (19 + l * .5), ox + nx * (19 + l) + (hash(i + j) - .5) * 12, oy + ny * (19 + l)); }
  X.stroke();
  X.restore(); X.strokeStyle = OL(); X.lineWidth = 4; X.stroke(c); X.strokeStyle = '#ffffff'; X.globalAlpha *= .6; X.lineWidth = 3; X.beginPath(); X.arc(0, 0, r - 10, -2.6, -1.9); X.stroke();
  X.restore(); }
// Holzschild auf Pfahl
function sign(x, y, t, o = {}) { X.save(); X.translate(x, y);
  const stake = S('stake', () => polyP([[-16, -470], [16, -470], [14, 60], [0, 90], [-14, 60]]), .6); ink(stake, P.wood, 3); hatch(stake, P.woodD, 8, 1, .5, sideRegion(4, 0, -1.4));
  const b = S('board', () => rrP(-330, -520, 660, 330, 14), 1.2); X.save(); X.translate(10, 12); hatch(b, OL(), 8, 1, .4); X.restore(); ink(b, '#d9b07a', 3.6);
  X.save(); X.clip(b); X.strokeStyle = F('#b98a5a'); X.lineWidth = 1.5; for (let i = 0; i < 9; i++) { X.beginPath(); X.moveTo(-330, -500 + i * 38); X.bezierCurveTo(-120, -490 + i * 38 + Math.sin(i) * 8, 80, -510 + i * 38, 330, -498 + i * 38); X.stroke(); } X.restore();
  X.fillStyle = '#3a2a20'; for (const [nx, ny] of [[-306, -496], [306, -496], [-306, -214], [306, -214]]) { X.beginPath(); X.arc(nx, ny, 5, 0, 7); X.fill(); }
  // Blatt-Signet
  leaf(-250, -420, -.8, 1.3, '#6fae55'); leaf(-250, -420, -1.9, 1.1, '#8fbc6b');
  hand('Grünwerk', 30, -400, 104, '#2f5f2c', 'center'); hand('Gartenbau', 30, -326, 56, P.ink, 'center');
  hand(o.contact || '', 0, -240, 32, P.ink, 'center', o.ca ?? 1);
  X.restore(); }
function sampleTube(x, y, h, k, t) { if (k <= 0) return; X.save(); X.translate(x, y); X.scale(1, eo(k)); const w = 110;
  const layers = [[P.topsoil, .2], [P.soil, .5], [P.gravel, .3]]; let yy = -h; for (const [c, f] of layers) { const hh = h * f; X.fillStyle = F(c); X.fillRect(-w / 2, yy, w, hh); if (c === P.gravel) { for (let i = 0; i < 10; i++) pebble(-40 + (i % 4) * 26, yy + 16 + Math.floor(i / 4) * 28, 11, 8, i, P.gravel); } else { X.save(); X.beginPath(); X.rect(-w / 2, yy, w, hh); X.clip(); X.globalAlpha = .5; X.fillStyle = hatchTile(mixCol(c, '#000', .35), 12, 1, 1, 3); X.fillRect(-w / 2, yy, w, hh); X.restore(); } yy += hh; }
  const g = S('tube', () => rrP(-w / 2 - 6, -h - 20, w + 12, h + 26, 22), .5); X.fillStyle = 'rgba(210,230,245,.25)'; X.fill(g); X.strokeStyle = OL(); X.lineWidth = 3.4; X.stroke(g);
  X.strokeStyle = 'rgba(255,255,255,.8)'; X.lineWidth = 6; X.beginPath(); X.moveTo(-w / 2 + 12, -h + 10); X.lineTo(-w / 2 + 12, -30); X.stroke();
  const cap = S('cap', () => rrP(-w / 2 - 12, -h - 50, w + 24, 40, 8), .5); ink(cap, P.red, 3);
  X.restore(); }

// Anhänger aus Karton an einer Schnur; k 0..1 = dreht sich von der Kante ins Bild
function hangTag(ax, ay, s, k, t, txt) { if (k <= 0) return; X.save(); X.translate(ax, ay);
  const sw = Math.sin((t - K.kostenlos) * 5) * .07 * Math.exp(-Math.max(0, t - K.kostenlos) * 1.4); X.rotate(sw);
  X.strokeStyle = OL(); X.lineWidth = 2.4; X.beginPath(); X.moveTo(0, 0); X.quadraticCurveTo(80, 10, 120, 74); X.stroke();
  X.translate(120, 74); X.scale(Math.sin(Math.PI / 2 * eo(k)), 1);
  const tg = S('htag', () => polyP([[-36, 0], [36, 0], [150, 26], [150, 116], [-150, 116], [-150, 26]]), .7);
  X.save(); X.translate(8, 8); hatch(tg, OL(), 8, 1, .35); X.restore(); ink(tg, '#f6f1e2', 3);
  X.beginPath(); X.arc(0, 18, 7, 0, 7); X.fillStyle = '#fff'; X.fill(); X.strokeStyle = OL(); X.lineWidth = 2.2; X.stroke();
  hand(txt, 0, 94, 58, '#2f6a2c', 'center'); X.restore(); }
