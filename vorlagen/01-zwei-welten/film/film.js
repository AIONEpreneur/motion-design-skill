// Netzwerk Nord IT – V6. Bild im Stil von „How browsers work in 40 seconds“ (Addy Osmani):
// Papierwelt (Diagonalstreifen, Tusche, Schraffur, Knuddel-Figuren) = Alltag im Büro,
// Blaupause (Nachtblau, Raster, leuchtende Linien, Funkeln) = was in der Technik passiert. Harte Schnitte zwischen den Welten.
// V6: keine Satz-Einblendungen mehr. Das Bild erzählt; Text nur als Beschriftung an Objekten, eine Zahl (< 60 min) und die Schlusskarte.
// V7 (neu): keine Sätze, keine Satzstücke. Betonung über Bildmittel (Status-Ring, Lupe, Kreis, Aufleuchten, rot/grün, Häkchen);
//     Text nur als Einzelwort/Zahl am Objekt (OFFLINE/ONLINE, 24/7, < 60 min, Etiketten). Zeiten aus neu vermessenem vo.json.
const CH0 = K.oft - .26;   // Beginn des Diagramm-Kapitels

// ================= Büro-Welt (Szene A und H) =================
const ROUTE = bezP([1215, 700], [1000, 380], [520, 380], [140, 640], 60);
const BLOBC = [P.lil, P.sky, P.teal, P.yel, P.pink];
function office(t, happy, tt) {
  // Holzgerüst des Bürohauses (Querschnitt), zwei Etagen mit je 10 Plätzen
  const x0 = -1250, x1 = 130, yG = 860, yF = 620, yR = 380;
  const roof = S('roof', () => polyP([[x0 - 40, yR], [(x0 + x1) / 2, 190], [x1 + 40, yR]]), 1.6);
  ink(roof, '#c77f5e', 5); hatch(roof, '#8e4c35', 12, 1.3, .55);
  X.save(); X.globalAlpha = .9; X.strokeStyle = hexA(P.ink, .55); X.lineWidth = 2; X.beginPath(); for (let i = 1; i < 6; i++) { const y = yR - i * 30; const w = (y - 190) / (yR - 190) * ((x1 - x0) / 2 + 40); X.moveTo((x0 + x1) / 2 - w + 20, y); X.lineTo((x0 + x1) / 2 + w - 20, y); } X.stroke(); X.restore();
  const wall = S('wall', () => rrP(x0, yR, x1 - x0, yG - yR, 4), 1); X.fillStyle = hexA('#fbf6ea', .82); X.fill(wall);
  hatch(wall, P.ink2, 12, 1, .12);
  for (let w = 0; w < 4; w++) { // Fenster hinten
    for (const fy of [yR + 50, yF + 40]) { const p = S('owin' + w + fy, () => rrP(x0 + 120 + w * 320, fy, 150, 90, 6), .8); ink(p, '#dfe9ef', 2.6); X.strokeStyle = hexA(P.ink, .5); X.lineWidth = 2; X.beginPath(); X.moveTo(x0 + 195 + w * 320, fy); X.lineTo(x0 + 195 + w * 320, fy + 90); X.stroke(); if (!happy) cloud(x0 + 170 + w * 320 + ((t * 8) % 60), fy + 50, .35, 'w'); }
  }
  for (let row = 0; row < 2; row++) for (let i = 0; i < 10; i++) {
    const n = row * 10 + i, x = x0 + 80 + i * 128, y = row ? yF - 22 : yG, col = BLOBC[(n * 3) % 5];
    const mood = happy ? 'happy' : (tt > K.warten - .15 ? 'sad' : 'flat');
    blob(x - 36, y - 52, .95, col, mood, t, n, { hop: happy && ((n + Math.floor(t * 2)) % 7 === 0), look: happy ? 0 : 1, tap: !happy && n === 9 && t > K.n20 - .2 });
    desk(x + 4, y, .9, t, happy ? 'work' : 'wait', n, 40);
    // Fragezeichen-Blasen: ploppen gestaffelt auf, alle fertig auf „warten“
    if (!happy) { const k0 = K.n20 + .05 + ((n * 7) % 20) * .025, k = back(lin(t, k0, k0 + .22)); if (k > 0) { X.save(); X.translate(x - 22, y - 158 + Math.sin(t * 3 + n) * 3); X.scale(k, k);
      const b = S('bub', () => [...ellP(0, 0, 24, 24, 4, Math.PI * .62, Math.PI * 2.38), [-14, 30]], .6); ink(b, P.win, 2.4);
      X.font = '700 30px IN'; X.fillStyle = P.ink; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText('?', 0, 2); X.restore(); } }
  }
  hangingPlant(x0 + 60, yR + 40, t, .8); hangingPlant(x1 - 70, yF + 50, t + 1, .7);
  // Balken
  for (const [yy, hh] of [[yF, 22], [yR - 6, 20]]) { const p = S('beam' + yy, () => rrP(x0 - 20, yy, x1 - x0 + 40, hh, 3), 1); ink(p, P.wood, 4); hatch(p, P.woodD, 12, 1.2, .5); X.fillStyle = P.ink; for (let bx = x0; bx < x1; bx += 160) { X.beginPath(); X.arc(bx + 10, yy + hh / 2, 3.4, 0, 7); X.fill(); } }
  for (const px of [x0 - 10, x1 - 10]) { const p = S('post' + px, () => rrP(px, yR - 6, 22, yG - yR + 6, 3), 1); ink(p, P.wood, 4); hatch(p, P.woodD, 12, 1.2, .5); }
}
// Wanduhr und Abreißkalender „MO“: Montagmorgen, 8:00 – in Szene A und als Spiegelbild in Szene H
function calendarMO(x, y, t) {
  X.save(); X.translate(x, y); X.rotate(Math.sin(t * 1.3) * .015);
  X.strokeStyle = hexA(P.ink, .8); X.lineWidth = 1.8; X.beginPath(); X.moveTo(0, -150); X.lineTo(-40, -92); X.moveTo(0, -150); X.lineTo(40, -92); X.stroke();
  X.fillStyle = P.ink; X.beginPath(); X.arc(0, -150, 5, 0, 7); X.fill();
  const pad = S('calpad', () => rrP(-82, -92, 164, 190, 8), 1); dropHatch(pad, 10, 12, .5); ink(pad, '#fbf8f1', 4.4);
  const head = S('calhead', () => rrP(-82, -92, 164, 46, 8), .8); ink(head, P.red, 4); hatch(head, P.redD, 12, 1.1, .5);
  for (const rx of [-40, 40]) { X.fillStyle = '#e9e2d0'; X.beginPath(); X.arc(rx, -92, 8, 0, 7); X.fill(); X.strokeStyle = P.ink; X.lineWidth = 2.6; X.stroke(); }
  X.strokeStyle = hexA(P.ink, .35); X.lineWidth = 1.2; X.beginPath(); for (let i = 1; i < 4; i++) { X.moveTo(-78, 98 - i * 3); X.lineTo(78, 98 - i * 3); } X.stroke();
  X.font = '600 84px IN'; X.letterSpacing = '-1px'; X.fillStyle = P.ink; X.textAlign = 'center'; X.textBaseline = 'alphabetic'; X.fillText('MO', 0, 58);
  X.restore();
}
function morningClock(x, y, t, happy) {
  // Minutenzeiger springt auf 8:00 (fertig vor „Montagmorgen“), Uhr wackelt kurz; beim Warten kriecht die Zeit weiter
  const t0 = happy ? CUT.office2 + .06 : .05, jump = eo(lin(t, t0, t0 + .2));
  const spin = 8 - 1 / 60 + jump / 60 + (happy ? 0 : .07 * lin(t, K.aus + .3, CUT.loss));
  const sh = Math.sin((t - t0 - .2) * 30) * .06 * (1 - lin(t, t0 + .2, t0 + .8)) * (t > t0 + .2 ? 1 : 0);
  X.save(); X.translate(x, y); X.rotate(sh);
  X.strokeStyle = hexA(P.ink, .8); X.lineWidth = 1.8; X.beginPath(); X.moveTo(0, -128); X.lineTo(0, -178); X.stroke(); X.fillStyle = P.ink; X.beginPath(); X.arc(0, -178, 5, 0, 7); X.fill();
  wallClock(0, 0, 118, t, spin, 0);
  const rk = lin(t, t0 + .2, t0 + .9); if (rk > 0 && rk < 1) { X.save(); X.globalAlpha = 1 - rk; X.strokeStyle = P.ink; X.lineWidth = 3; X.lineCap = 'round';
    for (const s of [-1, 1]) for (let i = 0; i < 2; i++) { X.beginPath(); X.arc(0, 0, 140 + i * 16 + rk * 10, -Math.PI / 2 + s * .45 - .16, -Math.PI / 2 + s * .45 + .16); X.stroke(); } X.restore(); }
  X.restore();
}
function statusRing(t, t0, col) {
  const k = eo(lin(t, t0, t0 + .25)); if (k <= 0) return;
  X.save(); X.strokeStyle = col; X.lineCap = 'round'; X.lineWidth = 6; X.shadowColor = col; X.shadowBlur = 10;
  X.beginPath(); X.ellipse(1350, 590, 200, 330, 0, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * k); X.stroke();
  for (let n = 0; n < 8; n++) { const p = lin(t, t0 + .25 + n * .9, t0 + 1.15 + n * .9); if (p <= 0 || p >= 1) continue; X.globalAlpha = (1 - p) * .8; X.lineWidth = 4; X.beginPath(); X.ellipse(1350, 590, 200 * (1 + .3 * p), 330 * (1 + .2 * p), 0, 0, 7); X.stroke(); }
  X.restore();
}
// Mail und Rechnung fliegen zum toten Server, prallen ab, landen am Boden und werden durchgestrichen – fertig auf ihr Wort
const BOUNCE = [{ k: 'mails', f: envelope, rest: [1080, 818], rot: -.22, s: 1.25 }, { k: 'rechnungen', f: invoice, rest: [915, 790], rot: .18, s: 1.25 }];
function bounceItems(t) {
  for (const it of BOUNCE) { const kw = K[it.k], k0 = kw - .8, kh = kw - .38, kl = kw - .1; if (t < k0) continue;
    let x, y, r;
    if (t < kh) { const p = Math.pow(lin(t, k0, kh), 1.25); [x, y] = polyAt(ROUTE, mix(.9, .0, p)); r = Math.sin(t * 9) * .08; }
    else { const u = eo(lin(t, kh, kl)); x = mix(1215, it.rest[0], u); y = mix(700, it.rest[1], u) - Math.sin(u * Math.PI) * 110; r = mix(0, it.rot, u) - (1 - u) * u * 3; }
    it.f(x, y, it.s, r);
    // Aufprall am Server
    const ik = lin(t, kh, kh + .3); if (ik > 0 && ik < 1) { X.save(); X.globalAlpha = 1 - ik; X.strokeStyle = P.ink; X.lineWidth = 3.4; X.lineCap = 'round'; X.beginPath();
      for (let i = 0; i < 5; i++) { const a = Math.PI * (.62 + i * .19), r0 = 26 + ik * 20, r1 = 50 + ik * 34; X.moveTo(1218 + Math.cos(a) * r0, 700 + Math.sin(a) * r0); X.lineTo(1218 + Math.cos(a) * r1, 700 + Math.sin(a) * r1); } X.stroke(); X.restore(); }
    missX(x, y, 74, lin(t, kw - .32, kw), t); ring(x, y, t, kw, 60, 170, '#e0356f', .7);
  }
}
function sceneOffice(t, happy) {
  paperBG(t, P.sBlue);
  let s, cx, cy;
  if (!happy) { const k = eio(lin(t, K.n20 - .42, K.n20 - .08)); s = mix(1 + .05 * lin(t, 0, K.n20 - .4), .66, k); cx = mix(1180, 160, k); cy = mix(560, 610, k); }
  else { const k = lin(t, CUT.office2, CUT.end); s = .66; cx = mix(160, 172, k); cy = 545; }
  X.save(); cam(s, cx, cy);
  constr(1350, 560, 420, t * .05, .45);
  ground(860, -2300, 2600, 5, 120, 900);
  cloud(1780, 250, 1.1, 'a'); cloud(560, 30, .8, 'b'); cloud(2150, 120, .9, 'c');
  // Datenweg Server -> Büro (blau gestrichelt wie im Original)
  X.save(); X.setLineDash([16, 12]); X.lineDashOffset = happy ? -t * 60 : 0; X.strokeStyle = P.dash; X.lineWidth = 4; X.stroke(pathOf(ROUTE)); X.restore();
  for (const q of [ROUTE[0], ROUTE[ROUTE.length - 1]]) { X.fillStyle = P.dash; X.beginPath(); X.arc(q[0], q[1], 7, 0, 7); X.fill(); }
  morningClock(820, 260, t, happy); calendarMO(1070, 262, t);
  // Status-Ring um den Server: rot pulsierend ab „aus“, grün ab „Team“ (zeichnet sich in 0,25 s, dann Pulse)
  if (!happy) statusRing(t, K.aus - .25, '#e0356f'); else statusRing(t, K.team - .25, '#5fae3e');
  office(t, happy, t);
  // Server
  if (!happy) {
    const off = lin(t, K.aus - .46, K.aus - .13), ledOff = [0, 1, 2, 3, 4].map(i => lin(t, K.aus - .48 + i * .06, K.aus - .42 + i * .06));
    server(1350, 860, 1, t, { on: 1 - off, mood: t > K.aus - .24 ? 'x' : 'happy', blink: (t % 2.3) < .12 ? 1 : 0, ledOff, smoke: lin(t, K.aus - .13, K.aus + .22), lamp: { on: t < K.aus - .28, t0: K.aus - .28 } });
    bounceItems(t);
  } else {
    server(1350, 860, 1, t, { on: 1, mood: 'happy', blink: (t % 2.1) < .12 ? 1 : 0, lamp: { on: true } });
    for (let i = 0; i < 6; i++) { const k = ((t - CUT.office2) * .55 + i / 6) % 1; const [x, y, a] = polyAt(ROUTE, k); (i % 2 ? invoice : envelope)(x, y - 6, .9, Math.sin(t * 4 + i) * .08); }
  }
  X.restore();
  paperGrain();
}

