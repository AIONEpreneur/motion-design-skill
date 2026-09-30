// Grünwerk Gartenbau – V6 (ohne jeden Text wie das Original) im Stil von „A short story about a watermelon“ (Claude/Kevin Ngo):
// derselbe Garten bei Regen (Nachtblau, helle Konturen), in der Hitze (orange Schraffur), dann hinab in den Querschnitt,
// wo Schicht für Schicht gebaut wird (gestrichelte Konstruktionslinie zuerst, dann füllt sie sich). Zum Schluss Schild im Beet.
const Y0 = 300;
// Verdichtung: 0 = lockere Schicht mit Poren, 1 = zusammengepresst (auf „verdichtet“)
const SQ = t => eo(tin(t, K.verdichtet, .38)), CTOP = t => 380 + SQ(t) * 130;

// ---------- Kamera der Gartenwelt ----------
const SECT = [1, 960, 540], WIN = [1.35, 1560, -120], FIN = [1.35, 820, 30], FORKCAM = [.72, 960, 60];
function gardenCam(t) {
  const lerp3 = (a, b, k) => [mix(a[0], b[0], k), mix(a[1], b[1], k), mix(a[2], b[2], k)];
  if (t < 2.95) return [mix(1.4, 1.46, lin(t, 0, 2.95)), 800, 20];
  if (t < 6.72) return t < 4.72 ? [mix(1.42, 1.46, lin(t, 2.95, 4.72)), mix(690, 680, lin(t, 2.95, 4.72)), 95] : lerp3([1.46, 680, 95], WIN, eio(lin(t, 4.72, 5.02)));
  if (t < 20.85) { const k = eio(lin(t, 6.72, 7.05)); let c = k < 1 ? lerp3(WIN, SECT, k) : [mix(1, 1.04, lin(t, 7.05, 20.85)), 960 + 40 * Math.sin((t - 7.05) * .45), 540 + 20 * lin(t, 12.6, 13.2)];
    // Grünwerk kommt: Kamera zieht auf, damit die Gabel mit dem Grünwerk-Etikett ganz im Bild ist, dann wieder hinein
    const z = eio(lin(t, 9.45, 9.8)) * (1 - eio(lin(t, 10.5, 10.8))); if (z > 0) c = lerp3(c, FORKCAM, z); return c; }
  const k = eio(lin(t, 20.85, 21.15)); const c = lerp3([1.02, 960, 560], FIN, k); if (k >= 1) c[0] = mix(1.35, 1.4, lin(t, 21.15, 24.45)); return c;
}

// ---------- Erdreich ----------
const ROOTS = [];
(function () { const R = rng(77); for (let i = 0; i < 11; i++) { const x0 = 180 + i * 160 + R() * 60, d = 780 + R() * 180, pts = []; let x = x0; for (let y = 325; y <= d; y += 12) { x += (R() - .5) * 9; pts.push([x, y]); }
  const br = []; for (let b = 0; b < 4; b++) { const s = Math.floor(pts.length * (.18 + b * .18)), [bx, by] = pts[s], dir = b % 2 ? 1 : -1, bp = [[bx, by]]; let px = bx, py = by; for (let j = 0; j < 9; j++) { px += dir * (7 + R() * 5); py += 6 + R() * 5; bp.push([px, py]); } br.push({ s: s / pts.length, pts: bp }); }
  ROOTS.push({ pts, br }); } })();
