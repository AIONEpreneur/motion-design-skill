// Fachwerk-Altbau als 3D-Linienmodell (Meter). Giebelseite = Fassade in der Ebene z = 0, Tiefe nach +z.
const HW = 5, HD = 8, EAVE = 6.4, RIDGE = 10.4;
// Hölzer der Fassade: [u1, v1, u2, v2, Breite, id]; id 'e…' = wird ersetzt
const TIMBER = [
  [-5.1, .3, 5.1, .3, .34, 'eS'],                     // Schwelle (links nass → ersetzt)
  [-4.87, .3, -4.87, 3.3, .3, 'eP1'], [-2.6, .3, -2.6, 3.3, .26, 'p2'], [0, .3, 0, 3.3, .26, 'p3'], [2.6, .3, 2.6, 3.3, .26, 'p4'], [4.87, .3, 4.87, 3.3, .3, 'p5'],
  [-5.1, 3.3, 5.1, 3.3, .36, 'r1'],
  [-4.87, 3.3, -4.87, 6.3, .3, 'q1'], [-2.6, 3.3, -2.6, 6.3, .26, 'q2'], [0, 3.3, 0, 6.3, .26, 'q3'], [2.6, 3.3, 2.6, 6.3, .26, 'q4'], [4.87, 3.3, 4.87, 6.3, .3, 'q5'],
  [-5.1, 6.3, 5.1, 6.3, .34, 'r2'],
  [-4.72, .45, -2.75, 2.3, .22, 'eB1'], [4.72, .45, 2.75, 2.3, .22, 'b2'],       // Streben unten
  [-4.72, 3.45, -2.75, 5.3, .22, 'b3'], [4.72, 3.45, 2.75, 5.3, .22, 'eB4'],      // Streben oben
  [-2.6, 1.0, 0, 1.0, .18, 'br1'], [0, 4.0, 2.6, 4.0, .18, 'br2'],               // Brüstungsriegel
  [-2.6, 5.7, 0, 5.7, .18, 'sr1'], [0, 5.7, 2.6, 5.7, .18, 'sr2'],
  [-5.3, 6.2, 0, RIDGE, .34, 'ra1'], [5.3, 6.2, 0, RIDGE, .34, 'ra2'],            // Ortgang
  [-2.2, 8.1, 2.2, 8.1, .26, 'kb'], [0, 6.3, 0, RIDGE - .3, .26, 'kp'], [-1.6, 6.3, -1.6, 8.1, .22, 'g1'], [1.6, 6.3, 1.6, 8.1, .22, 'g2']
];
const WINS = [[-2.2, 1.25, -.45, 2.85], [.45, 1.25, 2.2, 2.85], [-2.2, 3.95, -.45, 5.55], [.45, 3.95, 2.2, 5.55], [-.55, 8.45, .55, 9.35]];
const STAIN = [-3.9, 1.35];   // Mittelpunkt des Flecks (Fassadenkoordinaten)
function fp(u, v, z = 0) { return [u, v, z]; }
function timberQuad(tb, dz = 0, dv = 0) { const [u1, v1, u2, v2, w] = tb, L = Math.hypot(u2 - u1, v2 - v1), nx = -(v2 - v1) / L * w / 2, ny = (u2 - u1) / L * w / 2;
  return [fp(u1 + nx, v1 + ny + dv, dz), fp(u2 + nx, v2 + ny + dv, dz), fp(u2 - nx, v2 - ny + dv, dz), fp(u1 - nx, v1 - ny + dv, dz)]; }
const FACADE = [[-HW, -.1], [HW, -.1], [HW, EAVE], [0, RIDGE], [-HW, EAVE]];
// Fleck als organische Form in Fassadenkoordinaten
function stainPts(r, seed = 3) { const pts = []; for (let i = 0; i < 48; i++) { const a = i / 48 * Math.PI * 2, rr = r * (1 + .28 * n1(seed + Math.cos(a) * 2 + 7) + .14 * Math.sin(a * 5 + seed)); pts.push(fp(STAIN[0] + Math.cos(a) * rr, STAIN[1] + Math.sin(a) * rr * 1.25)); } return pts; }

