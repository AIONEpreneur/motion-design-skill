// film.js (V7 Zahnfee): das Stück auf der Theaterbühne, Szene für Szene an den neu vermessenen Wortzeiten K / Schnitten CUT.
// V7: keine Satz-Laute mehr (BLOSS NICHT, GRÖSSER, EIN LEBEN LANG, NUR SPIELEN, HUIII, OHNE BOHREN, NOCHMAL entfernt).
// Text nur als Schild/Etikett am Objekt (ZAHNARZT, ANGST, ZAHNFEE, 20 MIN, Wochentage) und ein Comic-Laut (AUA!) wie BOOM!/SLAM! im Original.
// Betonung über Bildmittel: Lupe, roter Filzstift-Ring, rotes X, Aufleuchten, Zoom.
// Jede Schot-Funktion malt das ganze Bild und ist eine reine Funktion von t.
const CRIMSON = '#C23B4E', HEADC = '#2A1F33';
const CONF = [PAL.rose, PAL.ochre, PAL.sky, PAL.sap, PAL.violet, PAL.cream, GOLD];
const MARKER = s => `${s}px "Permanent Marker", cursive`, HAND = s => `800 ${s}px "Shantell Sans", sans-serif`;

// ---------- Theater ----------
function footlights(t) {
  for (let i = 0; i < 11; i++) {
    const fx = 110 + i * 170, on = .6 + .4 * pulse(t + i * .05, 3);
    paint(ellPts(fx, 1040, 46, 14, 14), { fill: '#FFE7A8', fillOp: 110 * on, bleed: .25, tex: .2, ink: null });
    paint(rrPts(fx - 22, 1030, 44, 20, 8), { wash: GOLD, ink: PAL.ink, sw: .7 });
  }
}
function audience(t, cheer = 0) {  // Zuschauerköpfe vorne (Bildschirmraum, nach camEnd)
  const bp = bpOf(t);
  for (let i = 0; i < 12; i++) {
    const x = -30 + i * 176 + hash(i + 70) * 40, bob = Math.abs(Math.sin((bp + hash(i) * .5) * Math.PI)) * (4 + 12 * cheer);
    const y = 1110 - bob + (i % 2) * 20, r = 70 + hash(i + 71) * 26;
    if (cheer > .15 && i % 3 !== 1) for (const sd of [-1, 1]) {
      const a = -Math.PI / 2 + sd * (.45 + .25 * Math.sin(bp * TAU + i)), L = r * 1.5 * cheer, sx = x + sd * r * .7, sy = y - r * .1;
      inkLine([[sx, sy], [sx + Math.cos(a) * L * .6, sy + Math.sin(a) * L * .6], [sx + Math.cos(a) * L, sy + Math.sin(a) * L]], 5.5, HEADC, 'marker', .4);
      paint(ellPts(sx + Math.cos(a) * L, sy + Math.sin(a) * L, 16, 16, 10), { wash: HEADC, ink: null });
    }
    paint(ellPts(x, y, r, r * 1.05, 18), { wash: HEADC, fill: PAL.violet, fillOp: 45, tex: .4, border: .3, ink: null });
    inkLine([[x - r * .7, y - r * .72], [x, y - r * 1.04], [x + r * .7, y - r * .72]], .7, GOLD, 'inkfine', .6);
  }
}
function puff(x, y, age, dir = 1) {
  if (age < 0 || age > .5) return;
  for (let k = 0; k < 3; k++) { const r = (18 + k * 8) * (.4 + easeOut(age / .5)); paint(ellPts(x - dir * (20 + k * 34) * easeOut(age / .4), y - 8 - k * 6, r, r * .75, 12), { fill: '#EADBC4', fillOp: 170 * (1 - age / .5), bleed: .15, tex: .3, ink: null }); }
}
function burstConfetti(x, y, age, n = 18, v0 = 600, up = -Math.PI / 2, spread = 2.6) {
  if (age < 0 || age > 2.2) return;
  for (let i = 0; i < n; i++) {
    const a = up + (hash(i + 7) - .5) * spread, v = v0 * (.6 + hash(i + 8) * .8), drag = 1 - Math.exp(-age * 3);
    push(); translate(x + Math.cos(a) * v * drag / 3, y + Math.sin(a) * v * drag / 3 + 180 * age * age); rotate(age * 8 + i); scale(Math.cos(age * 9 + i), 1);
    paint(rectPts(-11, -6, 22, 12), { wash: CONF[i % CONF.length], ink: null }); pop();
  }
}
function confettiRain(t, t0, n = 40) {
  if (t < t0) return;
  for (let i = 0; i < n; i++) {
    const ti = t0 + hash(i + 300) * 1.1; if (t < ti) continue;
    const age = t - ti, v = 230 + hash(i + 301) * 220, y = -40 + (age * v) % 1200, x = hash(i + 302) * 2040 - 60 + Math.sin(age * 2.2 + i) * 50;
    push(); translate(x, y); rotate(age * (2 + hash(i) * 4) + i); scale(Math.cos(age * 7 + i), 1); paint(rectPts(-11, -6, 22, 12), { wash: CONF[i % CONF.length], ink: null }); pop();
  }
}
function trapHole(hx, hy, open) { if (open < .02) return; const rx = 220 * open, ry = 46 * open;
  paint(rectPts(hx - rx, hy - 110 * open, rx * 2, 110 * open, 2), { wash: WOOD, fill: WOOD_DK, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1 });
  paint(ellPts(hx, hy, rx, ry, 26), { wash: '#2A1A22', ink: PAL.ink, sw: 1.2 }); }
function trapLip(hx, hy, open) { if (open < .02) return; const rx = 220 * open, ry = 46 * open, lip = [];
  for (let i = 0; i <= 14; i++) { const a = i / 14 * Math.PI; lip.push([hx + Math.cos(a) * rx, hy + Math.sin(a) * ry]); }
  paint([...lip, [hx - rx - 40, 1400], [hx + rx + 40, 1400]], { wash: WOOD, fill: WOOD_DK, fillOp: 60, bleed: .05, tex: .8, border: .6, ink: null }); inkLine(lip, 1.1, PAL.ink, 'ink', .4); }