function soilWorld(t, st) {
  const L = st.loose || 0, x0 = -700, x1 = 2700;
  // Unterboden
  soilFill(S('sub', () => polyP([[x0, 600], [x1, 600], [x1, 1900], [x0, 1900]], true, 40), 0), P.soil, 3, [x0, 600, x1, 1900]);
  strata(760, x0, x1, 1); strata(1020, x0, x1, 2.3);
  // trockene Oberkrume
  soilFill(S('dryk', () => polyP([[x0, 322], [x1, 322], [x1, 642], [x0, 642]], true, 40), 0), P.soilL, 17, [x0, 322, x1, 642], { hatchA: .45, pebEvery: 60000 });
  // verdichtete Schicht (wird bei „verdichtet“ zusammengedrückt)
  if (L < 1) { const q = st.squeeze || 0, top = 380 + q * 130, sc = (640 - top) / 260; X.save(); X.translate(0, 640); X.scale(1, sc); X.translate(0, -640);
    const cp = S('cmp', () => polyP([[x0, 380], [x1, 380], [x1, 640], [x0, 640]], true, 40), 0);
    soilFill(cp, mixCol('#9c7e63', '#5a4538', q), 5, [x0, 380, x1, 640], { hc: 16, hatchA: .45 + .35 * q, flat: 1 - q * .6, pebEvery: 9000, clumpEvery: 5000 });
    // Luftporen: vor dem Pressen offen, danach zugedrückt
    if (q < 1) { const R = rng(44); X.save(); X.lineWidth = 2 / Math.max(sc, .3); for (let i = 0; i < 120; i++) { const x = x0 + 700 + R() * 2100, y = 395 + R() * 230, r = (7 + R() * 9) * (1 - q); if (r < .6) continue; X.beginPath(); X.ellipse(x, y, r * 1.3, r, R() * .6 - .3, 0, 7); X.fillStyle = F('#e9dcc0'); X.fill(); X.strokeStyle = hexA(P.ink, .7); X.stroke(); } X.restore(); }
    X.strokeStyle = F(P.compactD); X.lineWidth = 2.6 / sc; for (let i = 0; i < 6; i++) { const y = 400 + i * 40; X.beginPath(); for (let x = x0; x <= x1; x += 40) X.lineTo(x, y + Math.sin(x * .01 + i) * 3); X.stroke(); }
    X.restore(); strata(640, x0, x1, 4, P.compactD, 1); if (q > 0) strata(top, x0, x1, 8, '#3d2c22', q); }
  // gelockerte Schicht wächst vom Gabelstich aus
  if (L > 0) { X.save(); X.beginPath(); X.arc(st.lx || 960, 560, 1700 * eo(L), 0, 7); X.clip();
    const lp = S('loose', () => polyP([[x0, 325], [x1, 325], [x1, 840], [x0, 840]], true, 40), 0);
    soilFill(lp, P.soil, 9, [x0, 325, x1, 840], { hatchA: .35, pebEvery: 40000 });
    const R = rng(12); for (let i = 0; i < 520; i++) { const x = x0 + R() * (x1 - x0), y = 330 + R() * 505, r = 7 + R() * 15; X.beginPath(); X.ellipse(x, y, r, r * (.7 + R() * .3), R() * 3, 0, 7); X.fillStyle = F(R() > .5 ? P.soilL : '#8a6446'); X.fill(); X.strokeStyle = hexA(OL(), .55); X.lineWidth = 1.6; X.stroke();
      if (R() > .6) { X.fillStyle = F('#f0e6cf'); X.beginPath(); X.ellipse(x + r * 1.2, y + r * .3, r * .4, r * .25, R(), 0, 7); X.fill(); } }
    X.restore(); if (L < 1) { X.save(); X.strokeStyle = OL(); X.lineWidth = 2.4; X.globalAlpha = 1 - L; const rr0 = 1700 * eo(L); for (let i = 0; i < 26; i++) { const a = i / 26 * 6.28; X.beginPath(); X.moveTo(960 + Math.cos(a) * rr0, 560 + Math.sin(a) * rr0); X.lineTo(960 + Math.cos(a + .03) * (rr0 - 40), 560 + Math.sin(a + .03) * (rr0 - 40)); X.stroke(); } X.restore(); } }
  // Kies
  if (st.gravel > 0) { const g = st.gravel; X.save(); const gp = S('grv', () => polyP([[x0, 840], [x1, 840], [x1, 1000], [x0, 1000]], true, 40), 0);
    X.globalAlpha = clamp(g * 3); X.fillStyle = F('#8d7a64'); X.fill(gp); X.globalAlpha = 1;
    const R = rng(21); for (let i = 0; i < 150; i++) { const x = -200 + (i % 30) * 80 + R() * 40, row = Math.floor(i / 30), y = 862 + row * 32 + R() * 10, d0 = (x + 200) / 2400 * .5 + row * .04, k = eo(clamp((g - d0) / .34)); if (k <= 0) continue;
      pebble(x, mix(600, y, k) - Math.sin(k * Math.PI) * 30 * (1 - k), 22 + R() * 10, 15 + R() * 6, R() - .5, R() > .5 ? P.gravel : '#b0a591'); }
    X.restore(); strata(840, x0, x1, 5, P.strata, .9); strata(1000, x0, x1, 6, P.strata, .9); }
  // Mutterboden mit Kompost
  if (st.top > 0) { const hgt = 100 * eo(st.top); X.save(); X.beginPath(); X.rect(x0, 425 - hgt, x1 - x0, hgt); X.clip();
    const tp = S('tops', () => polyP([[x0, 322], [x1, 322], [x1, 425], [x0, 425]], true, 40), 0); soilFill(tp, P.topsoil, 13, [x0, 322, x1, 425], { hatchA: .5, pebbles: false, clumpEvery: 2500 });
    const R = rng(31); for (let i = 0; i < 90; i++) { const x = x0 + 700 + R() * 2000, y = 335 + R() * 80, k = back(lin(t, K.kompost - .35 + R() * .1, K.kompost - .05 + R() * .05)); if (k <= 0) continue; X.save(); X.translate(x, y); X.rotate(R() * 6); X.scale(k, k); const kind = i % 3;
      if (kind === 0) { leaf(0, 0, 0, .45, R() > .5 ? '#a9a24a' : '#7d9a4a'); } else if (kind === 1) { X.fillStyle = F('#f3ecdc'); X.beginPath(); X.moveTo(-8, -5); X.lineTo(9, -7); X.lineTo(6, 6); X.lineTo(-7, 5); X.closePath(); X.fill(); X.strokeStyle = OL(); X.lineWidth = 1.6; X.stroke(); } else { X.strokeStyle = F('#8a5a32'); X.lineWidth = 3; X.beginPath(); X.moveTo(-10, 0); X.lineTo(10, 2); X.stroke(); } X.restore(); }
    X.restore(); strata(425, x0, x1, 7, '#3a261b', clamp(st.top * 2)); }
  // Grasnarbe (Soden)
  const turf = S('turf', () => polyP([[x0, 300], [x1, 300], [x1, 326], [x0, 326]], true, 40), 0);
  const tc = st.turfCol || P.lawn; X.fillStyle = F(tc); X.fill(turf); X.save(); X.clip(turf); X.strokeStyle = F(mixCol(tc, '#2e4a20', .35)); X.lineWidth = 1.4; X.beginPath(); for (let x = x0; x < x1; x += 7) { X.moveTo(x, 302); X.lineTo(x + 2, 326); } X.stroke(); X.restore();
  X.strokeStyle = OL(); X.lineWidth = 2.6; X.beginPath(); X.moveTo(x0, 326); X.lineTo(x1, 326); X.stroke();
}
function waterLens(h, x0 = 320, x1 = 1450, y = 380) { if (h <= 1) return; const p = new Path2D(); p.moveTo(x0, y); for (let x = x0; x <= x1; x += 20) { const u = (x - x0) / (x1 - x0); p.lineTo(x, y - h * Math.sin(u * Math.PI) * (1 + .1 * Math.sin(x * .05))); } p.lineTo(x1, y); p.closePath();
  X.fillStyle = F(P.water); X.fill(p); X.strokeStyle = OL(); X.lineWidth = 2.6; X.stroke(p); X.save(); X.clip(p); X.strokeStyle = 'rgba(255,255,255,.55)'; X.lineWidth = 2; for (let i = 0; i < 6; i++) { const yy = y - h * .3 - i * 8, xx = x0 + 150 + i * 150; X.beginPath(); X.moveTo(xx, yy); X.quadraticCurveTo(xx + 30, yy - 6, xx + 60, yy); X.stroke(); } X.restore(); }

