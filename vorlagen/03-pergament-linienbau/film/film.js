// Bauhütte Architekten – V7 im Stil von „Western Civilization in Motion“ (vittorio).
// V7: keine Sätze, keine Überschriften. Betonung über Bildmittel (Lupe, Kreis, Rotfärbung, Lichtkegel, Zoom).
// Großer Text nur als Einzelwort/Zahl am Objekt: SCHIMMEL (Etikett an der Lupe), 100 JAHRE (unter dem Haus), Schlusskarte.
// Alle Zeiten aus K (werkzeuge/wortzeiten.py -> out/vo.json -> zeiten.py), Szenenwechsel in K.cut.
const C = K.cut;

// ---------- A: Fleck an der Wand – er wächst ----------
function sceneStain(t) {
  DARK = 0; parchment(t, 960, 540);
  // weit (Altbau erkennbar) -> auf „wächst“ nah an die Wand -> in den Fleck hinein (Übergang)
  const wide = eio(lin(t, K.altbau - .55, K.altbau - .05)), near = eio(lin(t, K.und - .3, K.waechst - .05)), dive = eio(lin(t, C.b - .17, C.b));
  const d0 = mix(mix(10.5, 10, lin(t, 0, K.altbau)), mix(18.5, 19, lin(t, K.altbau, K.und)), wide);
  const dist = mix(mix(d0, 7.2, near), 2.4, dive);
  const tx = mix(mix(-2.3, -.6, wide), STAIN[0] + .2, near), ty = mix(mix(2.6, 4.9, wide), STAIN[1] + .15, near);
  camLook(tx, ty, 0, dist, mix(mix(-.3, -.42, wide), -.12, near), 0, 1400, 960, 560);
  groundLine();
  const grow = eo(lin(t, K.waechst - .22, C.b - .1));
  house3(t, { stain: mix(.5, 1.45, grow), mold: 0 });
  // Wasserränder laufen beim Wachsen nach außen
  const c = prj(fp(STAIN[0], STAIN[1]));
  if (grow > 0 && grow < 1) for (let i = 0; i < 3; i++) ringPulse(c[0], c[1], t, K.waechst - .22 + i * .15, 60, 420, 'rgba(70,58,32,.9)', .55, 2);
  // Markierung auf „Fleck“: roter gestrichelter Kreis (Geste statt Wort)
  const mk = lin(t, K.fleck - .3, K.fleck) * (1 - lin(t, K.und - .1, K.und + .15));
  if (mk > 0) { const r = (.5 * 1.5) * CAM.f / c[2] + 26; X.save(); X.globalAlpha = mk; X.strokeStyle = P.red; X.lineWidth = 3; X.setLineDash([10, 8]); X.lineDashOffset = -t * 20;
    X.beginPath(); X.arc(c[0], c[1], r * mix(1.25, 1, eo(mk)), 0, 7); X.stroke(); X.restore(); }
  finish(t);
}