// ================= Blaupause: Datenverlust und Frühwarnung =================
const CARDS = [[900, 440], [1100, 385], [1300, 430], [980, 600], [1180, 560], [1380, 610]];
function card(x, y, a, broken, t, i) {
  X.save(); X.translate(x, y); X.globalAlpha *= a;
  const col = broken > 0 ? mixCol(P.lav, P.mag, clamp(broken * 2)) : P.lav;
  if (broken < .5) { const p = S('card', () => rrP(-72, -46, 144, 92, 10), .4); X.fillStyle = 'rgba(28,34,80,.85)'; X.fill(p); glow(p, col, 2, 8);
    X.strokeStyle = col; X.lineWidth = 2; X.beginPath(); X.arc(-40, -8, 16, 0, 7); X.stroke(); X.beginPath(); X.arc(-40, 26, 22, Math.PI * 1.15, Math.PI * 1.85); X.stroke();
    X.lineCap = 'round'; X.lineWidth = 5; X.globalAlpha *= .7; for (let l = 0; l < 3; l++) { X.beginPath(); X.moveTo(-8, -22 + l * 20); X.lineTo(50 - l * 12, -22 + l * 20); X.stroke(); } }
  else { const k = eo(lin(broken, .5, 1)); X.setLineDash([6, 7]); X.strokeStyle = hexA('#ff3fa0', .6 * (1 - k)); X.lineWidth = 1.6; rr(X, -72, -46, 144, 92, 10); X.stroke(); X.setLineDash([]);
    for (let f = 0; f < 6; f++) { const ang = hash(i * 13 + f) * 6.28, d = k * (60 + hash(f + i) * 90); X.save(); X.translate(Math.cos(ang) * d, Math.sin(ang) * d + k * k * 120); X.rotate(k * (hash(f * 3 + i) - .5) * 5); X.globalAlpha *= 1 - k;
      X.strokeStyle = P.mag; X.shadowColor = P.mag; X.shadowBlur = 8; X.lineWidth = 2; X.beginPath(); X.moveTo(-14, -8); X.lineTo(12, -10); X.lineTo(6, 10); X.closePath(); X.stroke(); X.restore(); } }
  X.restore();
}
function sceneLoss(t) {
  const push = lin(t, CUT.loss, CUT.watch);
  bpBG(t, 960 + push * 40, 600, t * .04);
  X.save(); cam(mix(1, 1.05, push), 900, 600);
  // Server (Linie)
  const weakLED = i => i === 2 && t > K.oft - .2 ? (Math.floor(t * 4) % 2 ? P.amber : '#6b4a2a') : P.mint;
  const draw = eo(lin(t, CUT.loss, CUT.loss + .18));
  X.save(); X.globalAlpha = draw; bpServer(470, 930, .86, t, { alarm: lin(t, K.weg - .3, K.weg) * (1 - lin(t, CH0 + .1, CH0 + .4)), ledCol: weakLED }); X.restore();
  dimLine(330, 525, 330, 915, draw); dimLine(372, 975, 568, 975, draw);
  tickRing(470, 620, 150, draw * .5, t * .1);
  // Sicherung: leerer gestrichelter Platz mit „+“ (wie im Original), rot durchgestrichen
  const sa = 1 - lin(t, CH0 - .05, CH0 + .15);
  if (sa > 0) { X.save(); X.globalAlpha = sa;
    const rt = bezP([585, 820], [760, 900], [900, 880], [1015, 870], 30), rp = polySub(rt, 0, tin(t, K.ohne, .28));
    X.setLineDash([8, 9]); X.strokeStyle = hexA(P.lav, .7); X.lineWidth = 1.8; X.stroke(pathOf(rp)); X.setLineDash([]);
    const pk = tin(t, K.ohne + .05, .3);
    if (pk > 0) { X.globalAlpha = sa * pk; X.setLineDash([10, 8]); X.strokeStyle = P.lav; X.lineWidth = 2.2; X.shadowColor = P.lav; X.shadowBlur = 8; rr(X, 1020, 830, 300, 84, 42); X.stroke(); rr(X, 1030, 840, 280, 64, 32); X.globalAlpha *= .5; X.stroke(); X.setLineDash([]); X.shadowBlur = 0; X.globalAlpha = sa * pk;
      // leerer Platz: gestrichelter Speicher-Zylinder (die Sicherung, die es nicht gibt)
      X.save(); X.setLineDash([5, 5]); X.strokeStyle = P.lav; X.lineWidth = 2; X.beginPath(); X.ellipse(1170, 850, 28, 8, 0, 0, 7); X.moveTo(1142, 850); X.lineTo(1142, 890); X.ellipse(1170, 890, 28, 8, 0, Math.PI, 0, true); X.moveTo(1198, 890); X.lineTo(1198, 850); X.moveTo(1142, 870); X.ellipse(1170, 870, 28, 8, 0, Math.PI, 0, true); X.stroke(); X.restore();
      X.strokeStyle = hexA(P.lav, .4); X.beginPath(); for (let i = 0; i <= 30; i++) { X.moveTo(1020 + i * 10, 930); X.lineTo(1020 + i * 10, i % 5 ? 936 : 942); } X.stroke(); }
    nodeDot(585, 820, pk); nodeDot(1015, 870, pk); tickRing(1170, 872, 74, tin(t, K.sicherung, .3), -t * .2, P.mag);
    const xk = tin(t, K.sicherung, .3); if (xk > 0) { X.save(); X.shadowColor = P.mag; X.shadowBlur = 14; missX(1170, 872, 58, xk * 1.0, t); X.restore(); ring(1170, 872, t, K.sicherung, 40, 190, P.mag, .8); }
    X.restore(); }
  // Kundendaten fliegen aus dem Server – und sind weg
  const ca = 1 - lin(t, CH0 + .15, CH0 + .3);
  if (ca > 0) {
    CARDS.forEach(([x, y], i) => { const k0 = K.kunden - .55 + i * .04, p = eo(lin(t, k0, k0 + .3)); if (p <= 0) return;
      const sx = 470, sy = 650; const br = lin(t, K.weg - .32 + i * .02, K.weg + .35);
      card(mix(sx, x, p), mix(sy, y, p) - Math.sin(p * Math.PI) * 80 + Math.sin(t * 3 + i) * 5, ca * p, br, t, i); });
    tagB('Kundendaten', 1140, 300, 26, tin(t, K.kunden - .25, .3) * ca, t > K.weg - .1 ? P.mag : P.lav);
    if (t > K.weg - .05 && t < K.weg + .6) for (let i = 0; i < 6; i++) spark(CARDS[i][0] + 20, CARDS[i][1] - 10, 16 * (1 - lin(t, K.weg, K.weg + .5)), 1 - lin(t, K.weg, K.weg + .5), '#ffd0ea');
    ring(1140, 500, t, K.weg - .05, 60, 420, P.mag, .8, 2.5);
    const rc = eo(lin(t, K.weg - .28, K.weg - .03)); if (rc > 0) { X.save(); X.globalAlpha = ca; X.strokeStyle = P.mag; X.lineWidth = 4.5; X.lineCap = 'round'; X.shadowColor = P.mag; X.shadowBlur = 14; X.beginPath(); X.arc(1140, 500, 290, -2.2, -2.2 + Math.PI * 2 * rc); X.stroke(); X.restore(); }
  }
  // Frühwarnung: Zustandskurve der Festplatte über 6 Wochen
  if (t > CH0) chart(t);
  X.restore();
  bpGrain();
}
function healthAt(u) { return .93 - .08 * u - .5 * Math.pow(u, 2.3) + .035 * n1(u * 14 + 3) + .02 * n1(u * 37); }
function chart(t) {
  const ox = 820, oy = 820, cw = 900, ch = 380, ax = eo(lin(t, CH0 + .02, CH0 + .3));
  X.save(); X.globalAlpha = ax;
  const axes = S('axes', () => polyP([[ox, oy - ch - 20], [ox, oy], [ox + cw + 30, oy]], false, 8), .3, false); X.save(); X.setLineDash([]); bpStroke(axes, 1, 2); X.restore();
  X.strokeStyle = hexA(P.lav, .16); X.lineWidth = 1; X.setLineDash([4, 8]); X.beginPath(); for (let i = 1; i <= 4; i++) { X.moveTo(ox, oy - i * ch / 4); X.lineTo(ox + cw, oy - i * ch / 4); } X.stroke(); X.setLineDash([]);
  X.strokeStyle = hexA(P.lav, .6); X.lineWidth = 1.5; X.beginPath(); for (let i = 0; i <= 6; i++) { X.moveTo(ox + i * cw / 6, oy); X.lineTo(ox + i * cw / 6, oy + 12); } X.stroke();
  for (let i = 0; i < 6; i++) mono('W' + (i + 1), ox + (i + .5) * cw / 6, oy + 38, 22, hexA(P.lav, .8), 'center');
  // Symbol an der y-Achse: Festplatte (Linie), statt eines Titels
  X.save(); X.translate(ox, oy - ch - 58); X.strokeStyle = P.lav; X.lineWidth = 2; X.shadowColor = P.lav; X.shadowBlur = 6; rr(X, -30, -20, 60, 40, 6); X.stroke(); X.beginPath(); X.arc(-8, 0, 12, 0, 7); X.stroke(); X.beginPath(); X.arc(-8, 0, 3, 0, 7); X.stroke(); X.beginPath(); X.moveTo(20, -12); X.lineTo(2, 4); X.stroke(); X.restore();
  X.restore();
  // Verbindung Server -> Messung, Lichtpaket läuft
  const lk = eo(lin(t, CH0 + .1, CH0 + .4)); if (lk > 0) { const lp = polySub([[590, 780], [700, 780], [700, 620], [ox - 10, 620]], 0, lk); X.save(); X.setLineDash([7, 7]); X.strokeStyle = hexA(P.lav, .6); X.lineWidth = 1.6; X.stroke(pathOf(lp)); X.restore(); nodeDot(590, 780); if (lk >= 1) { nodeDot(ox - 10, 620); const q = polyAt([[590, 780], [700, 780], [700, 620], [ox - 10, 620]], (t * .6) % 1); spark(q[0], q[1], 12, .9); } }
  dimLine(ox - 50, oy - ch, ox - 50, oy, ax * .8);
  // Kurve und Warnzeichen als Ebene (die Lupe zeigt sie vergrößert)
  const u1 = eo(lin(t, CH0 + .15, K.wochen - .45)); if (u1 <= 0) return;
  const lit = eo(lin(t, K.wochen - .3, K.wochen - .05));   // W2-Warnzeichen leuchtet auf, wenn die Lupe ankommt
  const layer = (sp) => {
    const N = 90, pts = []; for (let i = 0; i <= N * u1; i++) { const u = i / N; pts.push([ox + u * cw, oy - healthAt(u) * ch]); }
    if (pts.length > 1) { X.save(); const g = X.createLinearGradient(ox, 0, ox + cw, 0); g.addColorStop(0, P.mint); g.addColorStop(.35, P.mint); g.addColorStop(.6, P.gold); g.addColorStop(1, P.mag);
      X.strokeStyle = g; X.lineWidth = 3.4; X.shadowColor = u1 > .6 ? P.mag : P.mint; X.shadowBlur = 16; X.lineJoin = 'round'; X.stroke(pathOf(pts)); X.restore();
      if (sp && u1 < 1) { const q = pts[pts.length - 1]; spark(q[0], q[1], 22, 1); } }
    [[.25, K.zeigt - .25], [.55, K.zeigt], [.8, K.zeigt + .12]].forEach(([u, k0], wi) => { const k = back(lin(t, k0 - .05, k0 + .2)); if (k <= 0 || u1 < u - .02) return; const x = ox + u * cw, y = oy - healthAt(u) * ch - 44;
      const L = wi === 0 ? lit : 0; X.save(); X.translate(x, y); X.scale(k * (1 + .35 * L), k * (1 + .35 * L)); X.strokeStyle = L > 0 ? mixCol(P.mag, '#ffd0ea', L * .6) : P.mag; X.fillStyle = L > 0 ? `rgba(${Math.round(40 + 180 * L)},${Math.round(10 + 30 * L)},${Math.round(40 + 90 * L)},.85)` : 'rgba(40,10,40,.7)';
      X.lineWidth = 2.4; X.shadowColor = P.mag; X.shadowBlur = 10 + 26 * L; X.beginPath(); X.moveTo(0, -16); X.lineTo(15, 11); X.lineTo(-15, 11); X.closePath(); X.fill(); X.stroke(); X.shadowBlur = 0;
      X.fillStyle = '#ffd3ea'; X.fillRect(-1.4, -6, 2.8, 9); X.fillRect(-1.4, 5, 2.8, 2.8); X.restore(); });
  };
  layer(true);
  if (lit > 0) ring(ox + .25 * cw, oy - healthAt(.25) * ch - 44, t, K.wochen - .08, 20, 150, P.mag, .8, 3);
  // Lupe: fährt von W5 zurück über die Kurve und bleibt beim ersten Warnzeichen (W2) stehen – fertig kurz vor „Wochen“
  const lA = eo(lin(t, K.zeigt + .1, K.zeigt + .28)); if (lA > 0) {
    const um = mix(.8, .25, eio(lin(t, K.zeigt + .15, K.wochen - .1))), lx = ox + um * cw, ly = oy - healthAt(um) * ch - 34, LR = 96, Z = 1.8;
    X.save(); X.globalAlpha = lA; X.beginPath(); X.arc(lx, ly, LR, 0, 7); X.fillStyle = 'rgba(16,20,54,.96)'; X.fill(); X.clip();
    X.translate(lx, ly); X.scale(Z, Z); X.translate(-lx, -ly);
    X.strokeStyle = hexA(P.lav, .16); X.lineWidth = 1; X.beginPath(); for (let gx = ox; gx <= ox + cw; gx += 25) { X.moveTo(gx, oy - ch); X.lineTo(gx, oy); } for (let gy = oy; gy >= oy - ch; gy -= 25) { X.moveTo(ox, gy); X.lineTo(ox + cw, gy); } X.stroke();
    layer(false); X.restore();
    X.save(); X.globalAlpha = lA; X.strokeStyle = P.cream; X.shadowColor = P.cream; X.shadowBlur = 12; X.lineWidth = 5; X.beginPath(); X.arc(lx, ly, LR, 0, 7); X.stroke();
    X.lineWidth = 1.5; X.globalAlpha *= .6; X.beginPath(); X.arc(lx, ly, LR - 9, 0, 7); X.stroke(); X.globalAlpha = lA;
    X.lineCap = 'round'; X.lineWidth = 13; X.beginPath(); X.moveTo(lx - LR * .74, ly + LR * .74); X.lineTo(lx - LR * 1.32, ly + LR * 1.32); X.stroke();
    X.shadowBlur = 0; X.strokeStyle = 'rgba(255,255,255,.35)'; X.lineWidth = 4; X.beginPath(); X.arc(lx, ly, LR - 20, -2.6, -1.9); X.stroke(); X.restore(); }
  // Maßlinie ohne Beschriftung: vom ersten Warnzeichen bis zum Ausfall (zieht sich auf „Wochen vorher“)
  const dk = eo(lin(t, K.wochen, K.vorher + .1)); if (dk > 0) { const xa = ox + .25 * cw, xb = ox + cw, y = oy + 80, xm = mix(xa, xb, dk);
    X.save(); X.strokeStyle = P.cream; X.lineWidth = 2; X.shadowColor = P.cream; X.shadowBlur = 6; X.beginPath(); X.moveTo(xa, y - 14); X.lineTo(xa, y + 14); X.moveTo(xa, y); X.lineTo(xm, y); X.stroke(); arrowHead(xa + 2, y, Math.PI, 12, P.cream); if (dk > .98) { X.beginPath(); X.moveTo(xb, y - 14); X.lineTo(xb, y + 14); X.stroke(); arrowHead(xb - 2, y, 0, 12, P.cream); } X.restore(); }
  // Ausfall am Kurvenende: magentafarbenes Kreuz im Ring (wie „aus“ in Szene 1)
  const fk = lin(t, K.zeigt - .05, K.zeigt + .2); if (fk > 0) { const x = ox + cw; X.save(); X.globalAlpha = fk; X.setLineDash([6, 6]); X.strokeStyle = hexA(P.mag, .8); X.lineWidth = 2; X.beginPath(); X.moveTo(x, oy - ch); X.lineTo(x, oy); X.stroke(); X.restore();
    X.save(); X.shadowColor = P.mag; X.shadowBlur = 12; missX(x, oy - healthAt(1) * ch, 34, fk, t); X.restore(); tickRing(x, oy - healthAt(1) * ch, 46, fk, t * .3, P.mag); }
}