// ---------- V7: Anmerkungen am Querschnitt wie im Lehrbuch ----------
// Handschrift in Tinte, blauer Konstruktions-Pfeil zeichnet sich in 0,25 s zum Objekt; alles ist 0,25 s vor dem Wort ganz da,
// bleibt stehen, solange der Querschnitt zu sehen ist, und sammelt sich zum beschrifteten Bodenaufbau.
const INK = '#2b2622', NS = 50;
function noteArrow(t, t0, pts) { const k = eo(lin(t, t0, t0 + .25)); if (k <= 0) return; const sub = polySub(pts, 0, k); if (sub.length < 2) return; const done = k > .96, a = pts[pts.length - 2], b = pts[pts.length - 1], ang = Math.atan2(b[1] - a[1], b[0] - a[0]);
  // heller Rand unter dem Pfeil, damit Blau auf brauner Erde lesbar bleibt
  X.save(); X.globalAlpha *= .85; X.strokeStyle = '#f6f1e2'; X.lineWidth = 10; X.lineCap = 'round'; X.lineJoin = 'round'; X.stroke(pathOf(sub)); if (done) arrowHead(b[0], b[1], ang, 20, '#f6f1e2', 10); X.restore();
  bLine(sub, 1, null, 4.2); if (done) arrowHead(b[0], b[1], ang, 20, P.blue, 4.2); }
// Anmerkung auf Papierstreifen (auf der Erde wäre Tinte unlesbar); w = Wortzeit, fertig bei w - 0,25
function note(t, w, x, y, txt, target, out, o = {}) { const t0 = w - .5, a = lin(t, t0, t0 + .1) * out; if (a <= 0) return;
  X.save(); X.globalAlpha = a; X.font = `700 ${NS}px KA`; const tw = X.measureText(txt).width;
  if (o.tag !== false) { const tg = S('note' + txt, () => rrP(x - 16, y - 48, tw + 32, 66, 10), .6); X.save(); X.translate(6, 6); hatch(tg, OL(), 8, 1, .3); X.restore(); ink(tg, '#f6f1e2', 2.6); }
  X.fillStyle = INK; X.fillText(txt, x, y);
  if (o.strike) { const k = eo(lin(t, o.strike - .5, o.strike - .35)); if (k > 0) { X.strokeStyle = P.red; X.lineWidth = 4.5; X.lineCap = 'round'; X.beginPath(); X.moveTo(x - 6, y - 12); X.lineTo(x - 6 + (tw + 12) * k, y - 18 - 2 * k); X.stroke(); } }
  if (target) noteArrow(t, t0, typeof target === 'function' ? target(tw) : target);
  X.restore(); return tw; }
function sectionNotes(t) {
  const out = 1 - lin(t, 20.82, 21.0), nx = 120;
  // „verdichtet“ zeigt auf die gepresste Schicht; beim Lockern durchgestrichen, darunter „gelockert“
  note(t, K.verdichtet, nx, 582, 'verdichtet', tw => [[nx + tw + 20, 566], [500, CTOP(t) + (640 - CTOP(t)) * .5]], out, { strike: K.lockert });
  note(t, K.lockert, nx, 512, 'gelockert', tw => [[nx + tw + 20, 496], [500, 470]], out);
  note(t, K.kies, nx, 940, 'Kies', tw => [[nx + tw + 20, 924], [440, 924]], out);
  note(t, K.versickert, nx, 770, 'versickert', tw => [[nx + tw + 20, 754], [440, 754]], out);
  // Kompost: Etikett in der neuen dunklen Oberschicht, Pfeil zu den Kompost-Stückchen
  note(t, K.kompost, nx, 398, 'Kompost', tw => [[nx + tw + 20, 380], [440, 374]], out);
  // Lupe auf die gepresste Schicht: die Poren schließen sich genau beim Pressen
  const lk = tin(t, K.verdichtet, .3) * (1 - lin(t, 9.3, 9.45)); if (lk > 0) pressLens(1570, 585, 150, lk, SQ(t), 1330, CTOP(t) + (640 - CTOP(t)) * .5);
}