// ---------- B: Die Wand teilt sich – nasser Balken, Schimmel ----------
function sectionDraw(t) {
  X.save(); const s = mix(.9, .96, lin(t, C.b, C.c)); X.translate(1010, 600); X.scale(s, s); X.translate(-1220, -560);
  const wall = new Path2D(); wall.rect(420, 60, 1800, 1020); X.fillStyle = '#c9b391'; X.fill(wall);
  X.save(); X.clip(wall); X.strokeStyle = P.ink; X.lineWidth = 1.6; for (let r = 0; r < 23; r++) { const y = 60 + r * 48; X.beginPath(); X.moveTo(420, y); X.lineTo(2220, y); X.stroke(); for (let c = 0; c < 16; c++) { const x = 420 + c * 120 + (r % 2) * 60; X.beginPath(); X.moveTo(x, y); X.lineTo(x, y + 48); X.stroke(); } }
  X.globalAlpha = .45; X.fillStyle = hatchPat(P.ink2, 7, 1, 1); X.fillRect(420, 60, 1800, 1020); X.restore();
  // Balkenkopf im Schnitt
  const bx = 1220, by = 560, bw = 460, bh = 420, beam = new Path2D(); beam.rect(bx - bw / 2, by - bh / 2, bw, bh);
  X.fillStyle = '#c69a62'; X.fill(beam); X.save(); X.clip(beam);
  X.strokeStyle = P.woodD; X.lineWidth = 1.8; for (let r = 12; r < 380; r += 14 + (r % 3) * 3) { X.beginPath(); for (let i = 0; i <= 60; i++) { const a = i / 60 * Math.PI * 2, rr = r * (1 + .05 * Math.sin(a * 3 + r)); X.lineTo(bx - 60 + Math.cos(a) * rr, by + 30 + Math.sin(a) * rr * .92); } X.stroke(); }
  X.strokeStyle = P.ink; X.lineWidth = 3; X.beginPath(); X.moveTo(bx - 60, by + 30); X.lineTo(bx + 60, by - 70); X.lineTo(bx + 150, by - 110); X.moveTo(bx - 60, by + 30); X.lineTo(bx - 170, by + 120); X.stroke();
  // Nässe zieht auf „Balken“ von oben ein: dunkler, bläulicher Keil
  const wet = eo(lin(t, K.balken - .5, K.balken + .1));
  if (wet > 0) { const g = X.createLinearGradient(0, by - bh / 2, 0, by + bh / 2); g.addColorStop(0, hexA('#2f4a60', .8 * wet)); g.addColorStop(1, hexA('#3d566b', .25 * wet)); X.fillStyle = g; X.fillRect(bx - bw / 2, by - bh / 2, bw, bh * mix(.15, 1, wet)); }
  // Nässe glänzt: wandernde Glanzlichter
  if (wet > .3) { X.save(); X.globalAlpha = (wet - .3) / .7; X.strokeStyle = 'rgba(245,250,255,.85)'; X.lineCap = 'round';
    for (let i = 0; i < 7; i++) { const gx = bx - bw / 2 + 50 + i * 60 + Math.sin(t * 1.3 + i) * 8, gy = by - bh / 2 + 40 + hash(i * 3.1) * 260 * wet, sh = .5 + .5 * Math.sin(t * 5 + i * 1.7);
      X.lineWidth = 3 + 3 * sh; X.globalAlpha = ((wet - .3) / .7) * (.35 + .6 * sh); X.beginPath(); X.moveTo(gx, gy); X.quadraticCurveTo(gx + 14, gy + 20, gx + 8, gy + 48); X.stroke();
      X.beginPath(); X.arc(gx + 22, gy + 8, 3 + 2 * sh, 0, 7); X.fillStyle = 'rgba(250,252,255,.9)'; X.fill(); }
    X.restore(); }
  X.restore(); X.lineWidth = 3.6; X.strokeStyle = P.ink; X.stroke(beam);
  // Putzschicht mit Riss
  const pl = new Path2D(); pl.moveTo(330, 60); pl.lineTo(420, 60); pl.lineTo(420, 1080); pl.lineTo(330, 1080); pl.closePath(); X.fillStyle = P.plaster; X.fill(pl); hatchPath(pl, P.ink2, 5, 1, .4, -1); X.lineWidth = 2.6; X.stroke(pl);
  const crackP = new Path2D(); crackP.moveTo(330, 470); crackP.lineTo(370, 520); crackP.lineTo(340, 580); crackP.lineTo(385, 640); X.strokeStyle = P.red; X.lineWidth = 3; X.stroke(crackP);
  // Wasser läuft durch die Fuge, Tropfen fallen
  X.save(); X.globalAlpha = lin(t, K.dahinter - .1, K.dahinter + .3); X.strokeStyle = P.water; X.lineWidth = 7; X.lineCap = 'round'; X.beginPath(); X.moveTo(1380, 60); X.bezierCurveTo(1370, 200, 1400, 280, 1390, by - bh / 2); X.stroke(); X.restore();
  for (let i = 0; i < 6; i++) { if (t < K.dahinter - .1) continue; const ph = ((t * .9 + i / 6) % 1); const x = 1060 + i * 60, y = mix(by - bh / 2 + 20, by + bh / 2 + 160, ph * ph); X.save(); X.globalAlpha = 1 - lin(ph, .8, 1); X.fillStyle = hexA(P.water, .85); X.beginPath(); X.moveTo(x, y - 18); X.quadraticCurveTo(x + 10, y, x, y + 8); X.quadraticCurveTo(x - 10, y, x, y - 18); X.fill(); X.strokeStyle = P.ink; X.lineWidth = 1.6; X.stroke(); X.restore(); }
  // Schimmel breitet sich auf „Schimmel“ aus: Kolonien wachsen vom nassen Balken aus über Holz und Fugen
  const mk = eo(lin(t, K.schimmel - .45, K.schimmel + .45));
  if (mk > 0) { const cols = [[bx - 120, by - 120], [bx + 90, by - 60], [bx - 40, by + 110], [bx + 170, by + 150], [bx - 200, by + 40], [bx + 260, by - 170], [bx - 300, by - 180], [bx + 40, by - 190]];
    cols.forEach(([cx, cy], j) => { const R = (60 + hash(j * 9) * 70) * clamp(mk * 1.5 - j * .07); if (R <= 0) return;
      const g = X.createRadialGradient(cx, cy, 0, cx, cy, R * 1.2); g.addColorStop(0, 'rgba(34,44,28,.55)'); g.addColorStop(1, 'rgba(34,44,28,0)'); X.fillStyle = g; X.beginPath(); X.arc(cx, cy, R * 1.2, 0, 7); X.fill();
      for (let i = 0; i < 46; i++) { const a = hash(j * 100 + i * 2.3) * 6.28, r = Math.sqrt(hash(j * 50 + i * 4.1)) * R; const x = cx + Math.cos(a) * r, y = cy + Math.sin(a) * r * .85;
        X.fillStyle = hash(i * 7 + j) > .8 ? 'rgba(210,214,190,.9)' : 'rgba(26,32,20,.9)'; X.beginPath(); X.arc(x, y, 1.6 + hash(i + j * 3) * 4.2, 0, 7); X.fill(); }
      // feine Fäden (Myzel)
      X.save(); X.strokeStyle = 'rgba(40,48,30,.6)'; X.lineWidth = 1.2; for (let i = 0; i < 10; i++) { const a = hash(j * 30 + i) * 6.28; X.beginPath(); X.moveTo(cx, cy); X.quadraticCurveTo(cx + Math.cos(a + .5) * R * .6, cy + Math.sin(a + .5) * R * .6, cx + Math.cos(a) * R * 1.1, cy + Math.sin(a) * R); X.stroke(); } X.restore(); }); }
  X.restore();
}
// Lupe mit beliebigem Inhalt (draw), Vergrößerung m um den Lupenmittelpunkt
function loupeOf(x, y, r, m, draw) {
  X.save(); X.beginPath(); X.arc(x, y, r, 0, 7); X.clip(); X.translate(x, y); X.scale(m, m); X.translate(-x, -y); draw(); X.restore();
  X.save(); X.lineWidth = 16; X.strokeStyle = '#a9812f'; X.beginPath(); X.arc(x, y, r + 8, 0, 7); X.stroke(); X.lineWidth = 3; X.strokeStyle = P.ink; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.beginPath(); X.arc(x, y, r + 16, 0, 7); X.stroke();
  X.globalAlpha = .6; X.strokeStyle = '#f6e7c0'; X.lineWidth = 4; X.beginPath(); X.arc(x, y, r - 12, -2.6, -1.9); X.stroke(); X.globalAlpha = 1;
  X.translate(x, y); X.rotate(.75); const h = new Path2D(); h.rect(r + 16, -18, 190, 36); X.fillStyle = '#3a2618'; X.fill(h); X.save(); X.clip(h); X.globalAlpha = .5; X.fillStyle = hatchPat('#c9a26a', 6, 1, 1); X.fillRect(r, -30, 240, 60); X.restore(); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(h); X.restore(); }