// ================= Papier: Netzwerk Nord IT wacht (mint) =================
function monitorBig(x, y, t, kind, pulse) {
  X.save(); X.translate(x, y);
  ink(S('mbst', () => polyP([[-12, 0], [12, 0], [18, 34], [-18, 34]])), '#6e6a66', 3);
  const m = S('mb', () => rrP(-92, -128, 184, 132, 12), 1); dropHatch(m, 8, 10, .4); ink(m, '#3a3f4f', 4.2);
  const sc = S('mbs', () => rrP(-80, -116, 160, 106, 6), .6); X.fillStyle = '#f7f3e8'; X.fill(sc); X.save(); X.clip(sc);
  X.strokeStyle = hexA(P.ink, .1); X.lineWidth = 1; X.beginPath(); for (let gx = -80; gx < 80; gx += 16) { X.moveTo(gx, -116); X.lineTo(gx, -10); } for (let gy = -116; gy < -10; gy += 16) { X.moveTo(-80, gy); X.lineTo(80, gy); } X.stroke();
  // Herzschlag-Linie
  X.strokeStyle = P.grass; X.lineWidth = 3.4; X.lineJoin = 'round'; X.beginPath();
  for (let i = 0; i <= 64; i++) { const gx = -80 + i * 2.5, ph = ((i * 2.5 - t * 120) % 160 + 160) % 160, v = ph > 60 && ph < 80 ? Math.sin((ph - 60) / 20 * Math.PI * 2) * -26 : 0; i ? X.lineTo(gx, -40 + v) : X.moveTo(gx, -40 + v); } X.stroke();
  X.restore();
  // Symbol oben links
  X.save(); X.translate(-56, -92); X.strokeStyle = P.ink; X.lineWidth = 2.6; X.fillStyle = kind === 0 ? P.srvF : kind === 1 ? P.sky : P.yel;
  if (kind === 0) { rr(X, -12, -16, 24, 32, 4); X.fill(); X.stroke(); X.beginPath(); X.moveTo(-8, -4); X.lineTo(8, -4); X.moveTo(-8, 6); X.lineTo(8, 6); X.stroke(); }
  else if (kind === 1) { rr(X, -16, -12, 32, 22, 3); X.fill(); X.stroke(); X.beginPath(); X.moveTo(-6, 16); X.lineTo(6, 16); X.stroke(); }
  else { X.beginPath(); X.arc(-6, 2, 9, Math.PI * .5, Math.PI * 1.5); X.arc(4, -4, 11, Math.PI * 1.1, Math.PI * 1.95); X.arc(12, 3, 7, Math.PI * 1.5, Math.PI * .5); X.closePath(); X.fill(); X.stroke(); }
  X.restore();
  X.save(); X.fillStyle = P.led; X.shadowColor = P.led; X.shadowBlur = 10; X.beginPath(); X.arc(62, -96, 8, 0, 7); X.fill(); X.restore(); X.strokeStyle = P.ink; X.lineWidth = 2; X.beginPath(); X.arc(62, -96, 8, 0, 7); X.stroke();
  X.restore();
  ring(x, y - 62, t, pulse, 40, 150, P.dash, .6, 2.5);
}
function sceneWatch(t) {
  paperBG(t, P.sMint);
  const push = lin(t, CUT.watch, CUT.swap); X.save(); cam(mix(1, 1.035, push), 960, 560);
  constr(1500, 400, 250, t * .08, .5);
  ground(900, -100, 2020, 9, 110);
  cloud(760, 330, .8, 'e');
  // Wanduhr mit Tag und Nacht
  // einmal 24 Stunden: Zeiger drehen zweimal, Sonne und Mond umrunden die Uhr einmal, der blaue Bogen schließt sich auf „Uhr“
  const day = eio(lin(t, K.ueberwacht - .1, K.uhr)), spin = 8 + 24 * day, ak = day;
  const a0 = -2.5 + day * Math.PI * 2; sun(1500 + Math.cos(a0) * 250, 400 + Math.sin(a0) * 250, 34, t, 1); moonP(1500 + Math.cos(a0 + Math.PI) * 250, 400 + Math.sin(a0 + Math.PI) * 250, 30, 1);
  wallClock(1500, 400, 170, t, spin, ak, { s: '24/7', a: eo(lin(t, K.rund - .28, K.rund - .03)) });
  // Leitstand-Tisch mit drei Monitoren
  const top = S('ctop', () => rrP(700, 730, 660, 26, 6), 1.2);
  // Leitstand als Theke mit Firmenaufdruck (einmalige Nennung der Marke, am Objekt)
  castShadow(1030, 902, 700, 20, .6);
  const cab = S('ccab2', () => rrP(716, 752, 628, 146, 6), 1.2); ink(cab, P.wood, 4); hatch(cab, P.woodD, 12, 1.1, .45, sideRegion(1200, 820, -1.2));
  X.strokeStyle = hexA(P.woodD, .7); X.lineWidth = 1.4; X.beginPath(); for (const [a1, b1, yy] of [[740, 900, 772], [960, 1320, 776], [760, 1100, 880], [1150, 1320, 884]]) { X.moveTo(a1, yy); X.lineTo(b1, yy); } X.stroke();
  const pl = S('cplate2', () => rrP(750, 784, 560, 88, 10), .8); ink(pl, '#fbf6ea', 3.4);
  X.save(); X.font = '600 58px IN'; X.letterSpacing = '-1px'; X.fillStyle = P.ink; X.textAlign = 'center'; X.textBaseline = 'middle'; X.fillText('Netzwerk Nord IT', 1030, 830); X.restore();
  X.fillStyle = P.ink; for (const [bx, by] of [[764, 798], [1296, 798], [764, 858], [1296, 858]]) { X.beginPath(); X.arc(bx, by, 3.2, 0, 7); X.fill(); }
  ink(top, P.woodL, 4.2); hatch(top, P.woodD, 12, 1.1, .45);
  pottedPlant(1440, 900, t, 1.1); hangingPlant(1060, 120, t, .85);
  const tech = [K.technik - .3, K.technik - .15, K.technik];
  [0, 1, 2].forEach(i => monitorBig(800 + i * 225, 728, t + i * .4, i, tech[i]));
  // Roboter
  robot(560, 900, 1.28, t, { look: 8, armR: -.3 + Math.sin(t * 5) * .15, armL: .9, blink: (t % 2.6) < .12 ? 1 : 0, glowAnt: true });
  X.restore();
  paperGrain();
}