function pressLens(cx, cy, r, k, q, tx, ty) { X.save(); X.globalAlpha = clamp(k * 1.6);
  bLine([[tx, ty], [cx - r * .98, cy]], 1, [6, 6], 2.6); bCross(tx, ty, 10, 1);
  X.translate(cx, cy); X.scale(eo(k), eo(k)); const c = S('plens' + r, () => ellP(0, 0, r, r, 4), .5);
  X.fillStyle = F(mixCol('#8a6b52', '#4f3c30', q)); X.fill(c); X.save(); X.clip(c);
  // Körner: erst locker mit hellen Luftporen dazwischen, dann flachgedrückt und dicht an dicht
  const R = rng(9), rows = 9; for (let j = 0; j < rows; j++) for (let i = 0; i < 9; i++) { const gx = -r + i * 38 + (j % 2) * 19 + (R() - .5) * 8, gy0 = -r + 18 + j * 36, gy = mix(gy0, gy0 * .72 + 8, q), rx = 17 + R() * 6, ry = mix(13, 7, q) + R() * 2;
    X.beginPath(); X.ellipse(gx, gy, rx, ry, (R() - .5) * mix(.8, .15, q), 0, 7); X.fillStyle = F(R() > .5 ? '#a4856a' : '#8d6f58'); X.fill(); X.strokeStyle = OL(); X.lineWidth = 2; X.stroke();
    const pr = (1 - q) * (5 + R() * 5); if (pr > .5) { X.beginPath(); X.ellipse(gx + 19, gy + 16 * (1 - q * .5), pr * 1.3, pr, 0, 0, 7); X.fillStyle = '#efe4cc'; X.fill(); X.strokeStyle = hexA(P.ink, .6); X.lineWidth = 1.4; X.stroke(); } }
  X.restore(); X.strokeStyle = OL(); X.lineWidth = 4; X.stroke(c); X.strokeStyle = '#ffffff'; X.globalAlpha *= .6; X.lineWidth = 3; X.beginPath(); X.arc(0, 0, r - 10, -2.6, -1.9); X.stroke();
  X.restore(); }

// ---------- Gartenoberfläche ----------
function gardenSurface(t, st) {
  const va = st.vis ?? 1; X.save(); X.globalAlpha = va; if (va > 0) { swing(t, st.swingA ?? .04, 660, st.swingAng);
  house(t, { kids: st.kids ?? true, mood: st.kidMood || 'sad', lit: NIGHT > 0, fog: st.fog || 0, hands: st.hands }); } X.restore();
  // Rasenfarbe (trocken wird von links nach rechts braun)
  const dry = st.dry || 0;
  for (let seg = 0; seg < 12; seg++) { const xa = -200 + seg * 200, w = clamp(dry * 2.2 - seg / 12 * 1.2); grassLine(Y0, xa, xa + 200, t, P.grass, st.gh ?? 34, st.gd ?? 1, w, seg + 1); }
  if (dry > .6) { X.save(); X.globalAlpha = clamp((dry - .6) * 2.5); X.strokeStyle = OL(); X.lineWidth = 2.2; X.beginPath(); for (let i = 0; i < 9; i++) { const cx = 100 + i * 190; X.moveTo(cx, 326); X.lineTo(cx + 12, 350); X.lineTo(cx - 4, 372); X.lineTo(cx + 10, 396); } X.stroke(); X.restore(); }
}
function puddle(t, h) { if (h <= 1) return; const x0 = -500, x1 = 2400; const p = new Path2D(); p.moveTo(x0 - 20, Y0 + 2); for (let x = x0; x <= x1; x += 16) p.lineTo(x, Y0 - h + Math.sin(x * .03 + t * 5) * 3); p.lineTo(x1 + 20, Y0 + 2); p.closePath();
  X.save(); X.globalAlpha = .88; X.fillStyle = '#4d68c4'; X.fill(p); X.clip(p); X.globalAlpha = .5; X.strokeStyle = '#c9d2ff'; X.lineWidth = 2.4; X.lineCap = 'round'; X.beginPath(); for (let i = 0; i < 26; i++) { const x = -300 + hash(i * 4.4) * 2200 + Math.sin(t * 1.5 + i) * 20, y = Y0 - h + 16 + hash(i * 6.1) * Math.max(4, h - 26); X.moveTo(x, y); X.lineTo(x + 50 + hash(i) * 70, y); } X.stroke(); X.restore(); X.strokeStyle = OL(); X.lineWidth = 2.6; X.stroke(p);
  for (let i = 0; i < 7; i++) { const k = ((t * 1.4 + i * .37) % 1), x = 150 + hash(i * 3.1) * 1300; X.save(); X.globalAlpha = 1 - k; X.strokeStyle = '#e9e7f4'; X.lineWidth = 2; X.beginPath(); X.ellipse(x, Y0 - h + 2, 10 + k * 40, 3 + k * 9, 0, 0, 7); X.stroke(); X.restore(); } }

