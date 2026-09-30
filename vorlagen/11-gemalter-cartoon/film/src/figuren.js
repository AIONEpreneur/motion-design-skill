// figuren.js (V5 Zahnfee): das Kind, der Backenzahn und die Requisiten – gemalt mit denselben Werkzeugen
// wie Researcher und Clawd (paint = Lasur + Aquarell + Tuschekontur, inkLine, boilende Linien).

// ---------- das Kind (Mia) ----------
// (x, y) = Bodenpunkt zwischen den Füßen, s = Einheit (Höhe ≈ 10,4 s). Optionen wie researcher():
// eyes ('dot','wide','star','closed','sad','heart','x','look'), lookX, brows, mouth ('smile','grin','o','O','wobble','flat','cry'),
// aL/aR (Armwinkel, 0 = waagrecht, + = hoch), dy/sq/rot/flip, walk, kick, tears (0..1), blush, emote/emoteK, handL/handR.
const KID = { skin: '#F2C4A0', hair: '#6B3F2A', shirt: '#E8AA38', shirtDk: '#B9772A', pants: '#3A9C98', ribbon: '#E27A92' };
function child(x, y, s, o = {}) {
  const sw = clamp(s / 13, .45, 2.2), J = s * .05, sq = (o.sq || 0) + (o.take || 0);
  if (!o.noShadow) paint(ellPts(x, y + s * .1, s * 2.6, s * .55, 18), { fill: PAL.ink, fillOp: 80, bleed: .2, tex: .3, border: .1, ink: null });
  push(); translate(x, y + (o.dy || 0) * s); if (o.rot) rotate(o.rot); scale((o.flip ? -1 : 1) * (1 + sq * .5), 1 - sq);
  // Beine
  [-1, 1].forEach((side, i) => {
    let h = 2.0, a = 0;
    if (o.walk != null) { const ph = Math.sin((o.walk + (i ? .5 : 0)) * TAU); if (ph > 0) h -= ph * .7; a = Math.sin((o.walk + (i ? .5 : 0)) * TAU) * .25; }
    if (o.kick) a = Math.sin(T * 18 + i * 2) * .5 * o.kick;
    push(); translate(side * .7 * s, -2.0 * s); rotate(a);
    paint(rectPts(-.42 * s, 0, .84 * s, h * s, J), { wash: KID.pants, fill: PAL.indigo, fillOp: 40, tex: .5, ink: PAL.ink, sw: sw * .7 });
    paint(ellPts(side * .15 * s, h * s, .68 * s, .34 * s, 12), { wash: '#C8324A', fill: PAL.ink, fillOp: 40, ink: PAL.ink, sw: sw * .5 });
    pop();
  });
  // Arme
  const arm = (side, a, hook) => {
    push(); translate(side * 1.35 * s, -4.6 * s); rotate(side < 0 ? a : -a);
    paint(rectPts(side < 0 ? -2.3 * s : 0, -.38 * s, 2.3 * s, .76 * s, J), { wash: KID.shirt, fill: KID.shirtDk, fillOp: 50, tex: .5, ink: PAL.ink, sw: sw * .7 });
    translate(side * 2.45 * s, 0);
    paint(ellPts(0, 0, .48 * s, .48 * s, 12), { wash: KID.skin, ink: PAL.ink, sw: sw * .6 });
    if (hook) { if (side < 0) scale(-1, 1); hook(s, sw); }
    pop();
  };
  arm(-1, o.aL ?? -1.2, o.handL); arm(1, o.aR ?? -1.2, o.handR);
  // Kleidchen / Pulli
  const body = [[-1.45 * s, -5.1 * s], [1.45 * s, -5.1 * s], [1.95 * s, -1.9 * s], [-1.95 * s, -1.9 * s]];
  paint(body, { wash: KID.shirt, fill: KID.shirtDk, fillOp: 70, bleed: .08, tex: .7, border: .6, ink: null });
  paint(ellPts(-.6 * s, -4.2 * s, .9 * s, .5 * s, 12), { fill: '#FFF1C8', fillOp: 70, bleed: .2, ink: null });
  inkLine([[-1.8 * s, -2.5 * s], [1.8 * s, -2.5 * s]], sw * .5, KID.shirtDk, 'inkfine', 0);
  paint(starPts(.55 * s, -3.6 * s, .42 * s, .45, 5), { wash: PAL.cream, ink: PAL.ink, sw: sw * .35 });
  paint(body, { ink: PAL.ink, sw: sw * .9 });
  // Kopf
  const hy = -7.6 * s, R = 2.45 * s;
  paint(rectPts(-.4 * s, -5.6 * s, .8 * s, .7 * s), { wash: KID.skin, ink: null });
  // Zöpfe hinter dem Kopf
  for (const side of [-1, 1]) {
    const sw2 = Math.sin(T * 5 + side) * .12 * (o.kick ? 2 : 1);
    push(); translate(side * 2.3 * s, hy - .3 * s); rotate(side * (.5 + sw2));
    paint(ellPts(side * .7 * s, .6 * s, .85 * s, 1.25 * s, 16, J * .6), { wash: KID.hair, fill: PAL.violet, fillOp: 35, tex: .6, ink: PAL.ink, sw: sw * .6 });
    paint(ellPts(0, -.3 * s, .45 * s, .3 * s, 10), { wash: KID.ribbon, ink: PAL.ink, sw: sw * .4 });
    pop();
  }
  paint(ellPts(0, hy, R, R * .96, 26, J * .6), { wash: KID.skin, fill: '#E9A98A', fillOp: 45, tex: .6, border: .5, ink: PAL.ink, sw: sw * .85 });
  const hp = []; for (let i = 0; i <= 12; i++) { const a = Math.PI * 1.02 + i / 12 * Math.PI * .96; hp.push([Math.cos(a) * R * 1.07, hy + Math.sin(a) * R * 1.07]); }
  hp.push([1.9 * s, hy - .9 * s], [1.0 * s, hy - 1.5 * s], [.2 * s, hy - 1.0 * s], [-.6 * s, hy - 1.55 * s], [-1.5 * s, hy - 1.0 * s], [-2.3 * s, hy - .5 * s]);
  paint(hp, { wash: KID.hair, fill: PAL.violet, fillOp: 35, tex: .6, ink: PAL.ink, sw: sw * .7 });
  // Gesicht
  const e = (o.squint || 0) > .5 ? 'closed' : (o.eyes || 'dot'), blink = e === 'dot' && ((T * .8 + .4) % 3.1) < .12;
  const ey = hy + .15 * s, lx = (o.lookX || 0) * .3 * s, ly = (o.lookY || 0) * .2 * s;
  if (o.blush !== false) for (const bx of [-1.55, 1.55]) paint(ellPts(bx * s, hy + 1.0 * s, .5 * s, .28 * s, 12), { fill: PAL.rose, fillOp: 150, bleed: .2, ink: null });
  for (const side of [-1, 1]) {
    const cx = side * .95 * s;
    if (e === 'dot' || e === 'look' || e === 'sad') {
      if (blink) inkLine([[cx - .3 * s, ey], [cx + .3 * s, ey]], sw * .8, PAL.ink, 'ink', 0);
      else { paint(ellPts(cx + lx, ey + ly, .27 * s, .34 * s, 10), { wash: PAL.ink, ink: null }); paint(ellPts(cx + lx + .09 * s, ey + ly - .12 * s, .08 * s, .09 * s, 8), { wash: PAL.cream, ink: null }); }
    } else if (e === 'wide') {
      paint(ellPts(cx, ey, .62 * s, .7 * s, 16), { wash: PAL.cream, ink: PAL.ink, sw: sw * .5 });
      paint(ellPts(cx + lx * .6, ey + ly, .26 * s, .3 * s, 10), { wash: PAL.ink, ink: null });
    } else if (e === 'star') paint(starPts(cx, ey, .62 * s * (1 + .15 * Math.sin(T * 13 + side))), { wash: PAL.cream, fill: PAL.ochre, fillOp: 90, ink: PAL.ink, sw: sw * .4 });
    else if (e === 'closed') inkLine([[cx - .38 * s, ey + .12 * s], [cx, ey - .25 * s], [cx + .38 * s, ey + .12 * s]], sw * .85, PAL.ink, 'ink', .4);
    else if (e === 'shut') inkLine([[cx - .38 * s, ey - .05 * s], [cx, ey + .18 * s], [cx + .38 * s, ey - .05 * s]], sw * .85, PAL.ink, 'ink', .4);
    else if (e === 'heart') paint(heartPts(cx, ey, .5 * s), { wash: '#E2476E', ink: PAL.ink, sw: sw * .35 });
    else if (e === 'x') { inkLine([[cx - .3 * s, ey - .3 * s], [cx + .3 * s, ey + .3 * s]], sw * .7, PAL.ink, 'ink', 0); inkLine([[cx + .3 * s, ey - .3 * s], [cx - .3 * s, ey + .3 * s]], sw * .7, PAL.ink, 'ink', 0); }
  }
  const b = o.brows || (e === 'sad' || e === 'wide' && o.scared ? 'worried' : null);
  if (b) for (const side of [-1, 1]) { const tilt = b === 'worried' ? -side * .3 : b === 'angry' ? side * .35 : 0, lift = b === 'up' ? -.3 * s : 0, bx = side * .95 * s, by = hy - .85 * s;
    inkLine([[bx - .4 * s, by + lift + tilt * s * .6], [bx + .4 * s, by + lift - tilt * s * .6]], sw * .8, KID.hair, 'ink', 0); }
  const m = o.mouth || 'smile', my = hy + 1.35 * s;
  if (m === 'smile') inkLine([[-.5 * s, my - .1 * s], [0, my + .25 * s], [.5 * s, my - .1 * s]], sw * .7, PAL.ink, 'ink', .6);
  else if (m === 'o') paint(ellPts(0, my + .1 * s, .26 * s, .32 * s, 10), { wash: '#6A2A35', ink: PAL.ink, sw: sw * .4 });
  else if (m === 'O') paint(ellPts(0, my + .25 * s, .55 * s, .68 * s, 14), { wash: '#6A2A35', ink: PAL.ink, sw: sw * .5 });
  else if (m === 'cry') { paint([[-.8 * s, my - .1 * s], [.8 * s, my - .1 * s], [.55 * s, my + .75 * s], [-.55 * s, my + .75 * s]], { wash: '#6A2A35', ink: PAL.ink, sw: sw * .5, curv: .5 }); paint(ellPts(0, my + .55 * s, .35 * s, .16 * s, 10), { wash: PAL.rose, ink: null }); }
  else if (m === 'wobble') inkLine([[-.65 * s, my], [-.32 * s, my - .16 * s], [0, my], [.32 * s, my - .16 * s], [.65 * s, my]], sw * .6, PAL.ink, 'ink', .3);
  else if (m === 'flat') inkLine([[-.4 * s, my], [.4 * s, my]], sw * .7, PAL.ink, 'ink', 0);
  else if (m === 'grin') { paint([[-.8 * s, my - .15 * s], [.8 * s, my - .15 * s], [.5 * s, my + .5 * s], [-.5 * s, my + .5 * s]], { wash: '#6A2A35', ink: PAL.ink, sw: sw * .5, curv: .4 }); paint(rectPts(-.45 * s, my - .13 * s, .9 * s, .22 * s), { wash: PAL.cream, ink: null }); }
  if (o.tears) for (const side of [-1, 1]) for (let k = 0; k < 2; k++) {
    const ph = frac(T * 1.6 + k * .5 + side * .25), dx = side * (1.2 + ph * 1.4) * s, dy = ey + (.3 + ph * ph * 3.2) * s;
    paint([[dx, dy - .35 * s], [dx + .2 * s, dy + .05 * s], [dx, dy + .22 * s], [dx - .2 * s, dy + .05 * s]], { wash: PAL.sky, fill: '#FFFFFF', fillOp: 70, ink: PAL.ink, sw: sw * .35, curv: .7 });
  }
  pop();
  if (o.emote) emote(o.emote, x + (o.flip ? -1 : 1) * 2.8 * s, y + (o.dy || 0) * s - 10.6 * s, s * 1.1, o.emoteK ?? 1);
}