// ================= Papier: Festplattentausch (gelb) =================
function sceneSwap(t) {
  paperBG(t, P.sYel);
  X.save(); cam(mix(1, 1.03, lin(t, CUT.swap + .1, CUT.night)), 1000, 600);
  constr(1300, 620, 360, -t * .06, .45);
  ground(900, -100, 2020, 13, 110);
  cloud(250, 470, .9, 'f'); cloud(1760, 300, 1, 'g');
  const kP = K.platten, kT = K.tauschen, kB = K.bevor;
  // Führungslinien der Explosionsansicht
  const gA = lin(t, kT - .1, kT + .1) * (1 - lin(t, kB + .3, kB + .6));
  if (gA > 0) { X.save(); X.globalAlpha = gA; X.setLineDash([10, 9]); X.strokeStyle = P.dash; X.lineWidth = 3; X.beginPath(); X.moveTo(1170, 738); X.lineTo(760, 738); X.moveTo(1170, 782); X.lineTo(760, 782); X.stroke(); X.setLineDash([]); X.fillStyle = P.dash; for (const [x, y] of [[1170, 738], [1170, 782], [760, 738], [760, 782]]) { X.beginPath(); X.arc(x, y, 6, 0, 7); X.fill(); } X.restore(); }
  // Schublade: schwach -> raus (tauschen) -> leer -> neu rein (bevor)
  let slot = null; const happy = t > kB - .12;
  if (t < kT - .1) slot = { i: 2, out: mix(26, 120, eo(tin(t, kP, .3))) + (t > kP ? Math.sin(t * 20) * 2 : 0) + mix(0, 90, eo(lin(t, kT - .4, kT - .1))), weak: true };
  else if (t < kT + .35) slot = { i: 2, out: 3000, weak: false };
  else slot = { i: 2, out: mix(330, 0, eio(lin(t, kT + .35, kB - .14))), weak: false };
  const ledCol = [null, null, happy ? P.led : null, null, null];
  server(1300, 900, 1, t, { mood: happy ? 'happy' : 'sick', blink: (t % 2.2) < .1 ? 1 : 0, slot, ledCol, sweat: 1 });
  if (t > kT - .1 && t < kT + .35) { X.fillStyle = '#20242f'; rr(X, 1300 - 104, 900 - 184, 208, 44, 9); X.fill(); }
  // Roboter hüpft heran, zieht die schwache Platte (tauschen), wirft sie weg, fängt die neue, schiebt sie ein (bevor)
  const hop = eo(lin(t, kP - .45, kT - .2)), rx = mix(330, 930, hop), ry = 900 - Math.abs(Math.sin(hop * Math.PI * 2)) * 60 * (1 - hop * .2);
  const holdOld = t >= kT - .1 && t < kT + .06, holdNew = t >= kT + .3 && t < kT + .42;
  const hold = () => { if (holdOld) hdd(0, -250, .9, -.1, 'old', t); if (holdNew) hdd(0, -250, .9, .05, 'new', t, { shine: 1 }); };
  const armsUp = holdOld || holdNew;
  robot(rx, ry, 1.1, t, { look: 10, armL: armsUp ? -1.3 : .9, armR: armsUp ? -1.3 : (t > kT + .42 && t < kB ? .05 : .9), hold, squash: Math.max(0, Math.sin(hop * Math.PI * 2)) * .15, blink: (t % 2.4) < .1 ? 1 : 0, mouth: t < kT + .4 ? 'o' : 'happy' });
  // alte Platte fliegt im Bogen weg und landet im Staub
  // … und fällt dort auf „ausfallen“ aus (X-Augen, Rauch) – im Server ist sie da schon nicht mehr
  const fk = lin(t, kT + .06, kT + .5), dead = t > K.ausfallen - .2; if (fk > 0) { const x = mix(930, 470, fk), y = mix(650, 858, fk) - Math.sin(fk * Math.PI) * 190; hdd(x, y, .9, fk * (Math.PI * 2 - .12), dead ? 'dead' : 'old', t);
    if (fk >= 1) for (let i = 0; i < 5; i++) { const k = lin(t, kT + .5, kT + 1.1); X.save(); X.globalAlpha = 1 - k; X.strokeStyle = P.ink2; X.lineWidth = 2; X.beginPath(); X.arc(470 + (i - 2) * 30 * (1 + k), 880 - k * 20 * hash(i), 6 + k * 8, 0, 7); X.stroke(); X.restore(); }
    if (dead) { X.save(); X.translate(470, 812); X.scale(.55, .55); smoke(0, 0, lin(t, K.ausfallen - .2, K.ausfallen + .1), t); X.restore(); ring(470, 858, t, K.ausfallen - .15, 30, 130, '#e0356f', .6, 3); } }
  // neue Platte fällt von oben in die Hände
  const nk = lin(t, kT + .02, kT + .3); if (nk > 0 && nk < 1) hdd(930, mix(-120, 650, eio(nk)), .9, .05, 'new', t, { shine: 1 });
  // neue Platte sitzt: grünes Häkchen an der Schublade (bleibt)
  { const ck = back(lin(t, kB - .3, kB - .05)); if (ck > 0) { X.save(); X.translate(1172, 738); X.scale(ck * 1.3, ck * 1.3); const c = S('chk', () => ellP(0, 0, 22, 22, 4), .5); ink(c, '#79b857', 3.2); X.strokeStyle = '#fff'; X.lineWidth = 5; X.lineCap = 'round'; X.lineJoin = 'round'; X.beginPath(); X.moveTo(-10, 1); X.lineTo(-3, 9); X.lineTo(11, -8); X.stroke(); X.restore(); } }
  // Tausch fertig: Funkeln
  if (t > kB - .15) { const k = lin(t, kB - .15, kB + .6); spark(1390, 690, 30 * (1 - k), 1 - k, '#fff'); ring(1384, 738, t, kB - .12, 20, 150, P.grass, .7, 3); }
  // Etikett „Festplatte“ zeigt auf die schwache Schublade und wandert dann mit der alten Platte mit (steht 13,5 – 15,7 s)
  { const hx = t < kT + .06 ? 930 : mix(930, 470, fk), hy = t < kT + .06 ? 625 : mix(650, 858, fk) - Math.sin(fk * Math.PI) * 190;
    const m = eo(lin(t, kT - .15, kT + .05)), tx = mix(1060, hx, m), ty = mix(560, hy - 92, m), a = tin(t, kP - .1, .25) * (1 - lin(t, K.ausfallen - .15, K.ausfallen + .1));
    if (a > 0 && m < .5) { X.save(); X.globalAlpha = a * (1 - m * 2); X.setLineDash([5, 6]); X.strokeStyle = P.ink2; X.lineWidth = 2; X.beginPath(); X.moveTo(1060, 580); X.lineTo(1300 - (slot && slot.out < 1000 ? slot.out : 0) - 110, 738); X.stroke(); X.restore(); }
    tagP('Festplatte', tx, ty, 26, a); }
  X.restore();
  paperGrain();
}