// Etikett am Objekt: Pergament-Schild mit Versal-Wort, Maske von unten, fertig bei k; Faden zum Ziel
function tag(t, s, x, y, size, k, col, tx, ty, o = {}) {
  const p = e4(lin(t, k - .28, k)); if (p <= 0) return;
  X.save(); X.font = `800 ${size}px CZ`; X.letterSpacing = (size * .06) + 'px'; const w = X.measureText(s).width, pad = size * .32, bw = w + pad * 2, bh = size * 1.25;
  const x0 = x - bw / 2, y0 = y - bh / 2;
  // Faden
  X.strokeStyle = col; X.lineWidth = 3; X.globalAlpha = p; X.beginPath(); X.moveTo(tx, ty); X.lineTo(mix(tx, x0 + (tx < x ? 0 : bw), 1), y); X.stroke(); X.beginPath(); X.arc(tx, ty, 6, 0, 7); X.fillStyle = col; X.fill(); X.globalAlpha = 1;
  // Schild
  const plate = new Path2D(); plate.rect(x0, y0, bw, bh); X.fillStyle = '#e6d6b6'; X.fill(plate); X.save(); X.clip(plate); X.globalAlpha = .28; X.drawImage(GR[2], 0, 0, W, H); X.restore();
  X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(plate); X.lineWidth = 1.2; X.strokeRect(x0 + 7, y0 + 7, bw - 14, bh - 14);
  X.save(); X.beginPath(); X.rect(x0, y0, bw, bh); X.clip(); X.fillStyle = col; X.textBaseline = 'alphabetic'; X.fillText(s, x0 + pad, y + size * .36 + (1 - p) * bh); X.restore();
  X.restore(); }
function sceneSection(t) {
  DARK = 0; parchment(t, 1000, 560);
  sectionDraw(t);
  // Lupe fährt auf „Balken“/„Schimmel“ auf den Balkenkopf und bleibt dort
  const li = eio(lin(t, K.balken + .1, K.schimmel - .25)), lx = mix(1560, 900, li), ly = mix(-200, 470, li) + Math.sin(t * 2.2) * 3;
  if (li > 0) { loupeOf(lx, ly, 150, 2.2, () => { parchment(t, lx, ly); sectionDraw(t); });
    ringPulse(lx, ly, t, K.schimmel - .05, 160, 280, P.red, .6, 3);
    tag(t, 'SCHIMMEL', 1480, 250, 96, K.schimmel - .02, P.red, lx + 110, ly - 100); }
  // Die Wand teilt sich: zwei Putzhälften mit dem Fleck gleiten auseinander
  const k = eio(lin(t, C.b, K.dahinter));
  if (k < 1) { const edge = []; for (let i = 0; i <= 14; i++) edge.push([960 + (hash(i * 5.7) - .5) * 70, i / 14 * 1080]);
    for (const side of [-1, 1]) { X.save(); X.translate(side * k * 1150, 0); X.rotate(side * k * .05);
      const p = new Path2D(); if (side < 0) { p.moveTo(-50, 0); edge.forEach(q => p.lineTo(q[0], q[1])); p.lineTo(-50, 1080); } else { p.moveTo(1970, 0); edge.forEach(q => p.lineTo(q[0], q[1])); p.lineTo(1970, 1080); } p.closePath();
      X.fillStyle = '#e9dcc0'; X.fill(p); X.save(); X.clip(p); X.globalAlpha = .3; X.drawImage(GR[1], 0, 0, W, H); X.globalAlpha = 1;
      const g = X.createRadialGradient(960, 560, 0, 960, 560, 520); g.addColorStop(0, 'rgba(88,92,60,.8)'); g.addColorStop(.7, 'rgba(110,98,62,.55)'); g.addColorStop(1, 'rgba(120,100,60,0)'); X.fillStyle = g; X.fillRect(0, 0, W, H); X.restore();
      X.strokeStyle = P.ink; X.lineWidth = 3.4; X.stroke(p); X.restore(); } }
  finish(t);
}

// ---------- C: Drüberstreichen – der Fleck schlägt durch ----------
function roller(x, y, s) { X.save(); X.translate(x, y); X.scale(s, s);
  const r = new Path2D(); r.rect(-110, -34, 220, 68); X.fillStyle = '#efe6d2'; X.fill(r); hatchPath(r, P.ink2, 5, 1, .35, -1); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(r);
  X.beginPath(); X.moveTo(110, 0); X.lineTo(150, 0); X.lineTo(150, 90); X.lineTo(20, 110); X.lineTo(20, 330); X.stroke();
  const h = new Path2D(); h.rect(4, 200, 32, 150); X.fillStyle = P.red; X.fill(h); X.stroke(h); X.restore(); }