function houseCurtain(t, hemY, split, sy0, sy1) {
  for (const sd of [-1, 1]) {
    const pts = [], outer = sd < 0 ? -120 : W + 120; pts.push([outer, -60]);
    for (let i = 0; i <= 14; i++) { const y = lerp(-60, hemY, i / 14), bump = split > 0 && y > sy0 ? Math.sin(clamp((y - sy0) / (sy1 - sy0)) * Math.PI * .5) * split : 0; pts.push([960 + sd * (bump + Math.sin(i * 1.3 + t * 2) * 4), y]); }
    for (let i = 0; i <= 10; i++) { const x = lerp(960, outer, i / 10); pts.push([x, hemY + Math.sin(i * 2.1) * 10 + (i % 2) * 12]); }
    paint(pts, { wash: CURTAIN, washOp: 255, fill: CURTAIN_DK, fillOp: 90, bleed: .05, tex: .8, border: .7, ink: PAL.ink, sw: 1.5 });
    for (let f = 1; f < 7; f++) { const fx = lerp(960, outer, f / 7), fl = []; for (let i = 0; i <= 6; i++) fl.push([fx + Math.sin(i * 1.4 + f) * 10, lerp(40, hemY - 20, i / 6)]); inkLine(fl, .9, CURTAIN_DK, 'inkfine', .5); }
    const fr = []; for (let i = 0; i <= 12; i++) { const x = lerp(960 + sd * split * .2, outer, i / 12); fr.push([x, hemY - 14 + (i % 2) * 10]); } inkLine(fr, 2.2, GOLD, 'ink', .3);
  }
}
// Kulisse „Zuhause, abends“: Nachtblau, Fenster mit Mond, Bilderrahmen (Problemwelt, kühl)
function homeSet(t) {
  paint(rectPts(-400, -400, W + 800, 1240), { wash: '#2C3A63', washOp: 255, fill: PAL.indigo, fillOp: 140, bleed: .08, tex: .8, border: .3, ink: null });
  for (let i = 0; i < 9; i++) inkLine([[i * 240 + 60, -40], [i * 240 + 60 + jit(3), 800]], .5, '#3E4C82', 'inkfine', 0);
  const x = 1150, y = 170, w = 280, h = 300;
  paint(rectPts(x, y, w, h, 3), { wash: '#3C4C8C', fill: PAL.violet, fillOp: 80, tex: .6, ink: PAL.ink, sw: 1.2 });
  paint(ellPts(x + w * .68, y + h * .28, w * .15, w * .15, 18, 2), { wash: PAL.cream, fill: PAL.ochre, fillOp: 50, ink: PAL.ink, sw: .8 });
  for (let i = 0; i < 4; i++) paint(starPts(x + w * (.12 + hash(i) * .45), y + h * (.12 + hash(i + 5) * .75), 6 + hash(i + 2) * 6, .4), { wash: PAL.cream, ink: null });
  inkLine([[x + w / 2, y], [x + w / 2, y + h]], 1.1, PAL.ink, 'ink', 0); inkLine([[x, y + h / 2], [x + w, y + h / 2]], 1.1, PAL.ink, 'ink', 0);
  paint(rectPts(x - 16, y + h - 4, w + 32, 22, 2), { wash: '#6B5A7E', ink: PAL.ink, sw: .9 });
  paint(rectPts(640, 230, 150, 110, 2), { wash: '#C9A66B', fill: WOODD, fillOp: 40, tex: .5, ink: PAL.ink, sw: 1 });
  paint(rectPts(656, 246, 118, 78, 1), { wash: '#8EC3E6', fill: PAL.sap, fillOp: 50, tex: .5, ink: PAL.ink, sw: .6 });
}
// Kulisse Zahnfee-Welt: gedämpfter Sonnenstrahl in Pfirsich/Gold mit fernen Hügeln (wie die Finale-Bühne im Original)
function warmSet(t) {
  paint(rectPts(-400, -400, W + 800, 1240), { wash: '#EFC9A0', washOp: 255, ink: null });
  sunburst(960, 520, '#DE8E68', '#EDBF78', t * .1, 16, 1500, 150);
  paint([[-400, 820], [-100, 560], [250, 660], [560, 520], [900, 650], [1250, 540], [1600, 640], [1900, 560], [2300, 700], [2300, 820]], { wash: '#C98C5E', fill: '#A86A45', fillOp: 70, bleed: .06, tex: .7, border: .5, ink: PAL.ink, sw: .9, curv: .4 });
  paint(ellPts(960, 560, 420, 220, 24), { fill: '#FFE7A8', fillOp: 60, bleed: .3, tex: .3, ink: null });
}
// Kulisse Mund: Rachen dunkelrot, Gaumen-Zähne oben, Zahnfleisch als Boden
function mouthSet(t, warm = 0) {
  paint(rectPts(-400, -400, W + 800, 1300), { wash: mixCol('#5A1F2E', '#7A3440', warm), washOp: 255, fill: '#3A1420', fillOp: 140, bleed: .08, tex: .8, border: .3, ink: null });
  paint(ellPts(960, 560, 820, 330, 30, 6), { fill: '#1E0A12', fillOp: 110, bleed: .3, tex: .4, ink: null });   // Rachen-Tiefe
  paint([[-400, -60], [W + 400, -60], [W + 400, 150], [-400, 150]], { wash: '#D98A95', fill: '#B85A6A', fillOp: 90, tex: .7, border: .6, ink: PAL.ink, sw: 1.2 });
  for (let i = 0; i < 7; i++) { const x = 180 + i * 260; paint(rrPts(x - 90, 110, 180, 150, 40, 2), { wash: ZAHN.col, fill: ZAHN.dk, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.1 }); }
  paint([[-400, 770 + jit(2)], [W / 2, 760 + jit(2)], [W + 400, 770 + jit(2)], [W + 400, 1500], [-400, 1500]], { wash: '#D98A95', fill: '#B85A6A', fillOp: 90, bleed: .05, tex: .8, border: .6, ink: PAL.ink, sw: 1.3 });
  if (warm > 0) paint(ellPts(960, 180, 900, 420, 26), { fill: '#FFE7A8', fillOp: 70 * warm, bleed: .3, tex: .3, ink: null });
}
// Stück-Schild: Holzschild, das an Seilen herunterfährt
function hangSign(txt, x, drop, size = 86, w = 560) {
  const y = lerp(-140, 270, backOut(drop)); if (drop <= 0) return;
  board(x, y, w, 120, txt, size, { ropes: 400, rot: Math.sin((1 - clamp(drop)) * 9) * .04, ty: 6, font: MARKER(size) });
}