// ================= Blaupause: nächtliche Sicherung außer Haus =================
const ARC = bezP([600, 640], [760, 250], [1210, 250], [1440, 560], 80);
function house(x0, x1, yB, yT, apex, t, lit, key) {
  const p = S('hs' + key, () => polyP([[x0, yB], [x0, yT], [(x0 + x1) / 2, apex], [x1, yT], [x1, yB]]), .6);
  X.fillStyle = 'rgba(30,36,85,.55)'; X.fill(p); hatch(p, 'rgba(205,209,243,.14)', 12, 1, 1, sideRegion(x1 - 90, yB - 100, -1.2)); glow(p, P.lav, 2.2, 8);
  for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) { const wx = x0 + 50 + c * ((x1 - x0 - 100) / 2) - 30, wy = yT + 40 + r * 110; X.save(); X.strokeStyle = hexA(P.lav, .8); X.lineWidth = 1.8; X.strokeRect(wx, wy, 60, 70); X.beginPath(); X.moveTo(wx + 30, wy); X.lineTo(wx + 30, wy + 70); X.stroke();
    const l = lit ? lit(r * 3 + c) : .25; if (l > 0) { X.globalAlpha = l; X.fillStyle = P.cream; X.shadowColor = P.gold; X.shadowBlur = 16; X.fillRect(wx + 3, wy + 3, 54, 64); } X.restore(); }
}
function datacenter(x0, x1, yB, yT, t, lit) {
  const p = S('dc', () => rrP(x0, yT, x1 - x0, yB - yT, 6), .6);
  X.fillStyle = 'rgba(30,36,85,.55)'; X.fill(p); hatch(p, 'rgba(205,209,243,.14)', 12, 1, 1, sideRegion(x1 - 80, yB - 60, -1.2)); glow(p, P.lav, 2.2, 8);
  for (let r = 0; r < 6; r++) for (let c = 0; c < 4; c++) { const x = x0 + 30 + c * ((x1 - x0 - 60) / 4), y = yT + 30 + r * 58; const l = lit(r * 4 + c);
    X.save(); X.strokeStyle = hexA(P.lav, .75); X.lineWidth = 1.5; X.strokeRect(x, y, (x1 - x0 - 60) / 4 - 14, 40); X.fillStyle = l > 0 ? P.mint : hexA(P.lav, .3); X.globalAlpha = .3 + .7 * l; if (l > 0) { X.shadowColor = P.mint; X.shadowBlur = 10; } X.beginPath(); X.arc(x + (x1 - x0 - 60) / 4 - 28, y + 20, 4, 0, 7); X.fill(); X.restore(); }
  X.save(); X.strokeStyle = P.lav; X.lineWidth = 2; X.beginPath(); X.moveTo(x1 - 60, yT); X.lineTo(x1 - 60, yT - 70); X.stroke(); X.restore(); spark(x1 - 60, yT - 76, 10 + Math.sin(t * 5) * 4, .9, Math.floor(t * 2) % 2 ? '#ffd0e0' : '#fff');
}
function packet(x, y, s, lk, t) { X.save(); X.translate(x, y); X.scale(s, s); rr(X, -20, -20, 40, 40, 7); X.fillStyle = 'rgba(25,30,75,.9)'; X.fill(); X.strokeStyle = P.mint; X.lineWidth = 2; X.shadowColor = P.mint; X.shadowBlur = 10; X.stroke(); X.shadowBlur = 0;
  X.fillStyle = hexA(P.mint, .8); for (let i = 0; i < 3; i++) X.fillRect(-11, -9 + i * 7, 14 + (i % 2) * 6, 3); X.restore(); lock(x + 16 * s, y - 16 * s, .75 * s, lk); }