function scenePaint(t) {
  DARK = 0; parchment(t, 960, 540);
  camLook(-3.75, 1.8, 0, mix(8.2, 7.6, lin(t, C.c, C.d)), -.22, 0, 1400, 960, 600);
  groundLine();
  const pk = eio(lin(t, C.c + .02, K.drueber)), bleed = eo(lin(t, K.drueber + .02, C.d - .05));
  house3(t, { stain: 1.45, mold: .7, paint: pk, bleed });
  if (t < K.drueber + .1) { const top = prj(fp(-3.75, mix(.45, 3.15, pk))); roller(top[0], top[1] + Math.sin(t * 18) * 3, 1.3); }
  if (bleed > .3) { const c = prj(fp(STAIN[0], STAIN[1])); ringPulse(c[0], c[1], t, K.drueber + .15, 40, 330, P.red, .4, 3); }
  finish(t);
}

// ---------- D: Dunkel – das ganze Haus ----------
function sceneRisk(t) {
  DARK = 1; darkBG(t, 1200, 480, .9, 1);
  const yaw = mix(-.55, -.4, lin(t, C.d, C.e));
  camLook(0, 5, 4, mix(30, 25, lin(t, C.d, C.e)), yaw, -.1, 1400, 1010, 600);
  const sag = eio(lin(t, K.riskiert, K.haus + .3));
  const _prj = prj; prj = p => { const d = sag * .55 * clamp((1 - (p[0] + 5) / 10)) * (1 - p[1] / 14); return _prj([p[0] + sag * .12 * p[1] * .1, p[1] - d, p[2]]); };
  // Fäulnis kriecht vom Fleck durch alle Hölzer, auf „Haus“ ist das ganze Haus erfasst
  const rot = 13.5 * eio(lin(t, K.riskiert + .05, K.haus));
  house3(t, { stain: 1.4, mold: 1, crack: eo(lin(t, K.riskiert, K.riskiert + .5)), lineCol: P.cream, lc2: P.cream, rot });
  prj = _prj;
  for (let i = 0; i < 14; i++) { const t0 = K.riskiert + .2 + i * .12; const k = lin(t, t0, t0 + .8); if (k <= 0 || k >= 1) continue; const s = prj(fp(-4.5 + hash(i) * 7, 1 + hash(i * 3) * 5)); const x = s[0] + (hash(i * 7) - .5) * 60 * k, y = s[1] + k * k * 300;
    X.save(); X.translate(x, y); X.rotate(k * 4 * (hash(i) - .5)); const p = new Path2D(); p.moveTo(-12, -8); p.lineTo(14, -10); p.lineTo(10, 9); p.lineTo(-9, 12); p.closePath(); stroke(p, 2, P.cream, 8); X.restore(); }
  finish(t, true);
}

// ---------- E: Genau hinsehen – Lichtkegel und Lupe tasten ab ----------
function loupe(x, y, r, t, mag) {
  X.save(); X.beginPath(); X.arc(x, y, r, 0, 7); X.clip(); parchment(t, x, y);
  const f0 = CAM.f, cx0 = CAM.cx, cy0 = CAM.cy; CAM.f = f0 * mag; CAM.cx = x - (x - cx0) * mag; CAM.cy = y - (y - cy0) * mag;
  house3(t, { stain: 1.4, mold: 1, crack: 1 }); CAM.f = f0; CAM.cx = cx0; CAM.cy = cy0; X.restore();
  X.save(); X.lineWidth = 16; X.strokeStyle = '#a9812f'; X.beginPath(); X.arc(x, y, r + 8, 0, 7); X.stroke(); X.lineWidth = 3; X.strokeStyle = P.ink; X.beginPath(); X.arc(x, y, r, 0, 7); X.stroke(); X.beginPath(); X.arc(x, y, r + 16, 0, 7); X.stroke();
  X.globalAlpha = .6; X.strokeStyle = '#f6e7c0'; X.lineWidth = 4; X.beginPath(); X.arc(x, y, r - 12, -2.6, -1.9); X.stroke(); X.globalAlpha = 1;
  X.translate(x, y); X.rotate(.75); const h = new Path2D(); h.rect(r + 16, -18, 190, 36); X.fillStyle = '#3a2618'; X.fill(h); X.save(); X.clip(h); X.globalAlpha = .5; X.fillStyle = hatchPat('#c9a26a', 6, 1, 1); X.fillRect(r, -30, 240, 60); X.restore(); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(h); X.restore(); }