// ---------- der Backenzahn (Clawd als Zahn: gleiche Blockfigur, Wurzeln statt Beine) ----------
const ZAHN = { col: '#F4EEDF', dk: '#D6C9AE', lt: '#FFFFFF' };
function tooth(x, y, u, o = {}) {
  const J = u * .07, sw = clamp(u / 15, .45, 2.4);
  if (o.throb) paint(ellPts(x, y - 5 * u, u * (7.5 + 1.2 * o.throb), u * (5.6 + 1 * o.throb), 26), { fill: '#E0283F', fillOp: 110 * o.throb, bleed: .35, tex: .3, border: .1, ink: null });
  if (!o.noShadow) paint(ellPts(x, y + u * .15, u * 5.4, u * .9, 22), { fill: PAL.ink, fillOp: 90, bleed: .25, tex: .3, border: .1, ink: null });
  // Wurzeln (Beine)
  push(); translate(x, y + (o.dy || 0) * u); if (o.rot) rotate(o.rot); scale(1 + (o.sq || 0) * .6, 1 - (o.sq || 0));
  [-1, 1].forEach((side, i) => {
    let lift = 0; if (o.walk != null) { const ph = Math.sin((o.walk + (i ? .5 : 0)) * TAU); if (ph > 0) lift = ph * .7; }
    const r = [[side * 3.9 * u, -2.6 * u], [side * 1.2 * u, -2.6 * u], [side * 1.6 * u, (-.2 - lift) * u], [side * 2.9 * u, (-.05 - lift) * u]];
    paint(r, { wash: ZAHN.dk, fill: '#B8A888', fillOp: 70, tex: .6, ink: PAL.ink, sw: sw * .8, curv: .35 });
  });
  pop();
  const dr = (u2, sw2) => {
    // Höcker oben
    for (const bx of [-2.6, 2.6]) {
      const arc = []; for (let i = 0; i <= 10; i++) { const a = Math.PI + i / 10 * Math.PI; arc.push([bx * u + Math.cos(a) * 2.3 * u, -7.85 * u + Math.sin(a) * 1.0 * u]); }
      paint([...arc, [bx * u + 2.3 * u, -7.6 * u], [bx * u - 2.3 * u, -7.6 * u]], { wash: ZAHN.col, ink: null });
      inkLine(arc, sw2, PAL.ink, 'ink', .4);
    }
    const h = clamp(o.hole || 0), f = clamp(o.filled || 0);
    if (h > .02) {
      const hx = 2.9 * u, hy = -3.6 * u;
      paint(ellPts(hx, hy, (.5 + 1.1 * h) * u, (.4 + .85 * h) * u, 16, J * .5), { wash: '#6B4430', fill: '#3A2218', fillOp: 150, tex: .6, ink: PAL.ink, sw: sw2 * .6 });
      if (h > .6) paint(ellPts(hx - .2 * u, hy + .1 * u, (.3 + .5 * h) * u, (.25 + .4 * h) * u, 12), { wash: '#2A150E', ink: null });
      if (h > .82) { inkLine([[hx - 1.2 * u, hy - .6 * u], [hx - 2.2 * u, hy - 1.6 * u], [hx - 2.6 * u, hy - 1.4 * u]], sw2 * .6, PAL.ink, 'inkfine', 0); inkLine([[hx + .4 * u, hy + 1 * u], [hx + .9 * u, hy + 2 * u]], sw2 * .6, PAL.ink, 'inkfine', 0); }
      if (f > .02) { paint(ellPts(hx, hy, (.5 + 1.1 * h) * u * (.3 + .75 * f), (.4 + .85 * h) * u * (.3 + .75 * f), 16), { wash: '#FFFDF4', fill: PAL.sky, fillOp: 40, ink: null }); if (f > .9) paint(starPts(hx + .6 * u, hy - .6 * u, .9 * u), { wash: PAL.cream, fill: PAL.ochre, fillOp: 60, ink: PAL.ink, sw: sw2 * .4 }); }
    }
    if (o.scarf) { // Tuch gegen Zahnweh, oben geknotet
      paint([[-5.3 * u, -3.4 * u], [5.3 * u, -3.4 * u], [5.1 * u, -2.2 * u], [-5.1 * u, -2.2 * u]], { wash: '#F6EFE6', fill: PAL.rose, fillOp: 50, tex: .6, ink: PAL.ink, sw: sw2 * .6 });
      paint([[-.6 * u, -8.2 * u], [-2.2 * u, -10.2 * u], [-.2 * u, -9.4 * u], [.2 * u, -9.4 * u], [2.2 * u, -10.2 * u], [.6 * u, -8.2 * u]], { wash: '#F6EFE6', fill: PAL.rose, fillOp: 50, ink: PAL.ink, sw: sw2 * .6, curv: .3 });
      for (const sd of [-1, 1]) inkLine([[sd * 5.3 * u, -3.0 * u], [sd * 5.6 * u, -6 * u], [sd * 1 * u, -8.3 * u]], sw2 * .9, '#E9DCCB', 'ink', .5);
    }
    if (o.draw2) o.draw2(u2, sw2);
  };
  clawd(x, y - 0 * u, u, { ...o, col: ZAHN.col, dk: ZAHN.dk, lt: ZAHN.lt, noLegs: true, noShadow: true, draw: dr, throb: undefined });
}