function sceneNight(t) {
  bpBG(t, 1000, 600, t * .04);
  X.save(); cam(mix(1, 1.05, lin(t, CUT.night, CUT.restore)), 1000, 600);
  // Sterne und Mond (Papiermond mit Korn wie die Sonne im Original)
  for (let i = 0; i < 14; i++) { const x = 250 + hash(i * 3.3) * 1500, y = 70 + hash(i * 7.1) * 260; if (x < 900 && y < 380) continue; spark(x, y, 6 + 5 * Math.abs(Math.sin(t * 2 + i)), .8); }
  const mk = eo(tin(t, K.nacht, .35)); X.save(); X.globalAlpha = mk; const g = X.createRadialGradient(1640, 180, 20, 1640, 180, 150); g.addColorStop(0, 'rgba(255,240,200,.35)'); g.addColorStop(1, 'rgba(255,240,200,0)'); X.fillStyle = g; X.fillRect(1480, 20, 320, 320);
  X.beginPath(); X.arc(1640, 180 + (1 - mk) * 40, 52, 0, 7); X.fillStyle = '#f3e8c8'; X.fill(); X.save(); X.clip(); X.globalCompositeOperation = 'multiply'; X.globalAlpha = .5; X.drawImage(GRAIN_P, 600, 400, 200, 200, 1580, 120, 120, 120); X.restore();
  X.fillStyle = 'rgba(200,190,160,.5)'; for (const [dx, dy, r] of [[-14, -10, 9], [16, 14, 6], [8, -22, 4], [-20, 20, 5]]) { X.beginPath(); X.arc(1640 + dx, 180 + dy, r, 0, 7); X.fill(); } X.restore();
  const flyS = i => K.verschl + .03 + i * .15, arrive = i => flyS(i) + .95;
  house(250, 700, 930, 610, 470, t, i => .25, 'o');
  X.save(); X.globalAlpha = 1; bpServer(475, 925, .26, t, {}); X.restore();
  datacenter(1320, 1700, 930, 560, t, i => lin(t, arrive(Math.floor(i / 5)) - .1, arrive(Math.floor(i / 5)) + .05));
  // Rechenzentrum leuchtet auf, wenn die letzte Sicherung ankommt (fertig auf „Haus“)
  const dg = eo(lin(t, K.haus - .25, K.haus)); if (dg > 0) { const dp = S('dc', () => rrP(1320, 560, 380, 370, 6), .6); X.save(); X.globalAlpha = dg; X.fillStyle = 'rgba(125,230,201,.10)'; X.fill(dp); X.restore(); glow(dp, P.mint, 3.2, 26, dg); }
  // Bogen
  const dk = eo(lin(t, CUT.night + .05, CUT.night + .4)); X.save(); X.setLineDash([10, 10]); X.lineDashOffset = -t * 40; X.strokeStyle = hexA(P.lav, .75); X.lineWidth = 2; X.stroke(pathOf(polySub(ARC, 0, dk))); X.restore();
  if (dk > .98) { const [ax, ay, aa] = polyAt(ARC, .985); arrowHead(ax, ay, aa, 14, P.lav, 2.2); }
  nodeDot(600, 640, dk); nodeDot(1440, 560, dk > .98 ? 1 : 0); tickRing(1640, 180, 80, mk * .6, t * .1, P.cream); dimLine(210, 610, 210, 930, 1); dimLine(1740, 560, 1740, 930, 1);
  // Maßlinie außer Haus
  const mk2 = eo(tin(t, K.haus, .4)); if (mk2 > 0) { X.save(); X.strokeStyle = P.cream; X.lineWidth = 2; X.shadowColor = P.cream; X.shadowBlur = 6; const y = 1030, xa = 700, xb = mix(700, 1320, mk2); X.beginPath(); X.moveTo(xa, y - 12); X.lineTo(xa, y + 12); X.moveTo(xa, y); X.lineTo(xb, y); if (mk2 > .98) { X.moveTo(1320, y - 12); X.lineTo(1320, y + 12); } X.stroke(); X.restore(); }
  // Pakete
  for (let i = 0; i < 5; i++) { const e0 = K.nacht + i * .05, s0 = flyS(i), a = arrive(i); const em = eo(lin(t, e0 - .2, e0 + .15)); if (em <= 0) continue;
    const lk = back(tin(t, K.verschl - .02 + 0 * i, .25));
    if (t < s0) { const x = 640 + i * 0 + (i - 2) * 46 * em, y = 650 - em * 40; packet(x, y, em, lk, t); if (lk > 0 && lk < 1) spark(x + 16, y - 16, 16, 1); }
    else if (t < a) { const k = eio(lin(t, s0, a)); const [x, y] = polyAt(ARC, k); packet(x, y, 1, 1, t); X.save(); const tr = polySub(ARC, Math.max(0, k - .08), k); X.strokeStyle = P.mint; X.lineWidth = 3; X.shadowColor = P.mint; X.shadowBlur = 12; X.globalAlpha = .7; X.stroke(pathOf(tr)); X.restore(); }
    else { const k = lin(t, a, a + .3); if (k < 1) spark(1440, 580, 22 * (1 - k), 1 - k); } }
  ring(1510, 740, t, K.haus - .05, 60, 300, P.mint, .8, 2.5);
  X.restore();
  bpGrain();
}