// Abtastweg über die Fassade (Fassadenkoordinaten, Ankunftszeit)
const SCAN = [[4.2, 9.6, K.lampe + .18], [1.3, 8.9, K.bh + .45], [1.3, 4.75, K.sehen - .3], [-1.3, 4.75, K.sehen + .05], [-1.2, 2.3, K.erst2], [STAIN[0] + .35, STAIN[1] + .25, K.genau - .06]];
function scanAt(t) { if (t <= SCAN[0][2]) return [SCAN[0][0], SCAN[0][1]]; for (let i = 1; i < SCAN.length; i++) { const a = SCAN[i - 1], b = SCAN[i]; if (t <= b[2]) { const k = eio(lin(t, a[2] + .06, b[2])); return [mix(a[0], b[0], k), mix(a[1], b[1], k)]; } } const q = SCAN[SCAN.length - 1]; return [q[0], q[1]]; }
function sceneLook(t) {
  DARK = 0; parchment(t, 1000, 540);
  camLook(-.3, 4.6, 0, mix(20.5, 19.2, lin(t, C.e, C.f)), -.42, 0, 1400, 1000, 560);
  groundLine(); house3(t, { stain: 1.4, mold: 1, crack: 1 });
  const [u, v] = scanAt(t), tgt = prj(fp(u, v));
  const enter = eo(lin(t, C.e, K.lampe + .18)), lx = mix(2150, tgt[0], enter), ly = mix(-120, tgt[1], enter);
  const on = lin(t, K.lampe - .03, K.lampe + .12), focus = eo(lin(t, K.genau - .15, K.genau + .35));
  const sr = mix(300, 230, focus);
  // Dunkel mit Lichtkegel
  if (on > 0) { X.save(); const g = X.createRadialGradient(lx, ly, sr * .55, lx, ly, sr * 2.1); g.addColorStop(0, 'rgba(24,14,6,0)'); g.addColorStop(1, `rgba(24,14,6,${.62 * on})`); X.fillStyle = g; X.fillRect(0, 0, W, H);
    // Kegel von der Lampe oben rechts
    const L = [2020, -140], ang = Math.atan2(ly - L[1], lx - L[0]), d = Math.hypot(lx - L[0], ly - L[1]), w = Math.asin(Math.min(.99, sr / d));
    X.globalCompositeOperation = 'lighter'; const cg = X.createLinearGradient(L[0], L[1], lx, ly); cg.addColorStop(0, `rgba(255,236,190,${.16 * on})`); cg.addColorStop(1, `rgba(255,236,190,${.07 * on})`); X.fillStyle = cg;
    X.beginPath(); X.moveTo(L[0], L[1]); X.lineTo(L[0] + Math.cos(ang - w) * d * 1.02, L[1] + Math.sin(ang - w) * d * 1.02); X.arc(lx, ly, sr, ang - w - Math.PI / 2 + Math.PI, ang + w + Math.PI / 2 + Math.PI, true); X.closePath(); X.fill();
    const sg = X.createRadialGradient(lx, ly, 0, lx, ly, sr); sg.addColorStop(0, `rgba(255,240,205,${.22 * on})`); sg.addColorStop(1, 'rgba(255,240,205,0)'); X.fillStyle = sg; X.beginPath(); X.arc(lx, ly, sr, 0, 7); X.fill(); X.restore(); }
  loupe(lx, ly, 150, t, mix(2.3, 3.0, focus));
  ringPulse(lx, ly, t, K.genau - .05, 160, 300, P.red, .6, 3);
  finish(t);
}

// ---------- F: Vermessen ----------
function elevCam(t, z0, z1, a, b, e = lin) { camLook(.2, 4.9, 0, mix(z0, z1, e(t, a, b)), -.12, 0, 1400, 990, 560); }
function sceneMeasure(t) {
  DARK = 0; parchment(t, 1000, 540); elevCam(t, 20.5, 19.5, C.f, C.g);
  groundLine(); house3(t, { stain: 1.4, mold: 1, crack: 1 });
  // „Jeder Balken“: alle Hölzer werden rot nachgezogen, links -> rechts, eines bekommt die Maßkette
  const sw = lin(t, K.jeder - .35, K.jeder + .25);
  if (sw > 0) { X.save(); TIMBER.forEach(tb => { const mu = (tb[0] + tb[2]) / 2, k = clamp((sw * 13 - (mu + 5.5)) / 1.2) * (1 - lin(t, K.jeder2 - .1, K.jeder2 + .4) * .7); if (k <= 0) return; X.globalAlpha = k; X.strokeStyle = P.red; X.lineWidth = 3.2; X.stroke(poly3(timberQuad(tb))); }); X.restore(); }
  const q = TIMBER[1], A = prj(fp(q[0] - .3, q[1])), B = prj(fp(q[0] - .3, q[3])); dim(A[0] - 30, A[1], B[0] - 30, B[1], tin(t, K.jeder + .32, .35), '2,85 m', P.red, 6);
  // „jeder Riss“: Riss eingekreist, Rissbreite 3 mm
  const rk = tin(t, K.riss, .3), c1 = prj(fp(-1.2, 2.3)), cr = 84;
  if (rk > 0) { X.save(); X.strokeStyle = P.red; X.lineWidth = 2.6; X.beginPath(); X.arc(c1[0], c1[1], cr, -Math.PI / 2, -Math.PI / 2 + 6.283 * eo(rk)); X.stroke();
    if (rk >= 1) { X.beginPath(); X.moveTo(c1[0] + cr * .7, c1[1] - cr * .7); X.lineTo(c1[0] + 150, c1[1] - 140); X.lineTo(c1[0] + 260, c1[1] - 140); X.stroke(); } X.restore();
    mono('3 mm', c1[0] + 160, c1[1] - 152, 30, P.red, 'left', lin(rk, .7, 1), 2); }
  // „zentimetergenau“: Lineal mit Zentimeterteilung unter dem Haus
  const L0 = prj(fp(-5, -1.3)), L1 = prj(fp(5, -1.3)), lk = eo(tin(t, K.zgenau, .4));
  if (lk > 0) { X.save(); X.strokeStyle = P.red; X.lineWidth = 2; X.beginPath(); X.moveTo(L0[0], L0[1]); X.lineTo(mix(L0[0], L1[0], lk), mix(L0[1], L1[1], lk)); for (let i = 0; i <= 200; i++) { const u = i / 200; if (u > lk) break; const x = mix(L0[0], L1[0], u), y = mix(L0[1], L1[1], u), l = i % 20 === 0 ? 22 : i % 10 === 0 ? 15 : 8; X.moveTo(x, y); X.lineTo(x, y + l); } X.stroke();
    X.fillStyle = P.red; X.font = '500 20px PM'; X.textAlign = 'center'; for (let m = 0; m <= 10; m += 2) { if (m / 10 > lk) break; X.fillText(m + ' m', mix(L0[0], L1[0], m / 10), L0[1] + 46); } X.restore(); }
  // „vermessen“: Gesamtmaße + Zirkelbogen
  const vk = tin(t, K.vermessen, .4); const T0 = prj(fp(5.5, -.1)), T1 = prj(fp(5.5, RIDGE)); dim(T0[0] + 40, T0[1], T1[0] + 40, T1[1], vk, '10,50 m', P.red, 8);
  const G0 = prj(fp(-5, 11.3)), G1 = prj(fp(5, 11.3)); dim(G0[0], G0[1], G1[0], G1[1], vk, '10,20 m', P.red, -52);
  if (vk > 0) { const ap = prj(fp(0, RIDGE)); X.save(); X.strokeStyle = P.ink; X.lineWidth = 1.6; X.globalAlpha = .7; X.beginPath(); X.arc(ap[0], ap[1], 300, Math.PI * .25, Math.PI * .25 + Math.PI * .5 * eo(vk)); X.stroke(); X.restore(); }
  return { vk };
}
function sceneMeasureF(t) { sceneMeasure(t); finish(t); }