// ---------- V7-Bildmittel ----------
// roter Filzstift-Ring zeichnet sich (k 0..1), leicht unrund wie handgezogen
function markRing(x, y, rx, ry, k, col = '#D8394E', sw = 3) {
  if (k <= 0) return; const pts = [], n = Math.max(2, Math.round(40 * k));
  for (let i = 0; i <= n; i++) { const a = -2.3 + i / 40 * TAU * 1.08, w = 1 + .04 * Math.sin(a * 3 + 1); pts.push([x + Math.cos(a) * rx * w, y + Math.sin(a) * ry * w]); }
  inkLine(pts, sw, col, 'ink', .5);
}
// Lupe: goldener Rand, heller Glanz, Holzgriff (wie in 03), Mittelpunkt (x, y), Radius r
function lupe(x, y, r, a = .7) {
  paint(ellPts(x, y, r, r, 30), { fill: PAL.cream, fillOp: 40, bleed: .1, tex: .2, ink: null });
  const rim = []; for (let i = 0; i <= 36; i++) { const q = i / 36 * TAU; rim.push([x + Math.cos(q) * r, y + Math.sin(q) * r]); }
  inkLine(rim, 7, GOLD, 'marker', .5); inkLine(rim, 1.6, PAL.ink, 'ink', .5);
  const hx = x + Math.cos(a) * r, hy = y + Math.sin(a) * r, ex = x + Math.cos(a) * r * 2.1, ey = y + Math.sin(a) * r * 2.1;
  inkLine([[hx, hy], [ex, ey]], 13, '#6B4A3A', 'ink', 0);
  paint(ellPts(x - r * .38, y - r * .38, r * .22, r * .12, 12, 1, -.7), { wash: PAL.cream, washOp: 200, ink: null });
}