// ================= Blaupause: Notfall – in unter 1 Stunde wieder da =================
function sceneRestore(t) {
  bpBG(t, 900, 620, -t * .04);
  X.save(); cam(mix(1, 1.05, lin(t, CUT.restore, CUT.office2)), 1000, 640);
  const kN = K.notfall, kS = K.stunde, kW = K.wieder;
  const alarm = lin(t, kN - .3, kN - .05) * (1 - lin(t, kW - .25, kW)), ok = lin(t, kW - .25, kW);
  bpServer(1380, 940, .95, t, { alarm, ledCol: i => ok > .5 ? P.mint : (alarm > .5 ? (Math.floor(t * 5 + i) % 2 ? P.mag : '#5a1a45') : P.mint) });
  if (alarm > 0) { X.save(); X.shadowColor = P.mag; X.shadowBlur = 16; missX(1380, 560, 120, lin(t, kN - .3, kN) * (1 - ok), t); X.restore(); }
  ring(1380, 700, t, kN, 80, 520, P.mag, .9, 3); ring(1380, 700, t, kN + .45, 80, 520, P.mag, .9, 2);
  ring(1380, 700, t, kW, 80, 560, P.mint, .9, 3);
  if (ok > 0) { const k = lin(t, kW - .05, kW + .7); spark(1500, 470, 34 * (1 - k * .6), 1 - k * .7); X.save(); X.globalAlpha = ok; X.strokeStyle = P.mint; X.lineWidth = 6; X.shadowColor = P.mint; X.shadowBlur = 16; X.beginPath(); X.arc(1380, 560, 70, 0, 7); X.stroke(); X.beginPath(); X.moveTo(1348, 562); X.lineTo(1372, 588); X.lineTo(1414, 538); X.stroke(); X.restore(); }
  dimLine(1215, 475, 1215, 925, 1); tickRing(1380, 560, 132, alarm, t * .3, P.mag);
  // Stoppuhr
  const cx = 660, cy = 680, R = 190, sw = eo(lin(t, CUT.restore + .05, CUT.restore + .35));
  X.save(); X.globalAlpha = sw; const dial = S('sw', () => ellP(cx, cy, R, R, 5), .5); X.fillStyle = 'rgba(22,27,70,.8)'; X.fill(dial); glow(dial, P.lav, 2.6, 10);
  X.strokeStyle = hexA(P.lav, .8); X.lineWidth = 1.6; X.beginPath(); for (let i = 0; i < 60; i++) { const a = i / 60 * Math.PI * 2 - Math.PI / 2, l = i % 5 ? 8 : 18; X.moveTo(cx + Math.cos(a) * (R - 14), cy + Math.sin(a) * (R - 14)); X.lineTo(cx + Math.cos(a) * (R - 14 - l), cy + Math.sin(a) * (R - 14 - l)); } X.stroke();
  for (const [m, lab] of [[0, '60'], [15, '15'], [30, '30'], [45, '45']]) { const a = m / 60 * Math.PI * 2 - Math.PI / 2; mono(lab, cx + Math.cos(a) * (R - 58), cy + Math.sin(a) * (R - 58) + 8, 24, hexA(P.lav, .9), 'center'); }
  X.strokeStyle = P.lav; X.lineWidth = 2.4; rr(X, cx - 22, cy - R - 38, 44, 22, 5); X.stroke(); X.beginPath(); X.moveTo(cx, cy - R - 16); X.lineTo(cx, cy - R); X.stroke();
  const mins = 52 * eio(lin(t, kN + .3, kS)), a1 = -Math.PI / 2 + mins / 60 * Math.PI * 2;
  if (mins > 0) { X.strokeStyle = P.mint; X.lineWidth = 12; X.shadowColor = P.mint; X.shadowBlur = 16; X.globalAlpha = sw * .9; X.beginPath(); X.arc(cx, cy, R - 4, -Math.PI / 2, a1); X.stroke(); X.shadowBlur = 0; }
  X.globalAlpha = sw; X.strokeStyle = '#f1f2fb'; X.lineWidth = 4; X.beginPath(); X.moveTo(cx, cy); X.lineTo(cx + Math.cos(a1) * (R - 40), cy + Math.sin(a1) * (R - 40)); X.stroke(); X.fillStyle = P.salmon; X.beginPath(); X.arc(cx, cy, 9, 0, 7); X.fill();
  X.restore();
  if (mins > 0) spark(cx + Math.cos(a1) * (R - 4), cy + Math.sin(a1) * (R - 4), 18, 1);
  tickRing(cx, cy, R + 22, sw * .7, -t * .15);
  // einzige Zahl im Film: „< 60 min“ an der Stoppuhr, fertig auf „unter“ (das „<“), steht bis zum Szenenende (1,6 s)
  tagB('< 60 min', cx, cy + R + 66, 46, tin(t, K.unter, .28), P.mint);
  // Wiederherstellung: Pakete kommen aus dem Rechenzentrum zurück
  const back2 = bezP([1960, 300], [1760, 180], [1560, 260], [1450, 470], 40);
  for (let i = 0; i < 5; i++) { const s0 = kN + .35 + i * .25, e = s0 + .8; if (t < s0 || t > e + .1) continue; const k = eio(lin(t, s0, e)); const [x, y] = polyAt(back2, k); packet(x, y, 1 - lin(t, e - .1, e + .1) * .6, 1, t); }
  X.save(); X.setLineDash([10, 10]); X.lineDashOffset = t * 40; X.strokeStyle = hexA(P.lav, .5); X.lineWidth = 2; X.stroke(pathOf(back2)); X.restore();
  X.restore();
  bpGrain();
}