// ---------- G: Im Plan – was bleibt, was ersetzt wird ----------
function planFrame(t, k) { if (k <= 0) return; const x0 = 250, y0 = 50, x1 = 1760, y1 = 1020;
  const pts = [[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]], sub = polySub(pts, 0, eo(k));
  X.save(); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(pathOf(sub)); X.lineWidth = 1.3; X.stroke(pathOf(polySub([[x0 + 14, y0 + 14], [x1 - 14, y0 + 14], [x1 - 14, y1 - 14], [x0 + 14, y1 - 14], [x0 + 14, y0 + 14]], 0, eo(k))));
  // Schriftfeld unten rechts (Linien, darin die Legende)
  const a = lin(k, .6, 1); X.globalAlpha = a; X.lineWidth = 2; X.strokeRect(x1 - 14 - 330, y1 - 14 - 150, 330, 150); X.beginPath(); X.moveTo(x1 - 344, y1 - 89); X.lineTo(x1 - 14, y1 - 89); X.stroke();
  X.restore(); }
function scenePlan(t) {
  DARK = 0; parchment(t, 1000, 540); elevCam(t, 19.5, 21.8, C.g, C.g + .4, (t, a, b) => eio(lin(t, a, b)));
  groundLine();
  const b = eo(tin(t, K.bleibt, .35)), e = eo(tin(t, K.ersetzt, .35)), lift = eo(lin(t, K.ersetzt + .2, K.ersetzt + .8));
  house3(t, { stain: 1.4 * (1 - lin(t, K.wird2, K.wird2 + .4)), mold: 1, crack: 1, plan: { bleibt: b, ersetzt: e, lift } });
  planFrame(t, lin(t, C.g, K.im));
  const x1l = 1446; const lg = (y, col, s, k, dashed) => { if (k <= 0) return; X.save(); X.globalAlpha = k; X.fillStyle = col; X.fillRect(x1l, y - 26, 56, 32); if (dashed) { X.setLineDash([8, 6]); X.strokeStyle = P.red; } else X.strokeStyle = P.ink; X.lineWidth = 2.4; X.strokeRect(x1l, y - 26, 56, 32); X.restore(); mono(s, x1l + 76, y, 28, P.ink, 'left', k); };
  lg(906, '#c69b3c', 'BLEIBT', b, false); lg(980, '#c8563c', 'ERSETZT', e, true);
  finish(t);
}

// ---------- H: Gebaut mit Kalk und Holz, wie damals ----------
function trowel(x, y, a) { X.save(); X.translate(x, y); X.rotate(a); const b = new Path2D(); b.moveTo(-90, 0); b.lineTo(70, -30); b.lineTo(90, 0); b.lineTo(70, 30); b.closePath(); X.fillStyle = '#b7bcbf'; X.fill(b); hatchPath(b, P.ink2, 5, 1, .3); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(b);
  X.beginPath(); X.moveTo(0, 0); X.lineTo(0, -60); X.lineTo(-20, -60); X.stroke(); const h = new Path2D(); h.rect(-110, -76, 90, 30); X.fillStyle = '#8a5a32'; X.fill(h); X.stroke(h); X.restore(); }