// o: {plan: {bleibt 0..1, ersetzt 0..1, lift}, stain r, paint k, crack k, sag k, lit 0..1, rainA}
function house3(t, o = {}) {
  const gold = DARK > 0, lc0 = o.lineCol || null, lc = o.rot > 10 ? mixCol(lc0 || P.cream, '#ff5a3c', clamp((o.rot - 10) / 2.5)) : lc0;
  // Seitenwand (x = +HW) und Dach
  const side = poly3([[HW, -.1, 0], [HW, -.1, HD], [HW, EAVE, HD], [HW, EAVE, 0]]);
  if (!gold) { X.fillStyle = 'rgba(150,125,90,.35)'; X.fill(side); hatchPath(side, P.ink2, 6, 1, .6, 1); }
  else { X.fillStyle = 'rgba(40,28,14,.6)'; X.fill(side); hatchPath(side, hexA(o.lc2 || P.gold, .25), 7, 1, 1, 1); }
  stroke(side, 2.4, lc);
  for (let i = 1; i < 6; i++) stroke(seg3([HW, EAVE * i / 6, 0], [HW, EAVE * i / 6, HD]), 1, gold ? hexA(lc || P.gold, .35) : 'rgba(40,25,10,.35)', 4);
  const roofR = poly3([[0, RIDGE, -.4], [0, RIDGE, HD + .4], [HW + .4, EAVE - .3, HD + .4], [HW + .4, EAVE - .3, -.4]]);
  if (!gold) { X.fillStyle = 'rgba(160,80,50,.55)'; X.fill(roofR); } else { X.fillStyle = 'rgba(30,20,10,.7)'; X.fill(roofR); }
  for (let i = 1; i < 12; i++) { const k = i / 12; stroke(seg3([k * (HW + .4), mix(RIDGE, EAVE - .3, k), -.4], [k * (HW + .4), mix(RIDGE, EAVE - .3, k), HD + .4]), 1.3, gold ? hexA(lc || P.gold, .5) : 'rgba(30,15,8,.7)', 4); }
  stroke(roofR, 2.6, lc);
  // Schornstein
  const ch = poly3([[1.6, RIDGE - 1.2, 3], [2.4, RIDGE - 2, 3], [2.4, RIDGE + 1.2, 3], [1.6, RIDGE + 1.2, 3]]); if (!gold) { X.fillStyle = '#a4553d'; X.fill(ch); hatchPath(ch, P.ink2, 6, 1, .5); } stroke(ch, 2.2, lc);
  // Fassade: Putz
  const fac = poly3(FACADE.map(q => fp(q[0], q[1])));
  if (!gold) { X.fillStyle = 'rgba(245,234,212,.45)'; X.fill(fac); } else { X.fillStyle = 'rgba(20,14,8,.55)'; X.fill(fac); }
  // Fleck
  if (o.stain > 0) { const sp = poly3(stainPts(o.stain)); X.save(); X.clip(fac);
    const c = prj(fp(STAIN[0], STAIN[1])); const g = X.createRadialGradient(c[0], c[1], 0, c[0], c[1], o.stain * CAM.f / c[2] * 1.4);
    g.addColorStop(0, gold ? 'rgba(90,120,90,.5)' : 'rgba(88,92,60,.75)'); g.addColorStop(.7, gold ? 'rgba(60,80,60,.35)' : 'rgba(110,98,62,.55)'); g.addColorStop(1, 'rgba(120,100,60,.25)');
    X.fillStyle = g; X.fill(sp); X.strokeStyle = gold ? 'rgba(150,170,130,.6)' : 'rgba(70,58,32,.8)'; X.lineWidth = 2; X.stroke(sp);
    // Ränder wie Wasserflecken
    for (const f of [.72, .5]) { const sp2 = poly3(stainPts(o.stain * f, 5 + f * 10)); X.strokeStyle = gold ? 'rgba(150,170,130,.35)' : 'rgba(70,58,32,.45)'; X.lineWidth = 1.4; X.stroke(sp2); }
    // Schimmelpunkte
    if (o.mold > 0) for (let i = 0; i < 70; i++) { const a = hash(i * 3.7) * 6.28, r = Math.sqrt(hash(i * 1.9)) * o.stain * .9, k = clamp((o.mold * 1.3 - hash(i * 5.1) * .6)); if (k <= 0) continue; const q = prj(fp(STAIN[0] + Math.cos(a) * r, STAIN[1] + Math.sin(a) * r * 1.2)); X.fillStyle = 'rgba(30,36,24,.8)'; X.beginPath(); X.arc(q[0], q[1], (1.5 + hash(i) * 3.5) * k * CAM.f / q[2] / 60, 0, 7); X.fill(); }
    X.restore(); }
  // Frische Farbe (drübergestrichen)
  if (o.paint > 0) { X.save(); X.clip(fac); const pb = poly3([fp(-4.75, .45), fp(-4.75 + 2.0, .45), fp(-4.75 + 2.0, mix(.45, 3.15, o.paint)), fp(-4.75, mix(.45, 3.15, o.paint))]); X.fillStyle = '#f1e8d4'; X.fill(pb);
    X.strokeStyle = 'rgba(120,100,70,.25)'; X.lineWidth = 1; for (let i = 0; i < 8; i++) stroke(seg3(fp(-4.7 + i * .25, .45), fp(-4.7 + i * .25, mix(.45, 3.15, o.paint))), 1, 'rgba(150,130,100,.25)');
    if (o.bleed > 0) { X.save(); X.clip(pb); X.globalAlpha = o.bleed; const sp = poly3(stainPts(o.stain * mix(.6, 1.05, o.bleed), 11)); X.fillStyle = 'rgba(96,92,58,.7)'; X.fill(sp); X.strokeStyle = 'rgba(70,58,32,.8)'; X.lineWidth = 2; X.stroke(sp); X.restore(); }
    X.restore(); }
  // Risse
  if (o.crack > 0) { const cr = [[-1.4, 3.1], [-1.1, 2.6], [-1.3, 2.2], [-.9, 1.7], [-1.05, 1.3]]; const sub = polySub(cr, 0, o.crack); if (sub.length > 1) stroke(pathOf(sub.map(q => prj(fp(q[0], q[1])))), 2.2, gold ? '#ff6a4a' : P.red, 12); }
  // Fenster und Tür
  WINS.forEach((w, i) => { const q = poly3([fp(w[0], w[1]), fp(w[2], w[1]), fp(w[2], w[3]), fp(w[0], w[3])]);
    if (o.lit > 0 && gold) { X.save(); X.globalAlpha = o.lit; X.shadowColor = '#ffcf6a'; X.shadowBlur = 30; X.fillStyle = 'rgba(255,200,110,.75)'; X.fill(q); X.restore(); }
    else if (!gold) { X.fillStyle = 'rgba(70,70,70,.16)'; X.fill(q); hatchPath(q, '#2c2a26', 6, 1, .55, -1); }
    stroke(q, 2.4, lc); const mu = (w[0] + w[2]) / 2, mv = (w[1] + w[3]) / 2; stroke(seg3(fp(mu, w[1]), fp(mu, w[3])), 2, lc); stroke(seg3(fp(w[0], mv), fp(w[2], mv)), 2, lc); });
  // Hölzer
  const pl = o.plan || {};
  const rotCol = (u, v) => { if (!(o.rot > 0)) return lc; const dd = Math.hypot(u - STAIN[0], v - STAIN[1]), k = clamp((o.rot - dd) / 1.2); return k > 0 ? mixCol(lc || P.cream, '#ff5a3c', k) : lc; };
  TIMBER.forEach(tb => { const ers = tb[5][0] === 'e'; const lift = ers ? (pl.lift || 0) : 0; const q = poly3(timberQuad(tb, -lift * .8, 0));
    let fill = gold ? null : 'rgba(176,132,80,.55)';
    if (!gold && pl.bleibt > 0 && !ers) fill = hexA(mixCol('#b08450', '#d0a238', pl.bleibt), mix(.55, .9, pl.bleibt));
    if (!gold && pl.ersetzt > 0 && ers) fill = hexA(mixCol('#b08450', '#c8563c', pl.ersetzt), mix(.55, .9, pl.ersetzt));
    if (o.newWood && ers) fill = 'rgba(214,176,112,.9)';
    if (fill) { X.fillStyle = fill; X.fill(q); }
    if (!gold) { X.save(); X.clip(q); X.globalAlpha = .45; X.strokeStyle = P.woodD; X.lineWidth = 1; const [u1, v1, u2, v2, w] = tb; for (let j = -1; j <= 1; j++) { const off = j * w * .28; const L = Math.hypot(u2 - u1, v2 - v1), nx = -(v2 - v1) / L * off, ny = (u2 - u1) / L * off; X.stroke(seg3(fp(u1 + nx, v1 + ny), fp(u2 + nx, v2 + ny))); } X.restore(); }
    if (!gold && ers && pl.ersetzt > 0) { hatchPath(q, '#5a1a0e', 5, 1.2, pl.ersetzt * .8, -1); X.save(); X.setLineDash([10, 7]); stroke(q, 2.4, P.red); X.restore(); }
    else stroke(q, o.rot > 0 ? 2.8 : 2.4, rotCol((tb[0] + tb[2]) / 2, (tb[1] + tb[3]) / 2), o.rot > 0 ? 16 : 12);
    if (o.pegs && !gold) { const [u1, v1, u2, v2] = tb; for (const kk of [.08, .92]) { const c = prj(fp(mix(u1, u2, kk), mix(v1, v2, kk))); X.fillStyle = '#5a3a20'; X.beginPath(); X.arc(c[0], c[1], 3.6 * CAM.f / c[2] / 50, 0, 7); X.fill(); } } });
  // Sockel aus Bruchstein
  const pk = poly3([fp(-HW - .2, -.7), fp(HW + .2, -.7), fp(HW + .2, .12), fp(-HW - .2, .12)]); if (!gold) { X.fillStyle = '#a79a86'; X.fill(pk); } stroke(pk, 2.4, lc);
  for (let i = 0; i < 14; i++) { const u = -HW + .35 + i * .72, v = -.3 + (i % 2) * .12; const st = poly3([fp(u - .3, v - .22), fp(u + .3, v - .22), fp(u + .3, v + .2), fp(u - .3, v + .2)]); if (!gold) hatchPath(st, P.ink2, 5, 1, .45); stroke(st, 1.4, gold ? hexA(lc || P.gold, .6) : null, 4); }
  const sideP = poly3([[HW + .2, -.7, 0], [HW + .2, -.7, HD], [HW + .2, .12, HD], [HW + .2, .12, 0]]); if (!gold) { X.fillStyle = '#8c806d'; X.fill(sideP); hatchPath(sideP, P.ink2, 5, 1, .6); } stroke(sideP, 2, lc);
  stroke(fac, 3, lc);
}
function groundLine(y0 = -.7) { const a = prj([0, y0, 0]); const p = new Path2D(); p.moveTo(-100, a[1]); p.lineTo(2100, a[1]); stroke(p, 2.4);
  if (!DARK) { X.save(); X.strokeStyle = 'rgba(40,25,10,.5)'; X.lineWidth = 1.3; X.beginPath(); for (let x = -40; x < 2000; x += 14) { X.moveTo(x, a[1] + 28); X.lineTo(x + 24, a[1] + 2); } X.stroke(); X.restore(); } }