// Text erscheint als Ganzes aus einer Maske (nie getippt): fertig bei k1
function maskText(t, txt, x, y, size, col, k0, k1, ls = -1) {
  const k = eo(lin(t, k0, k1)); if (k <= 0) return;
  X.save(); X.font = `600 ${size}px IN`; X.letterSpacing = ls + 'px'; const w = X.measureText(txt).width;
  X.beginPath(); X.rect(x - 20, y - size * 1.05, w + 40, size * 1.35); X.clip();
  X.globalAlpha *= clamp(k * 1.6); X.fillStyle = col; X.textBaseline = 'alphabetic'; X.fillText(txt, x, y + (1 - k) * size * .9); X.restore();
}
// ================= Schluss: alles in einem Fenster (wie das Ende des Originals) =================
function sceneEnd(t) {
  bpBG(t, 960, 540, t * .05);
  X.save(); cam(mix(1, 1.04, lin(t, CUT.end, DUR)), 960, 540);
  const k = eo(lin(t, CUT.end, CUT.end + .22));
  const fx = 300, fy = 150, fw = 1320, fh = 760;
  X.save(); X.globalAlpha = k;
  const fr = S('efr', () => rrP(fx, fy, fw, fh, 22), .5); X.fillStyle = 'rgba(16,20,52,.7)'; X.fill(fr); glow(fr, P.lav, 2.4, 12);
  const fr2 = S('efr2', () => rrP(fx + 12, fy + 12, fw - 24, fh - 24, 16), .4); bpStroke(fr2, .35, 1.2);
  X.strokeStyle = hexA(P.lav, .6); X.lineWidth = 1.6; X.beginPath(); X.moveTo(fx, fy + 80); X.lineTo(fx + fw, fy + 80); X.stroke();
  for (let i = 0; i < 3; i++) { X.beginPath(); X.arc(fx + 40 + i * 28, fy + 40, 8, 0, 7); X.stroke(); }
  rr(X, fx + 160, fy + 20, 700, 40, 20); X.stroke(); lock(fx + 190, fy + 42, .6, 1, P.lav);
  // Lineale
  X.strokeStyle = hexA(P.lav, .35); X.lineWidth = 1.2; X.beginPath(); for (let x = fx; x <= fx + fw; x += 22) { X.moveTo(x, fy - 26); X.lineTo(x, (x - fx) % 110 ? fy - 32 : fy - 40); } X.moveTo(fx, fy - 26); X.lineTo(fx + fw, fy - 26);
  for (let y = fy; y <= fy + fh; y += 22) { X.moveTo(fx - 26, y); X.lineTo((y - fy) % 110 ? fx - 32 : fx - 40, y); } X.moveTo(fx - 26, fy); X.lineTo(fx - 26, fy + fh); X.stroke();
  X.restore();
  mono('netzwerk-nord-it.de', fx + 210, fy + 51, 27, hexA('#eef0ff', k));
  // Funkeln wandert am Rahmen entlang
  const rim = rrP(fx, fy, fw, fh, 22, 20); for (let i = 0; i < 2; i++) { const q = polyAt(rim, ((t - CUT.end) * .12 + i * .5) % 1); spark(q[0], q[1], 16, k); }
  // Name: als Ganzes aus einer Maske von unten, fertig auf „Netzwerk“
  maskText(t, 'Netzwerk Nord IT', fx + 110, fy + 250, 104, '#f4f5ff', K.ende - .24, K.ende - .02, -2);
  // „IT-Check“ fertig auf „IT-Check“, „kostenlos“ landet als Stempel auf „kostenlos“
  maskText(t, 'IT-Check', fx + 110, fy + 400, 84, '#f4f5ff', K.check - .3, K.check);
  X.save(); X.font = '600 84px IN'; X.letterSpacing = '-1px'; const kx = fx + 110 + X.measureText('IT-Check ').width, kw = X.measureText('kostenlos').width; X.restore();
  const sk = lin(t, K.kostenlos - .28, K.kostenlos - .04);
  if (sk > 0) { const sc = mix(1.45, 1, e4(sk)); X.save(); X.globalAlpha = clamp(sk * 2.2); X.translate(kx + kw / 2, fy + 372); X.scale(sc, sc); X.font = '600 84px IN'; X.letterSpacing = '-1px'; X.fillStyle = P.mint; X.textAlign = 'center'; X.textBaseline = 'alphabetic'; X.shadowColor = P.mint; X.shadowBlur = 14 * (1 - sk) + 4; X.fillText('kostenlos', 0, 28); X.restore(); }
  const uk = eo(lin(t, K.kostenlos - .14, K.kostenlos + .06)); if (uk > 0) { X.fillStyle = P.cream; rr(X, kx - 2, fy + 400 + 17, (kw + 4) * uk, 9, 3); X.fill(); }
  ring(kx + kw / 2, fy + 372, t, K.kostenlos - .04, 60, 320, P.mint, .7, 2.5);
  mono('040 318 27 60', fx + 114, fy + 540, 34, hexA('#eef0ff', .85 * lin(t, K.kostenlos + .35, K.kostenlos + .7)));
  // Logo (Roboter) baut sich als Blaupausen-Linie auf
  bpRobot(fx + fw - 250, fy + fh - 150, 1.9, t, { wave: true, tilt: Math.sin(t * 2) * .05, draw: lin(t, CUT.end, CUT.end + .7) });
  ring(fx + fw - 250, fy + fh - 250, t, CUT.end + .68, 60, 240, P.mint, .8);
  X.restore();
  bpGrain();
}

// ================= Ablauf =================
function frame(t) {
  X.setTransform(1, 0, 0, 1, 0, 0); X.globalAlpha = 1; X.globalCompositeOperation = 'source-over';
  if (t < CUT.loss) sceneOffice(t, false);
  else if (t < CUT.watch) sceneLoss(t);
  else if (t < CUT.swap) sceneWatch(t);
  else if (t < CUT.night) sceneSwap(t);
  else if (t < CUT.restore) sceneNight(t);
  else if (t < CUT.office2) sceneRestore(t);
  else if (t < CUT.end) sceneOffice(t, true);
  else sceneEnd(t);
}