function sceneBuild(t) {
  DARK = 0; parchment(t, 1000, 540);
  camLook(-3.1, 1.9, 0, mix(9.6, 8.9, lin(t, C.h, C.i)), -.28, 0, 1400, 1110, 640);
  groundLine();
  const wk = eio(lin(t, K.holz - .45, K.holz));
  house3(t, { stain: 0, plan: { lift: (1 - wk) * 3 }, newWood: true, pegs: t > K.damals - .2 });
  // Holznägel werden eingeschlagen (wie damals)
  if (t > K.damals - .25 && t < K.damals + .6) { [[-4.87, .5], [-4.87, 3.05], [-4.6, .55], [-2.9, 2.2]].forEach(([u, v], i) => { const c = prj(fp(u, v)); ringPulse(c[0], c[1], t, K.damals - .25 + i * .1, 6, 44, P.ink, .35, 2); }); }
  // Kalkputz: Kelle holt Kalk aus dem Eimer und streicht das Gefach zu
  const kk = eio(lin(t, K.kalk - .3, K.kalk + .6));
  if (kk > 0) { const pts = [fp(-4.7, .5), fp(-2.75, .5), fp(-2.75, mix(.5, 3.1, kk)), fp(-4.7, mix(.5, 3.1, kk))]; const p = poly3(pts); X.fillStyle = '#f4ecdb'; X.fill(p); X.save(); X.clip(p); X.globalAlpha = .35; X.drawImage(GR[1], 0, 0, W, H); X.restore(); }
  const bucket = [400, 900];
  { const fly = eio(lin(t, K.gebaut + .1, K.kalk - .3)); const e = prj(fp(-3.7, mix(.5, 3.1, kk))), sx = mix(bucket[0] + 40, e[0] + 20, fly), sy = mix(bucket[1] - 150, e[1] + 10, fly) - Math.sin(fly * Math.PI) * 120;
    if (t < K.kalk + .9) { trowel(sx, sy, -.15 + (kk > 0 ? Math.sin(t * 9) * .12 : 0)); if (fly < 1) { X.fillStyle = '#f4ecdb'; X.strokeStyle = P.ink; X.lineWidth = 2; X.beginPath(); X.ellipse(sx + 10, sy - 14, 44, 12, -.15, 0, 7); X.fill(); X.stroke(); } } }
  if (t > K.holz - .02 && t < K.holz + .45) { const c = prj(fp(-4.87, 1.8)); for (let i = 0; i < 10; i++) { const a = i / 10 * 6.28, k = lin(t, K.holz, K.holz + .45); X.save(); X.globalAlpha = 1 - k; X.strokeStyle = P.ink; X.lineWidth = 2.4; X.beginPath(); X.moveTo(c[0] + Math.cos(a) * 60, c[1] + Math.sin(a) * 60); X.lineTo(c[0] + Math.cos(a) * (90 + 40 * k), c[1] + Math.sin(a) * (90 + 40 * k)); X.stroke(); X.restore(); } }
  // Kalkeimer mit Etikett
  X.save(); X.translate(bucket[0], bucket[1]); const bk = new Path2D(); bk.moveTo(-90, -120); bk.lineTo(90, -120); bk.lineTo(70, 40); bk.lineTo(-70, 40); bk.closePath(); X.fillStyle = '#c9bca3'; X.fill(bk); hatchPath(bk, P.ink2, 6, 1, .45); X.strokeStyle = P.ink; X.lineWidth = 3; X.stroke(bk);
  X.beginPath(); X.ellipse(0, -120, 90, 22, 0, 0, 7); X.fillStyle = '#f4ecdb'; X.fill(); X.stroke(); X.beginPath(); X.arc(0, -120, 110, Math.PI * 1.1, Math.PI * 1.9); X.stroke();
  X.fillStyle = '#efe5cf'; X.fillRect(-58, -70, 116, 50); X.strokeRect(-58, -70, 116, 50); X.restore();
  mono('KALK', bucket[0] + 2, bucket[1] - 33, 32, P.ink, 'center', 1, 6);
  finish(t);
}

// ---------- I: Gold – trocken, 100 Jahre ----------
function sceneGold(t) {
  DARK = 1; darkBG(t, 960, 460, 1, .8);
  const yaw = mix(-.62, -.3, eio(lin(t, C.i, C.j))), up = eio(lin(t, K.naechsten - .3, K.n100 - .2));
  camLook(0, 5, 4, mix(mix(27, 25, lin(t, C.i, K.naechsten)), 33, up), yaw, -.08, 1400, 960, mix(560, 420, up));
  // Regen – prallt am Schutzbogen ab
  const ak = eo(tin(t, K.trocken, .4)), a0 = prj([0, RIDGE, 0]), R = 520 * mix(1, .8, up), acx = a0[0], acy = a0[1] - 90 * mix(1, .8, up) + R;
  X.save(); for (let i = 0; i < 140; i++) { const x = hash(i * 1.3) * 2200 - 100, sp = 900 + hash(i * 2.1) * 400; let y = ((hash(i * 4.4) * 1200 + t * sp) % 1200) - 200;
    const dx = x - acx, lim = Math.abs(dx) < R ? acy - Math.sqrt(R * R - dx * dx) : 9999; if (ak > .5 && y + 40 > lim) { if (y > lim + 80) continue; y = lim - 40; }
    X.strokeStyle = `rgba(230,210,160,${.12 + hash(i) * .25})`; X.lineWidth = 1.6; X.beginPath(); X.moveTo(x, y); X.lineTo(x - 8, y + 40); X.stroke(); } X.restore();
  house3(t, { stain: 0, lit: eo(lin(t, K.ihr - .25, K.haus2)), lineCol: P.gold });
  if (ak > 0) { X.save(); X.strokeStyle = P.goldL; X.shadowColor = P.gold; X.shadowBlur = 20; X.lineWidth = 3; X.beginPath(); X.arc(acx, acy, R, Math.PI * (1.5 - .32 * ak), Math.PI * (1.5 + .32 * ak)); X.stroke(); X.restore();
    for (let i = 0; i < 9; i++) { const u = (i + .5) / 9, an = Math.PI * (1.5 - .3 + .6 * u), px = acx + Math.cos(an) * R, py = acy + Math.sin(an) * R; spark(px, py - ((t * 60 + i * 13) % 20), 10 * ak, ak * .8, '#fff2c8'); } }
  // Jahresleiste läuft 2026 -> 2126 und steht auf „hundert“
  const yr = Math.round(mix(2026, 2126, eio(lin(t, K.trocken + .4, K.n100 - .02))));
  X.save(); X.globalAlpha = lin(t, K.trocken + .2, K.trocken + .4); X.strokeStyle = hexA(P.gold, .6); X.lineWidth = 1.5; X.strokeRect(330, 70, 1260, 64); X.fillStyle = 'rgba(0,0,0,.45)'; X.fillRect(330, 70, 1260, 64);
  X.beginPath(); X.rect(330, 70, 1260, 64); X.clip(); const off = (yr - 2026) * 10.8; X.font = '500 34px PM'; X.letterSpacing = '4px'; X.textAlign = 'center';
  for (let y = 2000; y <= 2175; y += 25) { const x = 960 + (y - 2026) * 10.8 - off; X.fillStyle = Math.abs(x - 960) < 60 ? P.goldL : hexA(P.gold, .45); X.fillText(String(y), x, 114); }
  X.fillStyle = P.goldL; X.beginPath(); X.moveTo(948, 70); X.lineTo(972, 70); X.lineTo(960, 84); X.fill(); X.restore();
  // Überschrift 2: „100 JAHRE.“ als Ganzes, steht auf „hundert“
  headline(t, [{ s: '100', size: 230, y: 900, gold: 1, ls: 12 }, { s: 'JAHRE', size: 86, y: 1010, gold: 1 }], K.n100 - .02, { align: 'center', d: .3 });
  if (t > K.n100 - .34) { X.save(); X.globalCompositeOperation = 'lighter'; const g = X.createRadialGradient(960, 830, 0, 960, 830, 420); g.addColorStop(0, `rgba(255,210,120,${.18 * lin(t, K.n100 - .34, K.n100)})`); g.addColorStop(1, 'rgba(0,0,0,0)'); X.fillStyle = g; X.fillRect(0, 400, W, 680); X.restore(); }
  finish(t, true);
}