// ================= SZENEN =================
const DAYS = ['MO', 'DI', 'MI', 'DO', 'FR', 'SA'];
// A · 0 – CUT.bc: Vorhang auf. Mia klammert sich an den Türrahmen (fertig auf „klammert“), Mama zeigt zum Schild ZAHNARZT,
// das Schild wackelt auf „Zahnarzt“. Kein Satz-Laut mehr („BLOSS NICHT!“ entfernt): Tränen + Klammern sagen es.
function shotA(t, lt) {
  const zin = ease(seg(t, K.dabei - .74, K.dabei - .19));
  const cx = lerp(930, 760, zin), cy = lerp(600, 520, zin), z = lerp(1.24 + .06 * ease(t / 3.8), 3.2, easeIn(zin));
  camBegin(cx, cy, z, 0);
  stageBack(t, { backdrop: homeSet, spots: [[700, PAL.cream]] });
  doorway(720, 800, 230, 440, { open: .85, light: 0, inside: '#4A3040', frame: '#9A6A48' });
  // Schild ZAHNARZT → mit fernem Bohrer
  const z0 = K.zahnarzt - .22, sh = t > z0 && t < z0 + .65 ? Math.sin((t - z0) * 30) * .07 * (1 - seg(t, z0, z0 + .65)) : 0;
  inkLine([[1460, 800], [1460, 590]], 2.4, WOODD, 'ink', 0);
  board(1460, 565, 330, 96, 'ZAHNARZT →', 50, { rot: -.05 + sh, font: MARKER(50) });
  drillProp(1400, 450, .42, -2.6 + Math.sin(t * 3) * .1, 1);
  // Mama (links hinter Mia? nein: rechts, zieht) – researcher ohne Kittel
  const lean = .12 + .04 * Math.sin(t * 6);
  researcher(1130, 800, 30, { coat: '#6E9F8C', shirt: PAL.cream, pants: '#4B3346', hair: '#8A4B2A', bun: true, bunCol: PAL.rose, noGlasses: true, eyes: 'dot', lookX: -1, brows: 'worried', mouth: t > K.klammert + .4 && t < K.zahnarzt - .2 ? 'o' : 'flat', rot: lean, aL: .05 + .08 * Math.sin(t * 6), aR: t > K.zahnarzt - .3 ? .55 : -1.1 });
  // Mias Arm reicht zur Mamas Hand
  const jumpK = backOut(seg(t, K.klammert - .3, K.klammert - .06));
  const kx = 800 + 18 * Math.sin(t * 21) * seg(t, K.klammert - .2, K.klammert + .2), ky = lerp(800, 690, jumpK);
  const cry = K.bloss - .2;
  child(kx, ky, 26, { rot: -.22, aL: .95 + .08 * Math.sin(t * 14), aR: .05 + .05 * Math.sin(t * 9), kick: seg(t, K.klammert - .2, K.klammert + .2), eyes: t < cry ? 'wide' : 'shut', scared: true, lookX: 1, mouth: t < cry ? 'O' : 'cry', tears: seg(t, K.bloss - .5, K.bloss - .1), noShadow: true, hairUp: 1, emote: t < K.bloss - .45 ? '!' : 'sweat', emoteK: t < K.bloss - .45 ? seg(t, K.klammert - .2, K.klammert) * (1 - seg(t, K.bloss - .65, K.bloss - .45)) : seg(t, K.bloss - .3, K.bloss - .1) });
  stageFront(t, { curtain: 1 - easeOut(seg(t, 0, .55)) });
  camEnd();
  if (zin < .5) { footlights(t); audience(t, 0); }
  if (t > CUT.bc - .22) { flushLetters(); iris(960, 540, lerp(1400, 0, ease(seg(t, CUT.bc - .22, CUT.bc)))); }
}
// B/C · CUT.bc – CUT.d: im Mund. Der Backenzahn bekommt das Zahnweh-Tuch auf „Backenzahn“, AUA! auf „weh“;
// Abreißkalender reißt auf „Tagen“, „Warten“, „macht“, „Loch“ – das Loch wächst jedes Mal; auf „größer“ roter Ring ums Loch.
function shotBC(t, lt) {
  const tears = [K.tagen - .15, K.tagen + .12, K.warten, K.macht, K.loch], idx = tears.filter(x => t >= x).length, last = tears.filter(x => t >= x).pop();
  const push = ease(seg(t, K.macht, K.groesser + .17));
  camBegin(lerp(980, 960, push), lerp(600, 610, push), 1.12 + .05 * ease(seg(t, CUT.bc, K.macht)) + .22 * push, 0);
  mouthSet(t);
  tearCal(1440, 700, 1.1, DAYS, idx, last != null ? t - last : null);
  // Nachbarzähne
  tooth(420, 800, 14, { eyes: 'look', lookX: 1, mouth: 'wobble', seed: 1, aL: -.3, aR: .6 });
  const gT = K.groesser - .15;
  const holeK = [.28, .28, .28, .45, .65, .85][idx] * (t > gT ? 1.18 : 1);
  const wT = K.weh - .15;
  const throb = t > wT ? .5 + .5 * Math.max(0, Math.sin((t - wT) * TAU / .5)) : 0;
  const md = mood(t, [[CUT.bc, 'normal'], [K.backenzahn - .2, 'scared', 'sweat'], [wT, 'x'], [K.warten - .3, 'scared', 'sweat'], [gT, 'x']]);
  const shake = t > wT ? Math.sin(t * 40) * .03 : 0;
  tooth(930, 800, 36, { ...md, mouth: t > wT ? 'O' : 'wobble', hole: holeK, throb, scarf: t > K.backenzahn - .12, rot: shake, aL: .9 + .2 * Math.sin(t * 8), aR: -.5, take: t > gT ? .1 * Math.exp(-(t - gT) * 6) * Math.cos((t - gT) * 20) : 0 });
  // Hervorhebung „größer“: roter Filzstift-Ring ums Loch (Loch sitzt bei x + 2,9u, y − 3,6u)
  const hr = (.5 + 1.1 * holeK) * 36;
  markRing(930 + 2.9 * 36, 800 - 3.6 * 36, hr + 34, hr * .8 + 30, ease(seg(t, K.groesser - .28, K.groesser)));
  camEnd();
  if (t > wT) sfx('AUA!', 700, 300, 130, '#E0283F', t - (K.weh - .2), { life: 1.1, stroke: PAL.ink, font: MARKER(130) });
  if (t < CUT.bc + .18) { flushLetters(); iris(960, 700, lerp(0, 1400, ease(seg(t, CUT.bc, CUT.bc + .18)))); }
  if (t > CUT.d - .33) { flushLetters(); iris(960, 600, lerp(1400, 0, ease(seg(t, CUT.d - .33, CUT.d)))); }
}
// D · CUT.d – CUT.ef: dunkle Bühne. Angst-Thermometer schießt auf „Angst“ hoch und glüht; Mia wächst auf „Leben“ (Jugendliche)
// und „lang“ (Erwachsene) – jede im eigenen Scheinwerfer, das Thermometer bleibt oben. Kein Satz („EIN LEBEN LANG“ entfernt).
function shotD(t, lt) {
  const pan = ease(seg(t, K.bleibt, K.bei - .59));
  camBegin(lerp(960, 1090, pan), 590, 1.16 + .03 * pan, 0);
  stageBack(t, { backdrop: () => { paint(rectPts(-400, -400, W + 800, 1240), { wash: '#1F2550', washOp: 255, fill: '#141A3A', fillOp: 150, bleed: .08, tex: .8, border: .3, ink: null }); }, floor: '#5A3F33' });
  // Bohrer-Schatten auf der Rückwand
  const sg = ease(seg(t, K.angst0 - .14, K.bei - .59));
  if (sg > .01) { push(); translate(1250, 470); rotate(-2.5); scale(.7 + 1.6 * sg); paint([[-20, -16], [200, -24], [220, 0], [200, 24], [-20, 16], [-90, 20], [-90, -20]], { wash: '#0E1026', washOp: 200, ink: null, curv: .2 }); pop(); }
  const spots = [[860, CUT.d + .02], [1150, K.leben], [1440, K.lang]];
  for (const [sx, s0] of spots) { const k = seg(t, s0 - .25, s0); if (k > 0) paint([[sx - 80, -60], [sx + 80, -60], [sx + 240 * k, 860], [sx - 240 * k, 860]], { fill: PAL.cream, fillOp: 55 * k, bleed: .05, tex: .2, border: .1, ink: null }); if (k > 0) paint(ellPts(sx, 860, 250 * k, 50 * k, 24), { fill: PAL.cream, fillOp: 90 * k, bleed: .1, tex: .2, ink: null }); }
  // Angst-Thermometer
  const v = lerp(18, 88, easeOut(seg(t, K.angst - .3, K.angst))) + 8 * ease(seg(t, K.leben - .2, K.lang + .2));
  meterProp(600, 860, .95, v, { label: 'ANGST', glow: seg(t, K.angst - .3, K.angst) });
  // Mia – als Kind, als Jugendliche, als Erwachsene: immer dieselbe Angst
  const shiver = Math.sin(t * 38) * 4;
  child(860 + shiver, 860, 28, { eyes: 'wide', scared: true, mouth: 'wobble', aL: -.55, aR: -.55, tears: .6, emote: 'sweat', emoteK: seg(t, CUT.d + .22, CUT.d + .47) });
  const k2 = backOut(seg(t, K.leben - .25, K.leben)), k3 = backOut(seg(t, K.lang - .25, K.lang));
  if (k2 > .01) { push(); translate(1150, 860); scale(1, k2); translate(-1150, -860); researcher(1150 + shiver, 860, 28, { coat: KID.shirt, shirt: PAL.cream, pants: KID.pants, hair: KID.hair, noGlasses: true, eyes: 'wide', brows: 'worried', mouth: 'wobble', aL: -.6, aR: -.6, emote: 'sweat', emoteK: seg(t, K.leben + .05, K.leben + .25) }); pop(); }
  if (k3 > .01) { push(); translate(1440, 860); scale(1, k3); translate(-1440, -860); researcher(1440 + shiver, 860, 33, { coat: '#5B6C8C', shirt: PAL.cream, pants: '#3A3552', hair: KID.hair, bun: true, bunCol: KID.ribbon, noGlasses: true, eyes: 'wide', brows: 'worried', mouth: 'wobble', aL: -.6, aR: -.6, emote: 'sweat', emoteK: seg(t, K.lang + .1, K.lang + .3),
    handR: (s, sw) => paint(rrPts(-.5 * s, .2 * s, 2.4 * s, 1.8 * s, .3 * s), { wash: '#6B4A3A', ink: PAL.ink, sw: sw * .6 }) }); pop(); }
  camEnd();
  if (t < CUT.d + .22) { flushLetters(); iris(800, 700, lerp(0, 1500, ease(seg(t, CUT.d, CUT.d + .22)))); }
  if (t > K.bei - .64) { flushLetters(); wipe(seg(t, K.bei - .64, K.bei - .04), 0); }
}
// E/F/H · 12,45 – 17,2 und 19,9 – 22,0: warme Sonnenstrahl-Bühne. Die Zahnfee kommt aus der Falltür, die Angst fällt;
// erster Besuch = Spielen auf dem Stuhl; 20 Minuten auf der Uhr, Konfetti.
const HX = 980, HY = 900;
// V7: Schild ZAHNFEE landet auf „Zahnfee“, das Angst-Thermometer fällt auf „anders“ (Zauberstrahl davor);
// Stuhl fährt vor „Beim ersten Besuch“ ein, auf „gespielt“ Luftballons + Herz. „HUIII!“/„NUR SPIELEN“ entfernt.
function shotEF(t, lt) {
  const toF = ease(seg(t, K.besuch0 - .42, K.besuch0 + .08)), inF = ease(seg(t, K.loecher0 - .66, K.loecher0 - .16));
  camBegin(lerp(960, 1030, toF) + lerp(0, 60, inF), lerp(620, 600, toF) + lerp(0, -60, inF), lerp(1.18, 1.24, toF) * lerp(1, 2.6, easeIn(inF)), 0);
  stageBack(t, { backdrop: warmSet, spots: [[HX, PAL.cream]] });
  hangSign('ZAHNFEE', 960, seg(t, K.zahnfee - .34, K.zahnfee));
  // Stuhl kommt im Übergang zu F von rechts
  const chairX = lerp(2300, 1180, easeOut(seg(t, K.besuch0 - .47, K.besuch0 + .13)));
  const G0 = K.gespielt;
  const lift = kf(t, [[G0 - .6, 0], [G0 - .3, 1], [G0 - .1, .5], [G0 + .1, 1.1]], easeOut);
  let seat = null;
  if (chairX < 2250) seat = dentChair(chairX, 900, 1, lift, { lamp: seg(t, G0 - .43, G0 - .35) });
  // Falltür
  const open = easeOut(seg(t, K.bei - .49, K.bei - .34)) * (1 - easeOut(seg(t, K.zahnfee - .06, K.zahnfee + .24)));
  trapHole(HX, HY, open);
  const rise = seg(t, K.bei - .37, K.bei - .07);
  const fx = lerp(HX, 700, ease(seg(t, K.besuch0 - .42, K.besuch0 + .08)));
  if (rise > 0) {
    const y = lerp(HY + 420, HY, backOut(rise)), m = move('idle', t);
    const wave = t > K.zahnfee + .24 && t < K.anders + .23 ? Math.sin((t - K.zahnfee - .24) * 14) : 0;
    wings(fx, y, 33, Math.sin(t * 12));
    researcher(fx, y, 33, { coat: COAT, shirt: PAL.teal, pants: '#3A9C98', hair: '#5A3A2A', bun: true, bunCol: PAL.ochre, eyes: 'dot', mouth: 'grin', blush: true, noShadow: rise < 1, dy: rise < 1 ? 0 : m.dy * .4,
      aL: t > K.besuch0 + .18 ? .3 : .2, aR: lerp(.4, 1.3, seg(t, K.anders - .62, K.anders - .42)) + .25 * wave, handR: wandHand(seg(t, K.anders - .57, K.anders - .27)), emote: t > K.bei && t < K.anders - .17 ? 'spark' : undefined, emoteK: seg(t, K.bei, K.bei + .2) });
  }
  trapLip(HX, HY, open);
  if (rise > 0) burstConfetti(HX, HY - 120, t - (K.bei - .19), 20, 900);
  // Zauberstrahl zum Angst-Thermometer, das auf „anders“ fällt
  const zap = seg(t, K.anders - .52, K.anders - .26);
  if (zap > 0 && t < K.anders + .33) { const p = []; for (let k = 0; k <= 8; k++) p.push([lerp(fx + 80, 520, k / 8 * zap), lerp(420, 520, k / 8 * zap) + Math.sin(k * 2 + t * 30) * 18]); inkLine(p, 3, PAL.ochre, 'marker', .5); for (let k = 0; k < 5; k++) paint(starPts(lerp(fx + 80, 520, hash(k) * zap), lerp(420, 520, hash(k)) + jit(20), 12 + hash(k + 3) * 10), { wash: PAL.cream, fill: PAL.ochre, fillOp: 70, ink: null }); }
  const mx = lerp(520, -260, ease(seg(t, K.besuch0 - .47, K.besuch0 - .02)));
  if (mx > -250) meterProp(mx, 900, .95, lerp(96, 6, easeOut(seg(t, K.anders - .28, K.anders + .02))), { label: 'ANGST' });
  // Mia: lugt von rechts herein (E), sitzt dann auf dem Stuhl (F)
  if (!seat || chairX > 1700) {
    const kx = lerp(2050, 1640, easeOut(seg(t, K.anders - .1, K.anders + .3))), st = K.anders + .3;
    child(kx, 900, 26, { eyes: t < st ? 'wide' : 'star', mouth: t < st ? 'o' : 'grin', lookX: -1, aL: .2, aR: -.9, emote: t > st ? '!' : undefined, emoteK: seg(t, st, st + .2) });
  } else {
    const bounce = Math.abs(Math.sin(bpOf(t) * Math.PI)) * .25;
    child(seat.sx, seat.sy + 6, 24, { eyes: t > K.besuch - .2 ? 'closed' : 'star', mouth: t > K.loecher0 - .56 ? 'O' : 'grin', aL: .9 + .3 * Math.sin(t * 9), aR: 1.0, dy: -bounce, noShadow: true, handR: mirrorHand, emote: t > G0 - .25 ? 'heart' : undefined, emoteK: seg(t, G0 - .25, G0) * (1 - seg(t, K.loecher0 - .66, K.loecher0 - .46)) });
    // Hervorhebung „gespielt“: Luftballons steigen auf, fertig auf dem Wort
    const bl = backOut(seg(t, G0 - .3, G0));
    for (let i = 0; i < 3; i++) if (bl > .02) balloon(chairX + 150 + i * 70, lerp(760, 360 - lift * 90 - i * 30, bl), 46 * clamp(bl, .3, 1.2), [PAL.rose, PAL.sky, PAL.ochre][i], t, i);
  }
  camEnd();
  if (t < K.bei - .04) { flushLetters(); wipe(seg(t, K.bei - .64, K.bei - .04), 0); }
  if (t > CUT.g - .29) { flushLetters(); iris(960, 540, lerp(1400, 0, ease(seg(t, CUT.g - .29, CUT.g - .04)))); }
}
// G · 17,34 – 20,2: im Mund, warmes Lampenlicht. Der Bohrer kommt – rotes X – die Zahnfee tupft das Loch zu.
// V7: Lupe fährt auf „Löcher“ aufs kleine Loch; Bohrer kommt auf „behandeln“, rotes X fertig auf „ohne“,
// Bohrer fliegt auf „Bohren“ raus, Pinsel tupft das Loch zu. „OHNE BOHREN!“ entfernt – das X ist die Aussage.
function shotG(t, lt) {
  camBegin(960, 560, 1.06 + .03 * ease(seg(t, CUT.g, K.nach - .18)), 0);
  mouthSet(t, 1);
  const dIn = easeOut(seg(t, K.behandeln - .45, K.behandeln - .1)), dOut = ease(seg(t, K.bohren + .05, K.bohren + .45));
  const scared = t > K.behandeln - .3 && t < K.bohren - .05;
  const md = mood(t, [[CUT.g, 'normal'], [K.behandeln - .3, 'scared', 'sweat'], [K.bohren - .05, 'happy', 'spark']]);
  const fill = ease(seg(t, K.bohren + .05, K.bohren + .3));
  tooth(900, 830, 37, { ...md, lookX: 1, mouth: scared ? 'wobble' : 'smile', hole: .45, filled: fill, blush: t > K.bohren + .2, sq: scared ? .04 * Math.sin(t * 40) : 0, aL: scared ? 1.2 : .4, aR: scared ? 1.1 : .9 });
  // Hervorhebung „Löcher“: Lupe gleitet von links aufs kleine Loch (Loch bei x + 2,9u, y − 3,6u), geht, wenn der Bohrer kommt
  const lu = ease(seg(t, K.loecher - .3, K.loecher)) * (1 - ease(seg(t, K.behandeln - .3, K.behandeln)));
  if (lu > .01) lupe(lerp(300, 900 + 2.9 * 37, lu), lerp(420, 830 - 3.6 * 37, lu), 95, .75);
  if (dIn > 0 && dOut < 1) drillProp(lerp(1900, 1260, dIn) + dOut * 700, 470 + dOut * -200, 1, -.35, t > K.behandeln - .1 && t < K.ohne ? 1 : 0);
  // rotes X (zwei Filzstiftstriche), fertig auf „ohne“
  const x1 = seg(t, K.ohne - .32, K.ohne - .16), x2 = seg(t, K.ohne - .16, K.ohne), dx = lerp(1260, 1960, dOut), dyy = 470 - 200 * dOut;
  // V7: deckender roter Strich (vorher durchscheinender Marker, kaum lesbar)
  if (x1 > 0) inkLine([[dx - 150, dyy - 150], [dx - 150 + 330 * x1, dyy - 150 + 300 * x1]], 3.2, '#D8394E', 'ink', 0);
  if (x2 > 0) inkLine([[dx + 180, dyy - 150], [dx + 180 - 330 * x2, dyy - 150 + 300 * x2]], 3.2, '#D8394E', 'ink', 0);
  // Pinsel der Zahnfee tupft
  const bp = seg(t, K.bohren - .2, K.bohren + .05) * (1 - seg(t, K.bohren + .45, K.bohren + .7));
  if (bp > 0) { const bx = lerp(-200, 1010, easeOut(bp)), by = lerp(900, 700, easeOut(bp)) + Math.sin(t * 30) * 6 * seg(t, K.bohren + .05, K.bohren + .3);
    inkLine([[bx - 520, by + 260], [bx, by]], 9, '#6B4A3A', 'ink', 0); paint(ellPts(bx + 10, by - 6, 26, 16, 12, 1, -.5), { wash: PAL.cream, fill: PAL.sky, fillOp: 60, ink: PAL.ink, sw: .8 }); }
  if (t > K.bohren + .3) for (let i = 0; i < 6; i++) { const a = t - K.bohren - .3 - i * .06; if (a > 0 && a < .8) paint(starPts(990 + Math.cos(i * 1.1) * 140 * easeOut(a / .8), 700 + Math.sin(i * 1.1) * 110 * easeOut(a / .8), 22 * (1 - a / .8) + 6), { wash: PAL.cream, fill: PAL.ochre, fillOp: 70, ink: PAL.ink, sw: .5 }); }
  camEnd();
  if (t < K.loecher0) { flushLetters(); iris(960, 540, lerp(0, 1400, ease(seg(t, CUT.g, K.loecher0)))); }
  if (t > CUT.h - .3) { flushLetters(); wipe(seg(t, CUT.h - .3, CUT.h + .3), 2); }
}
// H · 19,9 – 22,0: 20 Minuten auf der Wanduhr, dann Konfetti – vorbei.
// V7: Uhrzeiger laufen auf 20, Etikett „20 MIN“ an der Uhr fertig auf „zwanzig“; Sprung + Konfetti auf „vorbei“.
function shotH(t, lt) {
  camBegin(1000, 600, 1.16 + .04 * ease(seg(t, CUT.h, CUT.i)), 0);
  stageBack(t, { backdrop: warmSet, spots: [[1300, PAL.cream]] });
  const mins = 20 * easeOut(seg(t, K.nach - .05, K.minuten));
  wallClock(760, 430, 190, mins);
  letter('20 MIN', 760, 720, 90, PAL.cream, { font: MARKER(90), stroke: PAL.ink, pop: seg(t, K.n20 - .3, K.n20) * 1.5 });
  const seat = dentChair(1180, 900, .9, 0, { lamp: 1 });
  const vT = K.vorbei - .3, jmp = jump(t, vT, K.vorbei + .08, 3);
  if (t < vT) child(seat.sx, seat.sy + 6, 22, { eyes: 'dot', mouth: 'smile', lookX: -1, aL: .3, aR: .2, noShadow: true, dy: -Math.abs(Math.sin(bpOf(t) * Math.PI)) * .2 });
  else child(lerp(seat.sx, 960, seg(t, vT, K.vorbei + .08)), lerp(seat.sy + 6, 900, seg(t, vT, K.vorbei + .08)), 22, { ...jmp, eyes: 'closed', mouth: 'grin', aL: 1.3, aR: 1.3, emote: 'spark', emoteK: seg(t, vT, K.vorbei - .1) });
  wings(1500, 900, 28, Math.sin(t * 12));
  researcher(1500, 900, 28, { coat: COAT, shirt: PAL.teal, pants: '#3A9C98', hair: '#5A3A2A', bun: true, bunCol: PAL.ochre, eyes: t > vT ? 'closed' : 'dot', mouth: 'grin', blush: true, flip: true, aL: t > vT ? 1.2 : .2, aR: t > vT ? 1.2 : .4, handR: wandHand(0) });
  burstConfetti(960, 600, t - (K.vorbei - .1), 26, 1000);
  camEnd();
  confettiRain(t, K.vorbei - .05, 30);
  if (t < CUT.h + .35) { flushLetters(); wipe(seg(t, CUT.h - .3, CUT.h + .3), 2); }
}
// I · 22,0 – 24,3: Spiegel des Anfangs – jetzt zieht Mia die Mama zur Zahnfee-Tür und will nicht mehr weg.
// V7: „NOCHMAL!“ entfernt. Spiegel des Anfangs: auf „wiederkommen“ springt Mia an die Zahnfee-Tür und klammert sich fest, Herzen.
function shotI(t, lt) {
  camBegin(lerp(1000, 1040, ease(seg(t, CUT.i, CUT.j))), 600, 1.2, 0);
  stageBack(t, { backdrop: warmSet, spots: [[1300, PAL.cream]] });
  doorway(1300, 900, 240, 460, { open: .7, light: 1, inside: '#F6D6A0', leaf: '#6FB3AE', frame: '#E8B23A' });
  board(1300, 380, 300, 80, 'ZAHNFEE', 50, { col: PAL.teal, font: MARKER(50) });
  const wE = K.wieder - .25, walk = seg(t, CUT.i, wE), kx = lerp(900, 1180, ease(walk)), mx = lerp(560, 800, ease(walk));
  researcher(mx, 900, 30, { coat: '#6E9F8C', shirt: PAL.cream, pants: '#4B3346', hair: '#8A4B2A', bun: true, bunCol: PAL.rose, noGlasses: true, eyes: 'dot', mouth: t > K.kind2 ? 'smile' : 'o', lookX: 1, rot: -.14, walk: walk < 1 ? t * 1.6 : undefined, aR: .1, aL: -1.1, emote: t > K.wieder - .1 ? 'heart' : undefined, emoteK: seg(t, K.wieder - .1, K.wieder + .1) });
  child(kx, walk < 1 ? 900 : lerp(900, 800, backOut(seg(t, wE, K.wieder - .05))), 25, { rot: walk < 1 ? .15 : .22, walk: walk < 1 ? t * 2.2 : undefined, eyes: 'heart', mouth: 'grin', aL: walk < 1 ? .05 : .95, aR: .95, kick: walk < 1 ? 0 : .6 * seg(t, wE, K.wieder + .05), noShadow: walk >= 1, flip: false });
  wings(1500, 900, 26, Math.sin(t * 12));
  researcher(1500, 900, 26, { coat: COAT, shirt: PAL.teal, pants: '#3A9C98', hair: '#5A3A2A', bun: true, bunCol: PAL.ochre, eyes: 'closed', mouth: 'grin', blush: true, flip: true, aR: 1.1 + .3 * Math.sin(t * 12), handR: wandHand(0) });
  for (let k = 0; k < 6; k++) { const a = t - (CUT.i + .2 + k * .4); if (a > 0 && a < 1.4) paint(heartPts(kx + 30 + Math.sin(a * 5 + k) * 40, 560 - a * 260, 26 * backOut(a * 3)), { wash: '#E2476E', fill: PAL.rose, fillOp: 90, ink: PAL.ink, sw: .6 }); }
  // Hervorhebung „wiederkommen“: Tür-Rahmen leuchtet auf
  const dg = seg(t, K.wieder - .25, K.wieder);
  if (dg > 0) paint(ellPts(1300, 700, 230 * dg + 60, 300 * dg + 60, 26), { fill: '#FFE7A8', fillOp: 60 * dg, bleed: .3, tex: .2, ink: null });
  camEnd();
}
// J · 24,3 – Ende: Der Vorhang fällt. ZAHNFEE auf dem Vorhang, Schild „Kinderzahnarzt“, erster Besuch kostenlos.
// V7: Schlusskarte: ZAHNFEE (Name, auf „Zahnfee“), Schild Kinderzahnarzt (auf „Kinderzahnarzt“), Angebot in 2 Teilen:
// „1. Besuch“ auf „Besuch“, grüne Plakette „kostenlos“ auf „kostenlos“, dann Kontakt. Kein Satz („Der erste Besuch / ist kostenlos!“ ersetzt).
function shotJ(t, lt) {
  const a = seg(t, CUT.j, CUT.j + .36), land = t - (CUT.j + .36);
  let hemY = lerp(-80, 1010, easeIn(a)); if (land > 0) hemY = 1010 - Math.abs(Math.sin(land * 9)) * 26 * Math.exp(-land * 6);
  const [sx, sy] = land > 0 ? shakeXY(t, 14 * Math.exp(-land * 7)) : [0, 0];
  camBegin(960 + sx, 600 + sy, 1.06 + .04 * ease(seg(t, K.schluss - .09, DUR)), 0);
  stageBack(t, { backdrop: warmSet, spots: [[1300, PAL.cream]] });
  if (hemY < 1000) {
    doorway(1450, 900, 240, 460, { open: .7, light: 1, inside: '#F6D6A0', leaf: '#6FB3AE', frame: '#E8B23A' });
    child(1330, 800, 25, { rot: .22, eyes: 'heart', mouth: 'grin', aL: .95, aR: .95, noShadow: true });
    researcher(900, 900, 30, { coat: '#6E9F8C', shirt: PAL.cream, pants: '#4B3346', hair: '#8A4B2A', bun: true, bunCol: PAL.rose, noGlasses: true, eyes: 'closed', mouth: 'smile', rot: -.1 });
  }
  const pk = ease(seg(t, K.kostenlos + .2, K.kostenlos + .5)) * (1 - ease(seg(t, DUR - .9, DUR - .6))), split = 130 * pk;
  if (pk > .01) {
    paint([[960 - split * .3, 850], [960 + split * .3, 850], [960 + split * 1.1, 1012], [960 - split * 1.1, 1012]], { wash: '#2A1A22', ink: null });
    const wv = Math.sin((t - K.kostenlos - .3) * 16);
    tooth(960 - 20 + 60 * pk, 1010, 12, { rot: .2 * pk, eyes: t > K.kostenlos + 1 && t < K.kostenlos + 1.25 ? 'wink' : 'happy', mouth: 'grin', blush: true, noShadow: true, aL: -.2, aR: 1.1 + .45 * wv, filled: 1, hole: .45 });
  }
  houseCurtain(t, hemY, split, 850, 1010);
  if (land > -0.2) {
    letter('ZAHNFEE', 960, 250, 230, PAL.cream, { pop: seg(t, K.schluss - .29, K.schluss) * 1.5, rot: -.03 + Math.sin(bpOf(t) * Math.PI) * .012, stroke: CURTAIN_DK, font: MARKER(230) });
    board(960, lerp(-120, 440, backOut(seg(t, K.kza - .29, K.kza))), 640, 110, 'Kinderzahnarzt', 70, { ropes: 500, rot: Math.sin(clamp(1 - seg(t, K.kza, K.kza + .7)) * 10) * .03 * (t > K.kza ? 1 : 0), ty: 4, font: MARKER(70) });
    letter('1. Besuch', 960, 592, 76, GOLD, { pop: seg(t, K.kennen - .3, K.kennen) * 1.5, font: HAND(76) });
    const kb = seg(t, K.kostenlos - .3, K.kostenlos);
    if (kb > 0) { push(); translate(960, 705); scale(backOut(kb)); rotate(-.03); paint(rrPts(-240, -62, 480, 124, 50, 3), { wash: PAL.sap, fill: '#3E7A3A', fillOp: 70, tex: .6, ink: PAL.ink, sw: 1.4 }); pop(); }
    letter('kostenlos', 960, 705, 88, PAL.cream, { pop: seg(t, K.kostenlos - .3, K.kostenlos) * 1.5, rot: -.03, font: MARKER(88) });
    letter('zahnfee-kinderzahnarzt.de  ·  06221 55 44 33', 960, 810, 40, PAL.cream, { pop: seg(t, K.kostenlos + .3, K.kostenlos + .6) * 1.5, font: HAND(40), ink: false });
  }
  camEnd();
  footlights(t); stageFront(t, {}); audience(t, .8 * seg(t, K.schluss - .09, K.schluss + .21) * (1 - seg(t, K.kostenlos + .5, DUR - .6)));
  flushLetters();
  flash(ease(seg(t, DUR - .55, DUR)), PAL.paper);
}