// ================= Szenen =================
function sceneGarden(t) {
  const rainy = t < 2.95, final = t >= 20.85;
  NIGHT = rainy ? 1 : 0;
  if (rainy) nightBG(t); else paperBG(t);
  const [s, cx, cy] = gardenCam(t); X.save(); cam(s, cx, cy);
  // Himmel
  if (rainy) { cloud(900, -520, 1.6, 'a', '#7e82a8'); cloud(1500, -560, 1.2, 'b', '#7e82a8'); }
  else if (!final && t < 5.0) { const hot = lin(t, 3.0, 3.23); X.save(); X.globalAlpha = 1 - lin(t, 4.72, 4.97); sun(300, -140, 85, t, hot); bArc(300, -140, 160, -2.6, -.4, .6, [6, 8]); bCross(300, -140, 12, .6); X.restore(); }
  // Erdreich
  const lensH = t < 6.72 ? 0 : mix(34, 0, eio(lin(t, 14.0, K.ab)));
  // Rasen wird auf „braun“ braun (Welle von links nach rechts, 4,18–4,54 s; sichtbarer Teil ist bei 4,46 braun), ab „Die Wurzeln“ wieder grün
  const dryK = t < 2.95 ? 0 : (t < 17.95 ? lin(t, K.braun - .3, K.braun + .06) : 1 - lin(t, 17.95, 18.4));
  const st = { squeeze: SQ(t), loose: eo(lin(t, K.lockert - .1, K.lockert + .5)), gravel: lin(t, K.kies - .6, K.kies), top: lin(t, K.mutter - .4, K.mutter),
    turfCol: mixCol(P.lawn, P.dry, dryK) };
  if (NIGHT) { X.fillStyle = '#202145'; X.fillRect(-700, Y0, 3400, 1600); X.strokeStyle = hexA('#9aa3e0', .35); X.lineWidth = 2; X.beginPath(); for (let i = 0; i < 14; i++) { const y = Y0 + 30 + i * 26, x = hash(i) * 1600; X.moveTo(x, y); X.lineTo(x + 120 + hash(i * 3) * 200, y); } X.stroke(); }
  else soilWorld(t, st);
  waterLens(lensH, 320, 1450, 302);
  // alte, gestauchte Wurzeln (vor dem Lockern)
  const oldA = 1 - lin(t, K.lockert, K.lockert + .4);
  if (oldA > 0 && t > 6.5) { X.save(); X.globalAlpha = oldA; for (let i = 0; i < 9; i++) { const x = 260 + i * 170; root([[x, 326], [x + 3, 350], [x + 2, 372], [x + 20, 380], [x + 50, 378], [x + 70, 372]], 1, 3); } X.restore(); }
  // neue Wurzeln
  if (t > 17.95) ROOTS.forEach((r, i) => { const k = eo(lin(t, 18.0 + i * .03, K.tief2 - .05)); root(r.pts, k, 6); r.br.forEach(b => root(b.pts, clamp((k - b.s) / .25), 3.4)); });
  // Oberfläche
  // leere Schaukel pendelt aus (Kinder spielen drinnen)
  const swB = eo(lin(t, 4.72, 5.0)), swingAng = t >= 4.72 && t < 7 ? mix(Math.sin(t * 1.6) * .1, (.4 * Math.exp(-(t - 4.72) * 1.05) + .03) * Math.cos(2.5 * (t - 4.72)), swB) : null;
  const gh = final ? 50 : rainy ? 34 : mix(62, 40, lin(t, 6.72, 7.05)), gd = final ? 1.5 : rainy ? 1 : 1.6;
  gardenSurface(t, { swingA: .1, swingAng, gh, gd, vis: 1 - lin(t, 6.72, 6.95) + lin(t, 20.85, 21.05), kids: !final, dry: dryK, kidMood: final ? 'happy' : 'sad', fog: lin(t, 6.1, K.drinnen) * (1 - lin(t, 6.7, 6.9)), hands: t > 5.6 && t < 6.9 });
  // Regen: das Wasser steigt bis zum Wort „Wasser“ sichtbar über den ganzen Garten
  const wH = 105 * eio(lin(t, .35, K.wasser));
  if (rainy) { ball(760 + t * 18, Y0 - Math.max(34, wH + 6) + Math.sin(t * 3) * 4, 34, Math.sin(t * 2) * .3, t); puddle(t, wH); }
  else if (!final) { if (lensH > 1) ball(1080, 302 - lensH * .86 - 24 + Math.sin(t * 3) * 3, 34, Math.sin(t * 2) * .2, t); else ball(1080, Y0 - 34, 34, .4, t); }
  // Ameise
  if (rainy) { const h = wH; X.save(); X.translate(430, Y0 - h + Math.sin(t * 3.4) * 5); X.rotate(Math.sin(t * 2.6) * .08); leaf(-120, 0, 0, 4.6, P.leaf); ant(0, -8, .66, t, { noShadow: true }); X.restore(); }
  else if (t < 5.02) { const x = mix(360, 660, lin(t, 2.95, 5.02)); ant(x, Y0, .95, t, { walk: 1, sweat: t > 3.4, hold: () => drop(150, -250, 2.2) }); }
  // Hitze: Wellen über dem Boden
  if (!rainy && t < 5.02) { const hk = lin(t, 3.0, 3.23) * (1 - lin(t, 4.72, 5.02)); X.save(); X.globalAlpha = hk * .8; X.strokeStyle = '#e0452f'; X.lineWidth = 2.4; for (let i = 0; i < 6; i++) { const x = 150 + i * 200, y = Y0 - 80 - ((t * 40 + i * 30) % 120); X.beginPath(); for (let j = 0; j < 8; j++) X.lineTo(x + Math.sin(j * 1.2 + t * 4) * 8, y - j * 10); X.stroke(); } X.restore(); }
  // Querschnitt-Handlung
  if (t > 6.9 && t < 21.0) sectionNotes(t);
  if (t > 6.7 && t < 20.9) sectionAction(t);
  if (t > 6.9 && t < 20.9) ant(mix(1520, 1860, lin(t, 6.9, 20.9)), Y0, .5, t, { walk: 1 });
  if (final) finalSurface(t);
  X.restore();
  // Überlagerungen im Bild
  if (rainy) rain(t, 1, 1.2);
  if (!rainy && t < 5.02) { const hk = lin(t, 3.0, 3.23) * (1 - lin(t, 4.72, 5.02)); X.save(); X.globalAlpha = hk * .42; X.fillStyle = hatchTile('#ec8a4c', 20, 1.8, 3, 2); X.fillRect(0, 0, W, H); X.globalAlpha = hk * .12; X.fillStyle = '#f2a25c'; X.fillRect(0, 0, W, H); X.restore(); }
  grain();
}
function sectionAction(t) {
  // Wasser kommt nicht durch: Tropfen prallen auf der verdichteten Schicht ab
  if (t < 10.2) for (let i = 0; i < 10; i++) { const per = .7, ph = ((t + i * .13) % per) / per, x = 380 + i * 105; const a = 1 - lin(t, 9.9, 10.2); const ty = CTOP(t); if (ph < .6) drop(x, mix(250, ty - 10, ph / .6), .8, a); else { const k = (ph - .6) / .4; X.save(); X.globalAlpha = a * (1 - k); X.strokeStyle = P.blue; X.lineWidth = 2.4; X.beginPath(); X.ellipse(x, ty, 8 + k * 26, 3 + k * 6, 0, Math.PI, 0); X.stroke(); X.restore(); } }
  // Druckpfeile bei „verdichtet“
  // „Ihr Boden“: gestrichelter Rahmen um die Schicht; „verdichtet“: Pfeile drücken sie sichtbar zusammen
  const ty = CTOP(t), fa = tin(t, K.boden, .3) * (1 - lin(t, 9.35, 9.6));
  if (fa > 0) { X.save(); X.globalAlpha = fa; bLine([[20, ty - 8], [1900, ty - 8], [1900, 650], [20, 650], [20, ty - 8]], 1, [14, 10], 3); X.restore(); }
  const pa = lin(t, K.verdichtet - .62, K.verdichtet - .4) * (1 - lin(t, 9.35, 9.6)); if (pa > 0) { const ay = mix(150, 372, eo(lin(t, K.verdichtet - .62, K.verdichtet - .38))) + SQ(t) * 130; X.save(); X.globalAlpha = pa; for (let i = 0; i < 5; i++) { const x = 280 + i * 340; bLine([[x, ay - 120], [x, ay]], 1, null, 5); arrowHead(x, ay, Math.PI / 2, 20, P.blue, 5); } X.restore(); }
  if (t > K.verdichtet - .05 && t < K.verdichtet + .5) for (let i = 0; i < 3; i++) burst(480 + i * 480, ty + 20, 40, 90, 10, 1 - lin(t, K.verdichtet, K.verdichtet + .5));
  // Grabegabel von Grünwerk
  if (t > 9.4 && t < 13.0) { const dn = eio(lin(t, K.lockert - .28, K.lockert)), up = eio(lin(t, 12.55, 12.95)), tipY = mix(mix(-900, 200, eo(lin(t, 9.4, 9.8))), 840, dn) - up * 900, wig = t > K.lockert && t < K.lockert + .8 ? Math.sin((t - K.lockert) * 30) * .04 * (1 - lin(t, K.lockert, K.lockert + .8)) : 0;
    X.save(); X.beginPath(); X.rect(-700, -2000, 3400, 2000 + 326); X.clip(); fork(960, tipY, wig, t); X.restore();
    X.save(); X.beginPath(); X.rect(-700, 326, 3400, 2000); X.clip(); X.globalAlpha = .92; fork(960, tipY, wig, t); X.restore();
    if (t > K.lockert - .03 && t < K.lockert + .5) burst(960, 300, 70, 130, 12, 1 - lin(t, K.lockert, K.lockert + .5), .2); }
  // Maßstab direkt neben den Zinken: die Zinken reichen genau 30 cm tief; einzige Zahl „30 cm“, fertig auf „dreißig“
  const rk = eo(lin(t, K.n30 - .55, K.n30 - .12)) * (1 - lin(t, 12.8, 13.0));
  if (rk > 0) { const x = 1110; X.save(); X.globalAlpha = clamp(rk * 3) * (1 - lin(t, 12.8, 13.0)); const rs = S('rstick', () => rrP(x - 14, 316, 96, 546, 10), .6); ink(rs, '#f6f1e2', 2.6); X.restore(); bLine([[x, 326], [x, mix(326, 840, rk)]], 1, null, 3); for (let c = 0; c <= 30; c++) { const y = 326 + c * (514 / 30); if (y > mix(326, 840, rk)) break; bLine([[x, y], [x + (c % 10 === 0 ? 36 : c % 5 === 0 ? 24 : 12), y]], 1, null, c % 10 === 0 ? 3 : 2); } }
  const tk30 = tin(t, K.n30, .3), ta30 = 1 - lin(t, 12.8, 13.0); if (tk30 > 0 && ta30 > 0) { X.save(); X.globalAlpha = ta30; X.translate(1144, 905); X.scale(back(tk30), back(tk30)); const tg = S('rtag', () => rrP(-92, -34, 184, 68, 12), .6); ink(tg, '#f6f1e2', 2.8); hand('30 cm', 0, 16, 50, P.blue, 'center'); X.restore(); }
  const dk = eo(tin(t, K.tief1, .35)) * (1 - lin(t, 12.8, 13.0)); if (dk > 0) { bLine([[200, 840], [mix(200, 1800, dk), 840]], 1, [14, 10], 3); if (dk > .95) arrowHead(1800, 840, 0, 14, P.blue, 3); }
  // Kies: gestrichelter Rahmen zuerst
  const gk = eo(lin(t, K.darunter - .35, K.darunter)) * (1 - lin(t, 15.3, 15.6)); if (gk > 0) { X.save(); X.globalAlpha = gk; bLine([[-100, 840], [2100, 840]], 1, [14, 10], 3); bLine([[-100, 1000], [2100, 1000]], 1, [14, 10], 3); X.restore(); }
  // Wasser läuft ab: Tropfen sinken aus der Pfütze durch die gelockerte Erde in den Kies und laufen darin zur Seite weg
  if (t > 13.8 && t < 15.8) for (let i = 0; i < 18; i++) { const s0 = 13.83 + i * .05, k = lin(t, s0, s0 + 1.05); if (k <= 0 || k >= 1) continue; const xs = 380 + (i % 9) * 125 + (i > 8 ? 60 : 0); let x, y; if (k < .5) { x = xs + Math.sin(k * 20 + i) * 6; y = mix(300, 915, eio(k / .5)); } else { const u = (k - .5) / .5; x = mix(xs, 2050, u * u); y = 915 + Math.sin(k * 26 + i) * 22; } drop(x, y, 1.25); }
  const fk = lin(t, 14.3, 14.62) * (1 - lin(t, 15.5, 15.8)); if (fk > 0) { X.save(); X.globalAlpha = fk; X.fillStyle = hexA(P.water, .3); X.fillRect(-200, 870, 2400, 125); X.strokeStyle = P.blue; X.lineWidth = 3.4; X.lineCap = 'round'; X.setLineDash([46, 30]); X.lineDashOffset = -t * 320; for (let r = 0; r < 3; r++) { const yy = 895 + r * 34; X.beginPath(); for (let x = -200; x <= 2200; x += 20) X.lineTo(x, yy + Math.sin(x * .012 + r * 2) * 6); X.stroke(); } X.restore(); }
  const ak = tin(t, K.ab, .35) * (1 - lin(t, 15.4, 15.7)); if (ak > 0) for (let i = 0; i < 3; i++) { const y = 895 + i * 34; bLine([[1500, y], [mix(1500, 1860, ak), y]], 1, null, 4.4); if (ak > .9) arrowHead(1860, y, 0, 14, P.blue, 3.4); }
  // Mutterboden: gestrichelte Linie zuerst, dann rieseln Krümel
  const tk = eo(lin(t, K.oben - .35, K.oben)) * (1 - lin(t, 17.9, 18.2)); if (tk > 0) { X.save(); X.globalAlpha = tk; bLine([[-100, 425], [2100, 425]], 1, [14, 10], 3); X.restore(); }
  if (t > K.mutter - .6 && t < K.mutter + .1) { X.save(); X.fillStyle = F(P.topsoil); for (let i = 0; i < 130; i++) { const x = hash(i * 2.2) * 1920, y = ((t - K.mutter + .6) * 900 + hash(i * 3.3) * 400) % 420 - 100; X.beginPath(); X.arc(x, y, 6 + hash(i) * 1.4 * 5, 0, 7); X.fill(); } X.restore(); }
  if (t > K.kompost - .3 && t < 20.9) worm(mix(2100, 1250, eo(lin(t, K.kompost - .3, 18.8))), 378, 1.25, t);
  // Lupe mit Wurzelhaaren
  const mk = lin(t, K.tief2 - .35, K.tief2) * (1 - lin(t, 20.6, 20.85)); magnifier(1600, 640, 150, mk, t, ROOTS[8].pts[40][0], ROOTS[8].pts[40][1]);
  // Regen versickert
  if (t > 19.2 && t < 20.9) { rainWorld(t, lin(t, 19.2, 19.4) * (1 - lin(t, 20.5, 20.8))); for (let i = 0; i < 12; i++) { const s0 = 19.4 + i * .04, k = lin(t, s0, s0 + 1.2); if (k <= 0 || k >= 1) continue; const x = 460 + i * 105 + Math.sin(k * 12 + i) * 8; drop(x, mix(260, 960, k), .9, 1 - lin(k, .9, 1)); } }
  // V7: Tropfen laufen auf „versickert“ noch sichtbar nach unten (der Pfeil zeigt auf sie), versickern bis 20,5 s im Kies
}
function rainWorld(t, a) { if (a <= 0) return; X.save(); X.globalAlpha = a; X.strokeStyle = P.blue; X.lineWidth = 2.2; X.lineCap = 'round'; X.beginPath(); for (let i = 0; i < 90; i++) { const x = hash(i * 1.3) * 2100 - 100, y = ((hash(i * 5.1) * 500 + t * 1400) % 560) - 280, l = 20 + hash(i) * 20; X.moveTo(x - y * .15, y); X.lineTo(x - (y + l) * .15, y + l); } X.stroke(); X.restore(); }
function finalSurface(t) {
  // Blumen, Kind mit Ball, Tag/Nacht wechselt – der Rasen bleibt grün
  for (let i = 0; i < 12; i++) flower(80 + i * 165 + hash(i) * 40, Y0 - 8 - hash(i * 3) * 10, .9);
  const kk = Math.max(0, 1 - Math.abs(t - K.gruen) / .22) * (t < K.gruen + .22 ? 1 : 1);
  kid(620, Y0, .95, t, t < K.gruen ? eo(lin(t, K.gruen - .35, K.gruen)) : 1 - eo(lin(t, K.gruen, K.gruen + .35)));
  const bk = lin(t, K.gruen, K.gruen + .8); let bx = 740, by = Y0 - 34;
  if (bk > 0) { bx = mix(740, 1250, bk); by = Y0 - 34 - Math.sin(bk * Math.PI) * 320; if (t > K.gruen + .8) { const b2 = lin(t, K.gruen + .8, K.gruen + 1.3); bx = mix(1250, 1330, b2); by = Y0 - 34 - Math.sin(b2 * Math.PI) * 60; } }
  ball(bx, by, 34, t * 6 * (bk > 0 && bk < 1 ? 1 : 0), t); if (t > K.gruen - .03 && t < K.gruen + .4) burst(760, Y0 - 40, 40, 80, 9, 1 - lin(t, K.gruen, K.gruen + .4));
  ant(mix(900, 1060, lin(t, 21, 24.4)), Y0, .8, t, { antUp: .3, walk: 1 });
  // Tag/Nacht-Band und Strichliste
  const band = S('band', () => polyP([[-100, -555], [2100, -555], [2100, -490], [-100, -490]], true, 40), 0);
  X.save(); X.fillStyle = F('#f6e8b8'); X.fill(band); X.restore(); X.strokeStyle = OL(); X.lineWidth = 2.4; X.beginPath(); X.moveTo(-100, -490); X.lineTo(2100, -490); X.stroke();
  const sx = 200 + ((t - 20.85) * 420) % 1700; X.save(); X.translate(sx, -522); const sp = S('bsun', () => ellP(0, 0, 20, 20, 3), .4); ink(sp, P.sun, 2.4); X.restore();
  const rk = lin(t, K.regen3 - .35, K.regen3) * (1 - lin(t, K.regen3 + .5, K.regen3 + .7)); if (rk > 0) { X.save(); X.globalAlpha = rk; cloud(760, -240, 1.25, 'r', '#b9bccc'); X.restore(); rainWorld(t, rk); }
  const hk = lin(t, K.hitze - .35, K.hitze) * (1 - lin(t, K.hitze + .6, K.hitze + .9)); sun(1060, -330, 60 + hk * 12, t, hk);
  if (hk > 0) { X.save(); X.globalAlpha = hk * .25; X.fillStyle = hatchTile('#ec8a4c', 20, 1.8, 3, 2); X.fillRect(-200, -700, 2400, 1000); X.restore(); }
  tally(130, -150, Math.min(12, Math.floor(lin(t, 21.3, 24.0) * 12) + 1));
}