// ---------- J: Schluss – Marke, Angebot, Kontakt ----------
function emblem(t, cx, cy, s, k) { if (k <= 0) return;
  const outline = [[-1, .15], [-1, -.55], [0, -1.25], [1, -.55], [1, .15], [-1, .15]].map(q => [cx + q[0] * s, cy + q[1] * s]);
  const beams = [[[-1, -.2], [1, -.2]], [[0, -1.25], [0, .15]], [[-1, .15], [0, -.55]], [[1, .15], [0, -.55]], [[-1, -.55], [1, -.55]]].map(l => l.map(q => [cx + q[0] * s, cy + q[1] * s]));
  X.save(); DARK = 1; stroke(pathOf(polySub(outline, 0, eo(lin(k, 0, .7)))), 4, P.gold, 18);
  beams.forEach((b, i) => { const kk = eo(lin(k, .35 + i * .1, .75 + i * .06)); if (kk > 0) stroke(pathOf(polySub(b, 0, kk)), 3, P.gold, 14); }); X.restore(); }
// „KOSTENLOS.“ wird auf seinem Wort rot und bekommt einen gezogenen Unterstrich (Stempel-Geste)
function offerLand(t, k) { if (k <= 0) return; X.save(); X.font = '800 68px CZ'; X.letterSpacing = (68 * .06) + 'px';
  X.font = '800 76px CZ'; X.letterSpacing = (76 * .06) + 'px'; const a = X.measureText('ERSTGESPRÄCH ').width, b = X.measureText('KOSTENLOS').width, x0 = 960 - (a + b) / 2 + a;
  const pulse = 1 - lin(t, K.kostenlos, K.kostenlos + .5); X.shadowColor = '#ff5030'; X.shadowBlur = 24 + 30 * pulse;
  X.strokeStyle = '#ff6a4a'; X.lineWidth = 4; X.lineCap = 'round'; X.beginPath(); X.moveTo(x0, 752); X.lineTo(x0 + (b - 8) * k, 752); X.stroke(); X.restore(); }
function sceneEnd(t) {
  DARK = 1; darkBG(t, 960, 440, .8, .7);
  camLook(0, 5, 4, mix(32, 27, lin(t, C.j, DUR)), -.5 + (t - C.j) * .09, -.08, 1400, 960, 560);
  X.save(); X.globalAlpha = .1 * lin(t, C.j, C.j + .6); house3(t, { stain: 0, lit: 0, lineCol: P.gold }); X.restore();
  emblem(t, 960, 250, 70, lin(t, C.j, K.ende));
  headline(t, [{ s: 'BAUHÜTTE', size: 120, y: 440, gold: 1 }, { s: 'ARCHITEKTEN', size: 60, y: 525 }], K.ende - .02, { align: 'center', d: .32 });
  const kl = eo(lin(t, K.kostenlos - .28, K.kostenlos - .02));
  headline(t, [{ segs: [{ s: 'ERSTGESPRÄCH ' }, { s: 'KOSTENLOS', red: kl > .5 ? 1 : 0 }], size: 76, y: 720 }], K.erst - .02, { align: 'center', d: .3 });
  offerLand(t, kl);
  for (let i = 0; i < 40; i++) { const ph = (t * (.12 + hash(i) * .1) + hash(i * 3.3)) % 1, x = 300 + hash(i * 7.1) * 1320 + Math.sin(t * 1.5 + i) * 20, y = 1100 - ph * 1000; spark(x, y, 3 + hash(i * 2) * 5, (1 - ph) * .8, '#ffd9a0'); }
  mono('0221 348 71 90  ·  bauhuette-architekten.de', 960, 850, 30, P.goldL, 'center', lin(t, K.kostenlos + .5, K.kostenlos + .9) * .85);
  finish(t, true);
}

function frame(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.globalCompositeOperation = 'source-over'; X.shadowBlur = 0;
  if (t < C.b) sceneStain(t);
  else if (t < C.c) sceneSection(t);
  else if (t < C.d) scenePaint(t);
  else if (t < C.e) sceneRisk(t);
  else if (t < C.f) sceneLook(t);
  else if (t < C.g) sceneMeasureF(t);
  else if (t < C.h) scenePlan(t);
  else if (t < C.i) sceneBuild(t);
  else if (t < C.j) sceneGold(t);
  else sceneEnd(t);
}