// Pinsel-Wischblende (wie die Kapitelwechsel im Original)
const WIPE_COLS = [[PAL.indigo, PAL.violet], [PAL.clayDk, PAL.clay], [PAL.teal, PAL.sap], [PAL.violet, PAL.rose]];
function wipe(p, idx) {
  if (p <= 0 || p >= 1) return;
  const [c1, c2] = WIPE_COLS[idx % WIPE_COLS.length], n = 5, bh = (H + 420) / n + 40;
  push(); translate(W / 2, H / 2); rotate(-.1); translate(-W / 2, -H / 2);
  for (let i = 0; i < n; i++) {
    const y0 = -230 + i * (H + 420) / n, d = [0, .14, .06, .18, .1][i];
    const q = p < .5 ? easeOut(clamp((p * 2 - d) / (1 - d))) : ease(clamp(((p - .5) * 2 - d) / (1 - d)));
    const x0 = p < .5 ? -300 : lerp(-300, W + 400, q), x1 = p < .5 ? lerp(-300, W + 400, q) : W + 400;
    if (x1 - x0 < 30) continue;
    const pts = [], rag = (k, side) => side * (40 + 50 * hash(i * 31 + k)) + jit(12);
    for (let k = 0; k <= 8; k++) pts.push([lerp(x0, x1, k / 8), y0 + Math.sin(k * .9 + i) * 14 + jit(5)]);
    for (let k = 1; k < 9; k++) pts.push([x1 + rag(k, 1) - 40, y0 + bh * k / 9]);
    for (let k = 8; k >= 0; k--) pts.push([lerp(x0, x1, k / 8), y0 + bh + Math.sin(k * .8 + i * 2) * 14 + jit(5)]);
    if (p >= .5) for (let k = 8; k > 0; k--) pts.push([x0 - rag(k + 20, 1) + 40, y0 + bh * k / 9]);
    paint(pts, { wash: i % 2 ? c1 : c2, washOp: 255, fill: i % 2 ? c2 : c1, fillOp: 70, bleed: .05, tex: .8, border: .6, ink: null,
      hatch: { d: 44, a: 0, o: { rand: .6, gradient: .5 }, b: 'charcoal', c: i % 2 ? c2 : PAL.cream, w: .8 } });
  }
  pop();
}

const SHOTS = [[0, shotA], [CUT.bc, shotBC], [CUT.d, shotD], [CUT.ef, shotEF], [CUT.g, shotG], [CUT.h, shotH], [CUT.i, shotI], [CUT.j, shotJ]];
function drawWorld(t) {
  let i = 0; while (i + 1 < SHOTS.length && t >= SHOTS[i + 1][0]) i++;
  const t0 = SHOTS[i][0], end = i + 1 < SHOTS.length ? SHOTS[i + 1][0] : DUR;
  SHOTS[i][1](t, t - t0, end - t0); CAM = null;
  flushLetters();
}
// Sprung (aus dem ClaudeAnimationBase-Kern): Ausholen, Strecken, Landen mit Stauchen
function jump(t, t0, t1, h = 3) {
  if (t < t0 - .12) return { dy: 0, sq: 0 };
  if (t < t0) return { dy: 0, sq: .18 * ease(seg(t, t0 - .12, t0)) };
  if (t < t1) { const k = (t - t0) / (t1 - t0); return { dy: -h * 4 * k * (1 - k), sq: -.16 * Math.abs(1 - 2 * k) }; }
  const a = t - t1; return { dy: 0, sq: .22 * Math.exp(-8 * a) * Math.cos(20 * a) };
}