// ---------- Requisiten ----------
const WOODC = '#B87A4B', WOODD = '#7C4A2C';
function board(x, y, w, h, txt, size, o = {}) {  // Holzschild mit gemalter Schrift (wie das P(DOOM)-Schild)
  push(); translate(x, y); rotate(o.rot || 0);
  if (o.ropes) for (const sd of [-1, 1]) inkLine([[sd * w * .35, -h / 2], [sd * w * .3, -h / 2 - o.ropes]], 1.2, '#5A4030', 'ink', 0);
  paint(rrPts(-w / 2, -h / 2, w, h, 14, 2), { wash: o.col || WOODC, fill: WOODD, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.3 });
  for (let k = 1; k < 3; k++) inkLine([[-w / 2 + 16, -h / 2 + h * k / 3 + jit(2)], [w / 2 - 16, -h / 2 + h * k / 3 + jit(2)]], .45, WOODD, 'inkfine', .3);
  pop();
  const c = Math.cos(o.rot || 0), sn = Math.sin(o.rot || 0);
  if (txt) letter(txt, x - sn * (o.ty || 0), y + c * (o.ty || 0), size, o.tcol || PAL.cream, { rot: o.rot || 0, pop: o.pop, ...(o.font ? { font: o.font } : {}) });
}
function doorway(x, floorY, w, h, o = {}) {  // Türrahmen mit offener Tür (Angel links), warmes Licht innen
  const x0 = x - w / 2, y0 = floorY - h;
  paint(rectPts(x0, y0, w, h, 2), { wash: o.inside || '#3A2530', fill: PAL.violet, fillOp: 50, tex: .6, ink: null });
  if (o.light) paint([[x0 + 10, y0 + 10], [x0 + w - 10, y0 + 10], [x0 + w + 160, floorY + 60], [x0 - 60, floorY + 60]], { fill: PAL.ochre, fillOp: 60 * o.light, bleed: .2, tex: .3, ink: null });
  const open = o.open ?? .8;
  paint([[x0, y0], [x0 - w * .55 * open, y0 + 40 * open], [x0 - w * .55 * open, floorY + 10 * open], [x0, floorY]], { wash: o.leaf || '#8A5A3C', fill: WOODD, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.1 });
  paint(ellPts(x0 - w * .45 * open, y0 + h * .55, 10, 12, 10), { wash: '#E8B23A', ink: PAL.ink, sw: .6 });
  for (const px of [x0 - 24, x0 + w]) paint(rectPts(px, y0 - 24, 24, h + 24, 2), { wash: o.frame || WOODC, fill: WOODD, fillOp: 50, tex: .6, ink: PAL.ink, sw: 1.1 });
  paint(rectPts(x0 - 40, y0 - 44, w + 80, 26, 2), { wash: o.frame || WOODC, fill: WOODD, fillOp: 50, tex: .6, ink: PAL.ink, sw: 1.1 });
}
function tearCal(x, y, s, days, idx, tearT) {  // Abreißkalender; idx = aktuelles Blatt, tearT = Alter des letzten Abrisses
  push(); translate(x, y); scale(s);
  paint(rectPts(-10, 0, 20, 150), { wash: WOODD, ink: PAL.ink, sw: .8 });
  paint(rectPts(-110, -250, 220, 260, 2), { wash: '#6B4A3A', fill: WOODD, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.1 });
  paint(rectPts(-95, -228, 190, 222, 1.5), { wash: PAL.cream, washOp: 255, fill: '#E6D6B8', fillOp: 50, tex: .5, ink: PAL.ink, sw: .9 });
  paint(rectPts(-95, -228, 190, 50, 1), { wash: '#C8324A', ink: PAL.ink, sw: .8 });
  for (const rx of [-60, 0, 60]) paint(ellPts(rx, -238, 8, 8, 8), { wash: '#9AA3AE', ink: PAL.ink, sw: .5 });
  pop();
  letter(days[Math.min(idx, days.length - 1)], x, y - 105 * s, 92 * s, PAL.ink, { ink: false });
  if (tearT != null && tearT >= 0 && tearT < .8 && idx > 0) {
    const k = tearT / .8;
    push(); translate(x + 260 * s * k, y - 120 * s - 160 * s * Math.sin(k * Math.PI) + 380 * s * k * k); rotate(k * 3.2); scale(s * (1 - .3 * k));
    paint(rectPts(-95, -110, 190, 222, 1.5), { wash: PAL.cream, washOp: 255, ink: PAL.ink, sw: .9 });
    paint(rectPts(-95, -110, 190, 50, 1), { wash: '#C8324A', ink: null });
    pop();
  }
}
function drillProp(x, y, s, rot, buzz = 0) {  // Bohrer-Handstück mit Schlauch
  const bx = buzz ? Math.sin(T * 90) * 3 * buzz : 0;
  inkLine([[x + 180 * s, y - 40 * s], [x + 420 * s, y - 150 * s], [x + 700 * s, y - 520 * s]], 5 * s, '#4A4F5C', 'ink', .7);
  push(); translate(x + bx, y); rotate(rot); scale(s);
  paint([[-20, -16], [200, -24], [220, 0], [200, 24], [-20, 16]], { wash: '#B9C0C8', fill: '#6D7680', fillOp: 90, tex: .6, ink: PAL.ink, sw: 1.1, curv: .2 });
  paint(rectPts(-70, -20, 60, 40, 2), { wash: '#9AA3AE', fill: '#6D7680', fillOp: 70, tex: .5, ink: PAL.ink, sw: 1 });
  paint(rectPts(-88, -3, 24, 6), { wash: '#E8E2D2', ink: PAL.ink, sw: .6 });
  inkLine([[20, -8], [180, -12]], .8, '#FFFFFF', 'inkfine', 0);
  pop();
  if (buzz > .05) for (let k = 0; k < 4; k++) { const a = -2.4 + k * .5 + jit(.1), r0 = 90 * s, r1 = 140 * s; inkLine([[x - 70 * s + Math.cos(a) * r0, y + Math.sin(a) * r0], [x - 70 * s + Math.cos(a) * r1, y + Math.sin(a) * r1]], 1.1, PAL.ink, 'inkfine', 0); }
}
function dentChair(x, floorY, s, lift = 0, o = {}) {  // Behandlungsstuhl mit Lampe; gibt Sitzpunkt zurück
  const up = 90 * lift * s, seatY = floorY - (170 * s + up);
  paint(ellPts(x, floorY + 6, 220 * s, 34 * s, 18), { fill: PAL.ink, fillOp: 80, bleed: .2, tex: .3, ink: null });
  paint(rrPts(x - 150 * s, floorY - 40 * s, 300 * s, 42 * s, 12 * s, 2), { wash: '#9AA3AE', fill: '#6D7680', fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.1 });
  paint(rectPts(x - 28 * s, seatY + 30 * s, 56 * s, floorY - 40 * s - seatY - 30 * s), { wash: '#C9CED6', fill: '#9AA3AE', fillOp: 60, tex: .5, ink: PAL.ink, sw: 1 });
  // Lehne (schräg) + Sitz + Fußteil
  paint([[x - 190 * s, seatY - 250 * s], [x - 120 * s, seatY - 262 * s], [x - 40 * s, seatY], [x - 130 * s, seatY + 16 * s]], { wash: o.col || PAL.teal, fill: '#2A6E6B', fillOp: 70, tex: .7, ink: PAL.ink, sw: 1.3, curv: .25 });
  paint(rrPts(x - 150 * s, seatY - 10 * s, 290 * s, 46 * s, 20 * s, 2), { wash: o.col || PAL.teal, fill: '#2A6E6B', fillOp: 70, tex: .7, ink: PAL.ink, sw: 1.3 });
  paint([[x + 120 * s, seatY - 6 * s], [x + 250 * s, seatY + 90 * s], [x + 220 * s, seatY + 120 * s], [x + 100 * s, seatY + 30 * s]], { wash: o.col || PAL.teal, fill: '#2A6E6B', fillOp: 70, tex: .7, ink: PAL.ink, sw: 1.2, curv: .3 });
  paint(ellPts(x - 170 * s, seatY - 270 * s, 50 * s, 26 * s, 14), { wash: o.col || PAL.teal, ink: PAL.ink, sw: 1 });
  // Lampe am Arm
  const lx = x + 120 * s, ly = seatY - 420 * s;
  inkLine([[x + 250 * s, floorY - 20 * s], [x + 280 * s, seatY - 300 * s], [lx + 60 * s, ly]], 3.2 * s, '#6D7680', 'ink', .3);
  if (o.lamp) paint([[lx - 70 * s, ly + 20 * s], [lx + 70 * s, ly + 20 * s], [lx + 200 * s, seatY + 40 * s], [lx - 260 * s, seatY + 40 * s]], { fill: '#FFE7A8', fillOp: 90 * o.lamp, bleed: .2, tex: .2, border: .1, ink: null });
  paint(ellPts(lx, ly, 80 * s, 36 * s, 18), { wash: o.lamp ? '#FFF1C0' : '#E6D6B8', fill: PAL.ochre, fillOp: 60, ink: PAL.ink, sw: 1.1 });
  return { sx: x - 10 * s, sy: seatY + 4 * s, lamp: [lx, ly] };
}
function wallClock(x, y, r, minutes, o = {}) {
  paint(ellPts(x, y, r + 22, r + 22, 32, 2), { wash: WOODC, fill: WOODD, fillOp: 60, tex: .6, ink: PAL.ink, sw: 1.4 });
  paint(ellPts(x, y, r, r, 32, 1.5), { wash: PAL.cream, washOp: 255, fill: '#E6D6B8', fillOp: 40, tex: .5, ink: PAL.ink, sw: 1 });
  const a0 = -Math.PI / 2, a1 = a0 + minutes / 60 * TAU;
  if (minutes > .3) { const w = [[x, y]]; for (let i = 0; i <= 24; i++) { const a = lerp(a0, a1, i / 24); w.push([x + Math.cos(a) * r * .9, y + Math.sin(a) * r * .9]); } paint(w, { fill: PAL.sap, fillOp: 220, bleed: .08, tex: .5, ink: null }); }
  for (let k = 0; k < 12; k++) { const a = k / 12 * TAU; inkLine([[x + Math.cos(a) * r * .8, y + Math.sin(a) * r * .8], [x + Math.cos(a) * r * .94, y + Math.sin(a) * r * .94]], k % 3 ? .7 : 1.4, PAL.ink, 'ink', 0); }
  inkLine([[x, y], [x + Math.cos(a1) * r * .82, y + Math.sin(a1) * r * .82]], 2.2, PAL.ink, 'ink', 0);
  const ah = a0 + (o.hour ?? .35) * TAU; inkLine([[x, y], [x + Math.cos(ah) * r * .5, y + Math.sin(ah) * r * .5]], 3, PAL.ink, 'ink', 0);
  paint(ellPts(x, y, 12, 12, 10), { wash: '#C8324A', ink: PAL.ink, sw: .6 });
}
function balloon(x, y, r, col, t, ph = 0) {
  const bx = x + Math.sin(t * 1.6 + ph) * 12, by = y + Math.sin(t * 2.1 + ph) * 8;
  inkLine([[bx, by + r * 1.15], [bx + 10, by + r * 2], [x, y + r * 3.4]], .7, PAL.ink, 'inkfine', .6);
  paint(ellPts(bx, by, r, r * 1.15, 20, 1.5), { wash: col, fill: PAL.ink, fillOp: 25, tex: .5, ink: PAL.ink, sw: .9 });
  paint(ellPts(bx - r * .35, by - r * .45, r * .2, r * .3, 10), { wash: PAL.cream, washOp: 200, ink: null });
}
function wings(x, y, s, flap = 0) {  // Feenflügel (hinter der Figur malen)
  for (const sd of [-1, 1]) {
    const a = sd * (.25 + .18 * flap);
    push(); translate(x + sd * 1.4 * s, y - 7.4 * s); rotate(a);
    paint(ellPts(sd * 2.3 * s, -1.6 * s, 2.4 * s, 1.5 * s, 20, 0, sd * -.5), { wash: '#DDEFF4', washOp: 170, fill: PAL.sky, fillOp: 80, bleed: .2, tex: .5, ink: PAL.ink, sw: .8 });
    paint(ellPts(sd * 1.8 * s, .8 * s, 1.6 * s, 1 * s, 16, 0, sd * .5), { wash: '#DDEFF4', washOp: 170, fill: PAL.sky, fillOp: 80, bleed: .2, tex: .5, ink: PAL.ink, sw: .8 });
    pop();
  }
}
function wandHand(glowK = 0) { return (s, sw) => {  // Zauberstab in der Hand
  inkLine([[0, 0], [1.2 * s, -2.8 * s]], sw * 1.1, '#6B4A3A', 'ink', 0);
  paint(starPts(1.3 * s, -3.1 * s, .9 * s * (1 + .15 * glowK), .42, 5, -Math.PI / 2 + T * 2), { wash: PAL.ochre, fill: PAL.cream, fillOp: 70, ink: PAL.ink, sw: sw * .5 });
}; }
function mirrorHand(s, sw) {
  inkLine([[0, 0], [2.2 * s, -1.8 * s]], sw * .9, '#9AA3AE', 'ink', 0);
  paint(ellPts(2.5 * s, -2.1 * s, .6 * s, .6 * s, 12), { wash: '#DDEFF4', fill: PAL.sky, fillOp: 60, ink: PAL.ink, sw: sw * .6 });
}