// ---------- Schluss: Schild im Beet ----------
function sceneEnd(t) {
  NIGHT = 0; paperBG(t);
  X.save(); cam(mix(1, 1.04, lin(t, 24.45, 29.66)), 960, 560);
  const gy = 780;
  sun(1720, 150, 70, t, 0);
  // Mini-Querschnitt mit den drei guten Schichten
  X.save(); X.translate(0, gy - 300);
  soilWorld(t, { loose: 1, gravel: 1, top: 1, turfCol: P.lawn, lx: 960 });
  ROOTS.forEach(r => { root(r.pts, .6, 3.5); });
  X.restore();
  grassLine(gy, -100, 2020, t, P.grass, 34, 1, 0, 3);
  for (let i = 0; i < 10; i++) flower(120 + i * 190, gy - 10, .8);
  // Schild wird eingeschlagen (Tock bei ende+0,55)
  // Schild steht schon auf „Grünwerk“, wird dann mit einem Schlag eingeschlagen (Tock im Ton bei ende+0,55); Kontakt klein und ruhig danach
  const hit = K.ende + .5, drop = (t < hit ? 0 : eo(lin(t, hit, hit + .08)) * 64) - 64, bounce = t > hit && t < hit + .3 ? Math.sin((t - hit) / .3 * Math.PI) * -8 : 0;
  X.save(); X.translate(1250, gy - 10 + drop + bounce); X.scale(1.22, 1.22); sign(0, 0, t, { contact: 'gruenwerk-gartenbau.de · 0761 290 44 18', ca: lin(t, 25.7, 26.1) }); X.restore();
  if (t > hit && t < hit + .45) burst(1200, gy, 50, 110, 12, 1 - lin(t, hit, hit + .45), .2);
  ant(mix(980, 1400, lin(t, 24.5, 29)), gy - 10 - 520 * 1.22 + drop, .6, t, { walk: 1, noShadow: true });
  // Bodenprobe
  const pk = tin(t, K.probe, .32); sampleTube(470, gy + 6, 360, pk, t);
  if (pk > 0) { bArc(470, gy - 180, 250, -Math.PI * .9, -Math.PI * .1, pk * .7, [6, 8]); bCross(470, gy - 180, 12, pk * .7); }
  hangTag(522, gy - 400, 1, tin(t, K.kostenlos, .3), t, 'kostenlos');
  X.restore();
  grain();
}
function frame(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.globalCompositeOperation = 'source-over';
  if (t < 24.45) sceneGarden(t); else sceneEnd(t);
}
