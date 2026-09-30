// Kistenheld Umzüge – V5 im Stil des PS1-Casinos (g russ, „Final Version“): warme Innenräume mit Pixeltexturen
// (Teppichmuster, Holzvertäfelung, Tapete, Stoffrauschen), facettierte Köpfe mit Pixelgesichtern und Keilnase,
// Blockhaare, Nebel ins Dunkle, Lampenlicht, 640×360 mit Vertex-Snapping und 15-Bit-Dithering, harte Schnitte,
// Pixelschrift weiß/gelb mit schwarzer Kontur, LED-Schilder im Raum. Jedes Bild ist eine reine Funktion von t.
import * as THREE from './vendor/three.module.js';
import { K, CUT, DUR } from './zeiten.js';
await document.fonts.load('40px PX');

THREE.ColorManagement.enabled = false;
const W = 1920, H = 1080, RW = 640, RH = 360;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x)), lin = (t, a, b) => clamp((t - a) / (b - a)), mix = (a, b, k) => a + (b - a) * k;
const eo = k => 1 - Math.pow(1 - k, 3), eio = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
const back = k => { if (k <= 0) return 0; if (k >= 1) return 1; const c1 = 2, c3 = c1 + 1; return 1 + c3 * Math.pow(k - 1, 3) + c1 * Math.pow(k - 1, 2); };
function rng(a) { return () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
// Palette aus dem Casino (gemessen): Teppich #fe6927, Bezugsrot #681a12, Holz #6b3f25/#7d5e4a, Wand #343339/#201715, Haut #f1cfae, Tiefe #110804
const P = { carpet: '#E8571F', carpet2: '#FE6927', red: '#8E1E14', redDk: '#5A120C', wood: '#6B3F25', woodLt: '#93643E', woodDk: '#2E150A', wall: '#343339',
  deep: '#110804', skin: '#F1CFAE', skin2: '#D9A57C', gold: '#C9A13A', green: '#2F8A3C', orange: '#FF7A1A', blue: '#1E3A8A', yel: '#F2DC3C', kraft: '#B9804A', white: '#F4F4EE' };

// ---------- Renderer + PS1-Nachbearbeitung ----------
const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: false, preserveDrawingBuffer: true });
renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
const rt = new THREE.WebGLRenderTarget(RW, RH, { minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter, depthBuffer: true });
const post = new THREE.ShaderMaterial({
  uniforms: { tD: { value: rt.texture }, uRes: { value: new THREE.Vector2(RW, RH) }, uFade: { value: 1 }, uWarm: { value: .28 } },
  vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }',
  fragmentShader: `uniform sampler2D tD; uniform vec2 uRes; uniform float uFade, uWarm; varying vec2 vUv;
    float bayer(vec2 p){ int x=int(mod(p.x,4.)), y=int(mod(p.y,4.)); int i=x+y*4; float m[16];
      m[0]=0.;m[1]=8.;m[2]=2.;m[3]=10.;m[4]=12.;m[5]=4.;m[6]=14.;m[7]=6.;m[8]=3.;m[9]=11.;m[10]=1.;m[11]=9.;m[12]=15.;m[13]=7.;m[14]=13.;m[15]=5.;
      for(int k=0;k<16;k++){ if(k==i) return m[k]/16.; } return 0.; }
    void main(){ vec2 px=floor(vUv*uRes); vec3 c=texture2D(tD,(px+.5)/uRes).rgb;
      c=mix(c, c*vec3(1.12,.96,.82)+vec3(.02,.004,0.), uWarm);
      vec2 d=(vUv-.5)*vec2(1.,.75); c*=1.-smoothstep(.3,.78,length(d))*.6;
      c=floor(c*31.+(bayer(px)-.5)*1.1+.5)/31.; gl_FragColor=vec4(c*uFade,1.); }`, depthTest: false, depthWrite: false });
const postScene = new THREE.Scene(); postScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), post)); const postCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const SNAP = { value: new THREE.Vector2(RW / 2.2, RH / 2.2) };   // Vertex-Snapping (PS1-Wackeln)
function ps1(m) { m.onBeforeCompile = sh => { sh.uniforms.uSnap = SNAP; sh.vertexShader = 'uniform vec2 uSnap;\n' + sh.vertexShader.replace('#include <fog_vertex>',
  '#include <fog_vertex>\n if(gl_Position.w>0.0){ vec2 s=gl_Position.xy/gl_Position.w; s=floor(s*uSnap+.5)/uSnap; gl_Position.xy=s*gl_Position.w; }'); }; return m; }

// ---------- Pixeltexturen ----------
function canvasTex(w, h, draw, rep = [1, 1]) { const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d'); g.imageSmoothingEnabled = false; draw(g, w, h, c);
  const t = new THREE.CanvasTexture(c); t.magFilter = THREE.NearestFilter; t.minFilter = THREE.NearestFilter; t.generateMipmaps = false;
  t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); t.userData.canvas = c; return t; }
function noise(g, w, h, col, amt, seed) { const r = rng(seed); g.fillStyle = col; g.fillRect(0, 0, w, h); for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const v = (r() - .5) * amt; g.fillStyle = v > 0 ? `rgba(255,255,255,${v})` : `rgba(0,0,0,${-v})`; g.fillRect(x, y, 1, 1); } }
const TX = {};
TX.carpet = canvasTex(64, 64, (g, w, h) => { noise(g, w, h, P.carpet, .12, 1); const px = (x, y, c) => { g.fillStyle = c; g.fillRect(x & 63, y & 63, 1, 1); };
  for (const [cx, cy] of [[16, 16], [48, 48]]) { for (let k = -7; k <= 7; k++) { px(cx + k, cy, '#F4B830'); px(cx, cy + k, '#F4B830'); if (Math.abs(k) < 5) { px(cx + k, cy + k, P.red); px(cx + k, cy - k, P.red); } } px(cx, cy, '#1D8A8A'); px(cx + 1, cy, '#1D8A8A'); }
  for (let k = 0; k < 64; k += 3) { px(k, 32, '#F4D060'); px(32, k, P.red); } }, [6, 6]);
TX.runner = canvasTex(32, 32, (g, w, h) => { noise(g, w, h, '#A8251A', .14, 2); g.fillStyle = '#E0A93A'; g.fillRect(0, 0, 3, 32); g.fillRect(29, 0, 3, 32); for (let y = 2; y < 32; y += 8) { g.fillStyle = '#E0A93A'; g.fillRect(14, y, 4, 4); g.fillStyle = '#5A120C'; g.fillRect(15, y + 1, 2, 2); } });
TX.wood = canvasTex(32, 64, (g, w, h) => { noise(g, w, h, P.wood, .16, 3); for (let x = 0; x < w; x += 8) { g.fillStyle = P.woodDk; g.fillRect(x, 0, 1, h); } const r = rng(4); for (let i = 0; i < 40; i++) { g.fillStyle = 'rgba(30,12,4,.35)'; g.fillRect(r() * w | 0, r() * h | 0, 1, 3 + r() * 6 | 0); } g.fillStyle = P.woodLt; g.fillRect(0, 0, w, 2); }, [4, 1]);
TX.panel = canvasTex(32, 32, (g, w, h) => { noise(g, w, h, '#4A2412', .14, 5); g.fillStyle = '#2A1208'; g.fillRect(3, 3, 26, 26); g.fillStyle = '#5A2E16'; g.fillRect(5, 5, 22, 22); g.fillStyle = 'rgba(255,200,140,.12)'; g.fillRect(5, 5, 22, 2); }, [8, 2]);
TX.paper = canvasTex(32, 32, (g, w, h) => { noise(g, w, h, '#2E1A14', .1, 6); const r = rng(7); for (let y = 2; y < 32; y += 8) for (let x = (y / 8 % 2) * 4 + 2; x < 32; x += 8) { g.fillStyle = '#3E2418'; g.fillRect(x, y, 3, 3); g.fillStyle = '#5A3A24'; g.fillRect(x + 1, y + 1, 1, 1); } }, [6, 3]);
TX.plaster = canvasTex(32, 32, (g, w, h) => noise(g, w, h, '#C99A6A', .1, 8), [6, 2]);
TX.brick = canvasTex(32, 32, (g, w, h) => { noise(g, w, h, '#8A4A30', .14, 9); g.fillStyle = '#4A2A1E'; for (let y = 0; y < 32; y += 4) { g.fillRect(0, y, 32, 1); for (let x = (y / 4 % 2) * 4; x < 32; x += 8) g.fillRect(x, y, 1, 4); } }, [10, 8]);
TX.cobble = canvasTex(32, 32, (g, w, h) => { noise(g, w, h, '#3A3036', .16, 10); g.fillStyle = '#1E181C'; for (let y = 0; y < 32; y += 5) { g.fillRect(0, y, 32, 1); for (let x = (y / 5 % 2) * 3; x < 32; x += 6) g.fillRect(x, y, 1, 5); } }, [16, 6]);
TX.kraft = canvasTex(16, 16, (g, w, h) => { noise(g, w, h, P.kraft, .16, 11); g.fillStyle = '#D9B070'; g.fillRect(6, 0, 4, 16); g.fillStyle = 'rgba(0,0,0,.15)'; g.fillRect(0, 15, 16, 1); });
TX.velvet = canvasTex(16, 16, (g, w, h) => { noise(g, w, h, '#9A1C16', .18, 12); g.fillStyle = '#5A0E0A'; g.fillRect(3, 4, 1, 1); g.fillRect(11, 4, 1, 1); g.fillRect(7, 11, 1, 1); }, [2, 1]);
const fabric = (col, seed) => canvasTex(16, 16, (g, w, h) => noise(g, w, h, col, .2, seed));
const LAMB = {}; function M(col, map) { const k = col + (map ? map.uuid : ''); return LAMB[k] || (LAMB[k] = ps1(new THREE.MeshLambertMaterial({ color: map ? '#FFFFFF' : col, map: map || null, flatShading: true }))); }
function Mt(map, tint = '#FFFFFF') { return ps1(new THREE.MeshLambertMaterial({ color: tint, map, flatShading: true })); }
function E(col, map) { return ps1(new THREE.MeshBasicMaterial({ color: col, map: map || null, transparent: !!map, alphaTest: map ? .5 : 0 })); }

// Pixelschrift-Texturen (LED-Schilder, Etiketten)
let PXF = 'PX';
function led(txt, w, h, col, o = {}) { return canvasTex(w, h, (g, W2, H2) => { g.fillStyle = o.bg || '#140A06'; g.fillRect(0, 0, W2, H2); if (o.frame) { g.fillStyle = o.frame; g.fillRect(0, 0, W2, 2); g.fillRect(0, H2 - 2, W2, 2); g.fillRect(0, 0, 2, H2); g.fillRect(W2 - 2, 0, 2, H2); }
  g.font = `${o.size || h * .7}px ${PXF}`; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = col; g.fillText(txt, W2 / 2, H2 / 2 + 1);
  if (o.dots !== false) { g.fillStyle = 'rgba(0,0,0,.45)'; for (let y = 1; y < H2; y += 2) g.fillRect(0, y, W2, 1); } }); }

// ---------- Bausteine ----------
const scene = new THREE.Scene();
const cam = new THREE.PerspectiveCamera(50, W / H, .05, 200);
const hemi = new THREE.HemisphereLight('#FFD2A0', '#6A4030', .55); scene.add(hemi);
const key = new THREE.DirectionalLight('#FFF2E4', 2.3); scene.add(key); scene.add(key.target);
function box(par, w, h, d, mat, x = 0, y = 0, z = 0) { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); par.add(m); return m; }
function grp(par, x = 0, y = 0, z = 0) { const g = new THREE.Group(); g.position.set(x, y, z); par.add(g); return g; }
function plane(par, w, h, mat, x = 0, y = 0, z = 0, ry = 0) { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat); m.position.set(x, y, z); m.rotation.y = ry; par.add(m); return m; }
const LSC = 5; function light(par, col, int, dist, x, y, z) { const L = new THREE.PointLight(col, int * LSC, dist, 1.3); L.position.set(x, y, z); par.add(L); return L; }
function wallLamp(par, x, y, z, ry = 0) { const g = grp(par, x, y, z); g.rotation.y = ry; box(g, .08, .3, .06, M(P.gold), 0, 0, .03); box(g, .22, .16, .18, E('#FFE3A0'), 0, .16, .12); box(g, .26, .04, .22, M(P.gold), 0, .08, .12); return light(g, '#FFC890', 2.6, 8, 0, .15, .5); }

// Pixelgesichter 24×24 (Augen, Brauen, Mund, Rouge wie im Casino)
const FACES = {};
function faceTex(mood) { return FACES[mood] || (FACES[mood] = canvasTex(16, 16, (g) => { const px = (x, y, c, w = 1, h = 1) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  const ink = '#1A0E0A', br = '#4A2A1A', hap = mood === 'joy' || mood === 'happy';
  if (hap) { px(3, 7, ink); px(4, 6, ink); px(5, 7, ink); px(10, 7, ink); px(11, 6, ink); px(12, 7, ink); }
  else if (mood === 'tired') { px(3, 7, ink, 3, 1); px(10, 7, ink, 3, 1); px(3, 8, '#B07868', 3, 1); px(10, 8, '#B07868', 3, 1); }
  else { px(3, 6, '#F4F4EE', 3, 2); px(10, 6, '#F4F4EE', 3, 2); px(4, 6, '#2A5A9A', 1, 2); px(11, 6, '#2A5A9A', 1, 2); if (mood === 'shock') { px(3, 5, '#F4F4EE', 3, 1); px(10, 5, '#F4F4EE', 3, 1); } }
  if (mood === 'stress' || mood === 'shock') { px(2, 4, br, 2, 1); px(4, 3, br, 2, 1); px(12, 4, br, 2, 1); px(10, 3, br, 2, 1); }
  else if (mood === 'sad' || mood === 'tired') { px(3, 4, br, 2, 1); px(5, 5, br); px(11, 4, br, 2, 1); px(10, 5, br); }
  else if (!hap) { px(3, 4, br, 3, 1); px(10, 4, br, 3, 1); }
  if (mood === 'joy') { px(5, 10, ink, 6, 1); px(5, 11, '#8A1A20', 6, 2); px(6, 12, '#E86070', 4, 1); }
  else if (mood === 'happy') { px(5, 10, ink); px(10, 10, ink); px(6, 11, ink, 4, 1); }
  else if (mood === 'shock') { px(6, 10, ink, 4, 1); px(6, 11, '#6A1018', 4, 2); px(6, 13, ink, 4, 1); }
  else if (mood === 'stress') { px(5, 11, ink, 6, 1); px(5, 12, '#F4F4EE', 6, 1); px(5, 13, ink, 6, 1); }
  else if (mood === 'sad' || mood === 'tired') { px(6, 11, ink, 4, 1); px(5, 12, ink); px(10, 12, ink); }
  else px(6, 11, ink, 4, 1);
  if (hap) { px(1, 9, '#E88080', 2, 1); px(13, 9, '#E88080', 2, 1); }
  if (mood === 'stress' || mood === 'tired') { px(14, 1, '#8AD0FF', 1, 2); px(13, 3, '#8AD0FF', 2, 1); }
})); }
// Figur: Blockkörper mit Stofftextur, facettierter Kopf (Kugel 7×5, flach schattiert) + Pixelgesicht + Keilnase, Blockhaare
function person(par, o = {}) {
  const g = grp(par, o.x || 0, 0, o.z || 0); g.rotation.y = o.ry || 0; const skin = o.skin || P.skin;
  const shirtT = fabric(o.shirt || '#E8E4DA', (o.seed || 1) * 7), pantsT = fabric(o.pants || '#2E3A5A', (o.seed || 1) * 7 + 3);
  const body = grp(g, 0, 0, 0);
  const leg = side => { const hip = grp(body, side * .14, .9, 0); box(hip, .24, .46, .26, Mt(pantsT), 0, -.23, 0); const knee = grp(hip, 0, -.46, 0); box(knee, .22, .44, .24, Mt(pantsT), 0, -.22, 0); box(knee, .26, .12, .36, M('#1E1410'), 0, -.44, .05); return { hip, knee }; };
  const lL = leg(-1), lR = leg(1);
  const torso = box(body, .64, .74, .36, Mt(shirtT), 0, 1.28, 0);
  box(body, .6, .12, .34, Mt(pantsT), 0, .92, 0);
  if (o.logo) { const lg = plane(body, .26, .16, E('#FFFFFF', led('KH', 16, 10, P.orange, { bg: '#1E3A8A', size: 8, dots: false })), .15, 1.42, .185); }
  if (o.apron) box(body, .5, .5, .02, M(o.apron), 0, 1.1, .19);
  const arm = side => { const sh = grp(body, side * .41, 1.58, 0); box(sh, .2, .42, .22, Mt(shirtT), 0, -.2, 0); const el = grp(sh, 0, -.42, 0); box(el, .18, .38, .2, o.short ? M(skin) : Mt(shirtT), 0, -.19, 0);
    const hand = grp(el, 0, -.42, 0); box(hand, .15, .14, .1, M(skin), 0, 0, 0); for (let f = 0; f < 3; f++) box(hand, .035, .07, .05, M(skin), -.04 + f * .04, -.09, 0); return { sh, el, hand }; };
  const aL = arm(-1), aR = arm(1);
  box(body, .16, .12, .16, M(skin), 0, 1.7, 0);
  const head = grp(body, 0, 1.98, 0);
  const hg = new THREE.SphereGeometry(.3, 7, 5); const hm = new THREE.Mesh(hg, M(skin)); hm.scale.set(1, 1.12, .95); head.add(hm);
  const faceMat = E('#FFFFFF', faceTex(o.mood || 'neutral')); const face = plane(head, .42, .42, faceMat, 0, -.02, .305);
  const nose = new THREE.Mesh(new THREE.ConeGeometry(.055, .15, 4), M(o.skin2 || P.skin2)); nose.rotation.x = Math.PI / 2; nose.position.set(0, -.03, .35); head.add(nose);
  const hc = o.hair || '#3A2014', hmat = Mt(fabric(hc, 5), '#FFFFFF');
  if (o.hairStyle !== 'bald') { const cap = new THREE.Mesh(new THREE.SphereGeometry(.315, 7, 4, 0, Math.PI * 2, 0, Math.PI * .5), hmat); cap.scale.set(1.03, 1.08, 1.03); cap.rotation.x = -.22; cap.position.set(0, .03, -.02); head.add(cap);
    for (let k = 0; k < 4; k++) box(head, .14, .07 + (k % 2) * .03, .06, hmat, -.21 + k * .14, .25 - (k % 2) * .02, .24);
    box(head, .1, .2, .3, hmat, -.29, .08, -.05); box(head, .1, .2, .3, hmat, .29, .08, -.05); }
  if (o.hairStyle === 'long') { box(head, .14, .6, .3, hmat, -.33, -.2, -.05); box(head, .14, .6, .3, hmat, .33, -.2, -.05); box(head, .5, .5, .12, hmat, 0, -.2, -.28); }
  if (o.cap) { box(head, .66, .14, .62, M(o.cap), 0, .33, 0); box(head, .5, .04, .26, M(o.cap), 0, .28, .4); }
  if (o.beard) box(head, .44, .16, .08, hmat, 0, -.22, .25);
  return { g, body, lL, lR, aL, aR, head, faceMat, mood(m) { const t = faceTex(m); if (faceMat.map !== t) { faceMat.map = t; faceMat.needsUpdate = true; } } };
}
function pose(p, t, o = {}) {
  const w = o.walk || 0, ph = t * 8 + (o.ph || 0), br = Math.sin(t * 2.2 + (o.ph || 0)) * .015;
  for (const [L, s] of [[p.lL, 1], [p.lR, -1]]) { L.hip.rotation.x = Math.sin(ph) * .5 * w * s; L.knee.rotation.x = Math.max(0, -Math.sin(ph) * s) * .6 * w; }
  for (const [A, s] of [[p.aL, 1], [p.aR, -1]]) { A.sh.rotation.set(-Math.sin(ph) * .45 * w * s, 0, s * -.08); A.el.rotation.set(-.15, 0, 0); }
  p.body.position.y = br + Math.abs(Math.sin(ph)) * .04 * w; p.body.rotation.set(0, 0, 0);
  if (o.push) { p.aL.sh.rotation.x = p.aR.sh.rotation.x = -1.25 * o.push; p.aL.el.rotation.x = p.aR.el.rotation.x = -.4 * o.push; p.body.rotation.x = .3 * o.push; p.lL.hip.rotation.x = -.5 * o.push; p.lR.hip.rotation.x = .35 * o.push; p.lL.knee.rotation.x = .5 * o.push; p.body.position.y = -.08 * o.push + Math.sin(t * 22) * .01; }
  if (o.phone) { p.aR.sh.rotation.x = -.7 * o.phone; p.aR.el.rotation.x = -1.3 * o.phone; p.aR.sh.rotation.z = .2 * o.phone; }
  if (o.carry) { p.aL.sh.rotation.x = p.aR.sh.rotation.x = -1.0 * o.carry; p.aL.el.rotation.x = p.aR.el.rotation.x = -.6 * o.carry; }
  if (o.wave) { p.aR.sh.rotation.z = 2.5 * o.wave + Math.sin(t * 11) * .3 * o.wave; p.aR.el.rotation.x = -.3; }
  if (o.cheer) { p.aL.sh.rotation.z = -2.6 * o.cheer; p.aR.sh.rotation.z = 2.6 * o.cheer; p.body.position.y += Math.abs(Math.sin(t * 7)) * .1 * o.cheer; }
  if (o.sit) { p.lL.hip.rotation.x = p.lR.hip.rotation.x = -1.45 * o.sit; p.lL.knee.rotation.x = p.lR.knee.rotation.x = 1.3 * o.sit; p.body.position.y = -.5 * o.sit + br; }
  if (o.eat) { p.aR.sh.rotation.x = -1.1 + Math.sin(t * 3) * .15; p.aR.el.rotation.x = -1.2; }
  if (o.slump) { p.head.rotation.x = .25 * o.slump; p.body.rotation.x = .08 * o.slump; p.aL.sh.rotation.x = p.aR.sh.rotation.x = .05; }
  else p.head.rotation.x = o.nod || 0;
  p.head.rotation.y = (o.look || 0) + Math.sin(t * 1.3 + (o.ph || 0)) * .06;
}
function sofa(par, x, y, z) { const g = grp(par, x, y, z); const v = Mt(TX.velvet); box(g, 2.1, .4, .9, v, 0, .42, 0); box(g, 2.1, .7, .26, v, 0, .85, -.34);
  box(g, .24, .58, .9, v, -1.05, .6, 0); box(g, .24, .58, .9, v, 1.05, .6, 0); box(g, .96, .14, .66, v, -.5, .7, .08); box(g, .96, .14, .66, v, .5, .7, .08);
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) box(g, .1, .22, .1, M('#2A140A'), sx * .92, .12, sz * .34); box(g, 2.14, .06, .92, M(P.gold), 0, .22, 0); return g; }
const ROOMS = [['KÜCHE', '#E8322E'], ['BAD', '#2D8BE8'], ['KIND', '#F2DC3C'], ['WOHNEN', '#2DBE6C']];
const LABELS = ROOMS.map(([n, c]) => led(n, 48, 16, n === 'KIND' ? '#1A1008' : '#FFFFFF', { bg: c, size: 11, dots: false }));
function carton(par, x, y, z, s = 1, lab = -1) { const g = grp(par, x, y, z); g.scale.setScalar(s); const km = Mt(TX.kraft); box(g, .62, .46, .5, km, 0, .23, 0);
  if (lab >= 0) plane(g, .34, .12, E('#FFFFFF', LABELS[lab]), 0, .28, .252); return g; }
function flatCarton(par, x, y, z, ry) { const m = box(par, .9, .7, .03, Mt(TX.kraft), x, y, z); m.rotation.set(-.12, ry, 0); return m; }
function books(par, x, y, z, w, seed) { const r = rng(seed); let bx = x - w / 2; while (bx < x + w / 2 - .05) { const bw = .04 + r() * .05, bh = .22 + r() * .12; box(par, bw, bh, .2, M(['#8E1E14', '#1E4A6A', '#C9A13A', '#2F6A3C', '#5A2E6A', '#D8C8A0'][r() * 6 | 0]), bx + bw / 2, y + bh / 2, z); bx += bw + .005; } }
function truck(par, kind) { const g = grp(par); const kh = kind === 'kh', main = kh ? P.orange : '#E8E8E0', bl = kh ? 5 : 3.4, bh = kh ? 2.6 : 2.1;
  const side = canvasTex(128, 64, (c, w, h) => { c.fillStyle = main; c.fillRect(0, 0, w, h); const r = rng(kh ? 20 : 21); for (let i = 0; i < 300; i++) { c.fillStyle = `rgba(0,0,0,${r() * .08})`; c.fillRect(r() * w | 0, r() * h | 0, 1, 1); }
    if (kh) { c.fillStyle = P.blue; c.fillRect(0, 46, w, 18); c.fillStyle = P.kraft; c.fillRect(8, 12, 20, 16); c.fillStyle = '#D9B070'; c.fillRect(16, 12, 4, 16); c.font = `14px ${PXF}`; c.fillStyle = '#FFFFFF'; c.fillText('KISTENHELD', 34, 24); c.font = `10px ${PXF}`; c.fillStyle = P.yel; c.fillText('UMZÜGE', 34, 38); c.fillStyle = '#FFFFFF'; c.font = `9px ${PXF}`; c.fillText('kistenheld-umzuege.de', 8, 58); }
    else { c.fillStyle = '#1E6BD6'; c.fillRect(0, 40, w, 6); c.font = `13px ${PXF}`; c.fillStyle = '#20284A'; c.fillText('MIETWAGEN', 22, 30); } });
  const sm = Mt(side); box(g, bl, bh, 2.3, M(main), -bl / 2 + 1, .7 + bh / 2, 0); plane(g, bl - .2, bh - .2, sm, -bl / 2 + 1, .7 + bh / 2, 1.16);
  box(g, 1.8, 1.7, 2.3, M(kh ? P.blue : '#E8E8E0'), 1.9, 1.55, 0); box(g, .05, .75, 1.9, E('#8ABEDC'), 2.81, 1.95, 0);
  for (const zz of [-.8, .8]) box(g, .08, .22, .44, E('#FFF1B0'), 2.82, .95, zz);
  for (const x of [-bl + 1.9, 1.9]) for (const zz of [-1.12, 1.12]) { const w = new THREE.Mesh(new THREE.CylinderGeometry(.42, .42, .28, 8), M('#15100E')); w.rotation.x = Math.PI / 2; w.position.set(x, .42, zz); g.add(w); }
  return g; }
// Pixel-Herz / Ausruf als Sprite
const HEART = canvasTex(9, 8, g => { const rows = ['.xx...xx.', 'xxxx.xxxx', 'xxxxxxxxx', 'xxxxxxxxx', '.xxxxxxx.', '..xxxxx..', '...xxx...', '....x....']; rows.forEach((r, y) => [...r].forEach((c, x) => { if (c === 'x') { g.fillStyle = y < 2 && x % 4 === 1 ? '#FF9AA8' : '#E8243A'; g.fillRect(x, y, 1, 1); } })); });
const BANG = canvasTex(5, 10, g => { g.fillStyle = '#E8243A'; g.fillRect(1, 0, 3, 6); g.fillRect(1, 7, 3, 2); g.fillStyle = '#FFFFFF'; g.fillRect(1, 0, 1, 5); });
function sprite(par, tex, s) { const m = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true, alphaTest: .5, depthTest: false })); m.scale.set(s * tex.image.width / tex.image.height, s, 1); m.renderOrder = 10; par.add(m); return m; }

// ================= Sets =================
const SETS = [];
function set(x) { const g = grp(scene, x, 0, 0); SETS.push(g); return g; }
let OX = 0; function vis(s) { SETS.forEach(g => g.visible = g === s); OX = s.position.x; }

// A · Altbau-Treppenhaus: Holzstufen mit Läufer, Tapete, Messinglampen, dunkles Treppenauge
const sA = set(0);
box(sA, 10, .2, 6, Mt(TX.wood), 0, -.1, 0);
plane(sA, 18, 3.4, Mt(TX.paper), 2, 4.6, -1.6); plane(sA, 18, 1.4, Mt(TX.panel), 2, 1.9, -1.59); plane(sA, 18, 1.4, Mt(TX.panel), 2, .7, -1.59);
box(sA, 18, .1, .12, M(P.woodLt), 2, 2.62, -1.55);
for (let i = 0; i < 16; i++) { const x = .4 + i * .42, y = .12 + i * .26;
  box(sA, .44, .26 * (i + 1), 1.5, M(P.woodDk), x, .13 * (i + 1) - .01, -.75);
  box(sA, .46, .05, 1.54, Mt(TX.wood), x, .27 + i * .26, -.75); box(sA, .46, .052, .9, Mt(TX.runner), x, .272 + i * .26, -.8);
  if (i % 2 === 0) box(sA, .05, .95, .05, M(P.woodDk), x, .75 + i * .26, .02); }
{ const rail = box(sA, 7.2, .08, .1, M(P.woodLt), 3.55, 1.25 + 2.08, .02); rail.rotation.z = Math.atan2(.26, .42); }
box(sA, .14, 1.2, .14, M(P.woodLt), .3, .6, .02); box(sA, .2, .1, .2, M(P.gold), .3, 1.24, .02);
const lampA1 = wallLamp(sA, 1.2, 2.4, -1.55), lampA2 = wallLamp(sA, 5.2, 3.6, -1.55);
const signOG = plane(sA, .8, .3, Mt(led('3. OG', 48, 18, '#E0C890', { bg: '#2A1A0E', frame: P.gold, size: 12, dots: false })), 6.6, 4.4, -1.55);
const ledSA = plane(sA, 1.9, .42, E('#FFFFFF', led('SAMSTAG 08:00', 96, 20, P.yel, { size: 13 })), -1.2, 3.25, -1.55);
const liftSign = plane(sA, 1.1, .7, Mt(canvasTex(44, 28, (g) => { g.fillStyle = '#E8E0C8'; g.fillRect(0, 0, 44, 28); g.fillStyle = '#20180E'; g.fillRect(14, 4, 16, 18); g.fillStyle = '#E8E0C8'; g.fillRect(16, 6, 12, 14); g.fillStyle = '#20180E'; g.fillRect(18, 8, 3, 3); g.fillRect(23, 8, 3, 3); g.fillRect(18, 12, 3, 6); g.fillRect(23, 12, 3, 6);
  g.fillStyle = '#E8243A'; for (let k = 0; k < 22; k++) { g.fillRect(11 + k, 3 + k * 1.05 | 0, 3, 2); g.fillRect(33 - k, 3 + k * 1.05 | 0, 3, 2); } })), -2.4, 1.9, -1.55);
const sofaA = sofa(sA, 2.1, 1.35, -.75); sofaA.rotation.set(0, .42, .5);
const man = person(sA, { x: .7, z: -.5, shirt: '#3E5A8A', pants: '#2A2A3A', hair: '#3A2014', mood: 'stress', seed: 2 });
man.g.rotation.y = -1.5;
const bangA = sprite(sA, BANG, .5);
box(sA, 30, 12, 1, M('#0A0503'), 2, 5, -2.4);

// B · alte Wohnung: Teppichmuster, Holzvertäfelung, volles Regal, flache Kartons, Stehlampe
const sB = set(100);
box(sB, 12, .1, 10, Mt(TX.carpet), 0, -.05, 0);
plane(sB, 12, 3.2, Mt(TX.panel), 0, 1.6, -3.2); plane(sB, 10, 3.2, Mt(TX.panel), -4.2, 1.6, 0, Math.PI / 2); box(sB, 12, .14, .1, M(P.woodLt), 0, 3.2, -3.15);
for (let s = 0; s < 4; s++) { box(sB, 2.6, .05, .34, M(P.wood), -2.4, .5 + s * .6, -2.95); books(sB, -2.4, .53 + s * .6, -2.95, 2.4, 30 + s); } box(sB, .08, 2.6, .36, M(P.woodDk), -3.72, 1.3, -2.95); box(sB, .08, 2.6, .36, M(P.woodDk), -1.08, 1.3, -2.95);
box(sB, 2.2, .5, .6, M(P.wood), 1.6, .25, -2.8); const tvB = box(sB, .9, .6, .1, E('#2A3A40'), 1.6, .85, -2.85);
for (let k = 0; k < 4; k++) flatCarton(sB, .2 + k * .18, .36, -2.5 + k * .06, .1 * k);
const lampB = grp(sB, 3.2, 0, -2.2); box(lampB, .08, 1.7, .08, M(P.gold), 0, .85, 0); box(lampB, .5, .4, .5, E('#FFD890'), 0, 1.8, 0); const lampBL = light(lampB, '#FFA850', 5, 10, 0, 1.6, .6);
const picB = plane(sB, 1.1, .8, Mt(canvasTex(22, 16, g => { g.fillStyle = '#C9A13A'; g.fillRect(0, 0, 22, 16); g.fillStyle = '#1E2A40'; g.fillRect(2, 2, 18, 12); g.fillStyle = '#C04020'; g.fillRect(4, 8, 8, 6); g.fillStyle = '#E8C070'; g.fillRect(12, 4, 6, 5); })), 3.3, 2.2, -3.15);
// V7: Kalenderblatt nur „MO“ + Aktentasche (Symbol für den neuen Job) statt „MONTAG / NEUER JOB“
const cal = plane(sB, .9, 1.1, Mt(canvasTex(24, 30, g => { g.fillStyle = '#F0E6D0'; g.fillRect(0, 0, 24, 30); g.fillStyle = '#C0281E'; g.fillRect(0, 0, 24, 6); g.fillStyle = '#F0E6D0'; g.fillRect(5, 1, 2, 4); g.fillRect(17, 1, 2, 4);
  g.fillStyle = '#20180E'; g.font = `13px ${PXF}`; g.textAlign = 'center'; g.fillText('MO', 12, 18);
  g.fillStyle = '#6B3F25'; g.fillRect(7, 22, 10, 6); g.fillStyle = '#3C1F16'; g.fillRect(10, 20, 4, 1); g.fillRect(10, 20, 1, 2); g.fillRect(13, 20, 1, 2); g.fillRect(7, 24, 10, 1); g.fillStyle = P.gold; g.fillRect(11, 24, 2, 2); })), .2, 1.9, -3.14);
const man2 = person(sB, { x: 0, z: 0, shirt: '#3E5A8A', pants: '#2A2A3A', hair: '#3A2014', mood: 'sad', seed: 2 });
const phone = grp(sB, 0, 0, 0); box(phone, .34, .62, .04, M('#141418'), 0, 0, 0);
const phoneScr = canvasTex(40, 72, () => {}); const phoneMat = E('#FFFFFF', phoneScr); phoneMat.transparent = false; phoneMat.alphaTest = 0; plane(phone, .3, .56, phoneMat, 0, 0, .025);
const handB = grp(sB, 0, 0, 0); box(handB, .3, .3, .12, M(P.skin), 0, 0, 0); for (let f = 0; f < 3; f++) box(handB, .07, .16, .08, M(P.skin), -.09 + f * .08, .2, .02); box(handB, .2, .5, .14, Mt(fabric('#3E5A8A', 3)), 0, -.35, 0);

// C · Straße am Abend: Pflaster, Altbaufassade mit warmen Fenstern, Laternen, Wagen
const sC = set(200);
box(sC, 60, .1, 30, Mt(TX.cobble), 0, -.05, 4);
const facade = grp(sC, 0, 0, -3);
box(facade, 26, 14, .6, Mt(TX.brick), 0, 7, -.3);
const WINS = [];
for (let fl = 0; fl < 4; fl++) for (let c = 0; c < 8; c++) { const x = -10.5 + c * 3, y = 1.6 + fl * 3.2, on = rng(fl * 9 + c)() > .35;
  const wm = E(on ? '#FFB85A' : '#1A1418'); const w = box(facade, 1.2, 1.9, .1, wm, x, y, .02); box(facade, 1.4, .12, .2, M('#D8C8A0'), x, y - 1.0, .08); box(facade, .06, 1.9, .12, M('#2A1A10'), x, y, .06); WINS.push({ w, wm, fl, c, on }); }
box(facade, 26, .3, .5, M('#D8C8A0'), 0, 3.1, .1); box(facade, 2, 2.8, .1, M(P.woodDk), 1.5, 1.4, .02);
const lanterns = []; for (const x of [-8, 0, 8]) { const g = grp(sC, x, 0, 1.5); box(g, .14, 4, .14, M('#1A1410'), 0, 2, 0); box(g, .5, .5, .5, E('#FFD890'), 0, 4.2, 0); box(g, .7, .1, .7, M('#1A1410'), 0, 4.5, 0); lanterns.push(light(g, '#FFB060', 6, 12, 0, 3.8, .4)); }
const van = truck(sC, 'rent'); van.position.set(-2, 0, 2.2);
const vanTag = plane(van, 1.5, .4, E('#FFFFFF', led('RÜCKGABE 20:00', 80, 20, '#FF3A2A', { size: 12 })), -.7, 3.25, 1.2);
const clockC = grp(sC, 4.2, 0, 2.6); box(clockC, .12, 3, .12, M('#1A1410'), 0, 1.5, 0); const clockTex = canvasTex(48, 20, () => {}); plane(clockC, 1.5, .62, E('#FFFFFF', clockTex), 0, 3.2, .07); box(clockC, 1.6, .72, .1, M('#1A1410'), 0, 3.2, 0);
const khT = truck(sC, 'kh'); const khSign = plane(khT, 3.2, .6, E('#FFFFFF', led('KISTENHELD', 150, 24, P.orange, { size: 17, frame: P.yel })), -1.5, 3.7, 1.0); box(khT, 3.4, .7, .1, M('#140A06'), -1.5, 3.7, .95);
const crew = [0, 1, 2, 3].map(i => person(sC, { shirt: P.orange, pants: '#1E2A50', cap: i % 2 ? P.blue : null, hair: ['#3A2014', '#C8A060', '#1A1010', '#7A3A1A'][i], hairStyle: i === 2 ? 'long' : 'short', mood: 'happy', logo: true, seed: 10 + i, skin: i === 3 ? '#C08A60' : P.skin, beard: i === 1 }));
const liftG = grp(sC, 0, 0, 0); const liftArm = box(liftG, .3, 13, .3, M('#D8D8D0'), 0, 6.5, 0); const liftPlat = grp(liftG, 0, 0, 0); box(liftPlat, 2.4, .1, 1.1, M('#8A8A90'), 0, 0, 0);
const sofaC = sofa(liftPlat, 0, .05, 0);
const priceA = plane(sC, 4.4, .9, E('#FFFFFF', led('FESTER PREIS', 128, 26, '#FFFFFF', { bg: '#1E7A3A', frame: P.yel, size: 18 })), 0, 0, 0);
const priceB = plane(sC, 6.4, .9, E('#FFFFFF', led('BESICHTIGUNG KOSTENLOS', 250, 26, '#1A1008', { bg: P.yel, frame: '#FFFFFF', size: 17 })), 0, 0, 0);

// D · Draufsicht: Kartons füllen den Teppich
const sD = set(300);
box(sD, 10, .1, 8, Mt(TX.carpet), 0, -.05, 0); box(sD, 10, 1, .2, Mt(TX.panel), 0, .5, -4); box(sD, .2, 1, 8, Mt(TX.panel), -5, .5, 0); box(sD, .2, 1, 8, Mt(TX.panel), 5, .5, 0);
const GRID = []; for (let r = 0; r < 10; r++) for (let c = 0; c < 10; c++) GRID.push(carton(sD, -3.4 + c * .76, 0, -3.1 + r * .62, .95, (r * 10 + c) % 4));
const crewD = [0, 1].map(i => person(sD, { shirt: P.orange, pants: '#1E2A50', cap: P.blue, mood: 'happy', logo: true, seed: 20 + i }));
const lampD = light(sD, '#FFC890', 1.6, 14, 0, 4, 0);

// E · Etikettieren: Kartonstapel nah
const sE = set(400);
box(sE, 8, .1, 6, Mt(TX.carpet), 0, -.05, 0); plane(sE, 8, 3, Mt(TX.panel), 0, 1.5, -2.2);
const stackE = []; for (let i = 0; i < 12; i++) stackE.push(carton(sE, -1.6 + (i % 4) * .7, Math.floor(i / 4) * .47, -1.2, 1, -1));
const labE = [0, 1, 2, 3].map(i => plane(sE, .34, .12, E('#FFFFFF', LABELS[i]), 0, 0, 0));
const handE = grp(sE, 0, 0, 0); box(handE, .16, .14, .1, M(P.skin), 0, 0, 0); box(handE, .16, .4, .14, Mt(fabric(P.orange, 4)), 0, -.25, -.05);
const lampE = wallLamp(sE, 1.8, 2.2, -2.15);
const crewE = person(sE, { x: 1.9, z: -.4, shirt: P.orange, pants: '#1E2A50', hair: '#C8A060', hairStyle: 'long', mood: 'happy', logo: true, seed: 31 });

// G · neue Wohnung als Puppenhaus (Draufsicht schräg): vier Räume, Licht geht an
const sG = set(500);
const RM = [[-2.2, -1.6], [2.2, -1.6], [-2.2, 1.6], [2.2, 1.6]], roomF = [], roomL = [], roomS = [];
const FLOORS = [canvasTex(16, 16, g => { noise(g, 16, 16, '#D8D0C0', .1, 40); g.fillStyle = '#9A9080'; for (let k = 0; k < 16; k += 4) { g.fillRect(k, 0, 1, 16); g.fillRect(0, k, 16, 1); } }, [4, 3]),
  canvasTex(16, 16, g => { noise(g, 16, 16, '#9AC8D8', .1, 41); g.fillStyle = '#6A98A8'; for (let k = 0; k < 16; k += 4) { g.fillRect(k, 0, 1, 16); g.fillRect(0, k, 16, 1); } }, [4, 3]), TX.carpet, TX.wood];
RM.forEach(([x, z], i) => { const f = box(sG, 4.2, .1, 3, Mt(FLOORS[i]), x, 0, z); roomF.push(f); roomL.push(light(sG, '#FFC070', 0, 5, x, 1.6, z)); const s = plane(sG, 1.2, .4, E('#FFFFFF', LABELS[i]), x, 1.3, z); s.rotation.x = -.9; roomS.push(s); });
box(sG, 8.8, 1.1, .12, Mt(TX.paper), 0, .55, -3.1); box(sG, 8.8, 1.1, .12, Mt(TX.paper), 0, .55, 0); box(sG, 8.8, 1.1, .12, Mt(TX.paper), 0, .55, 3.1); box(sG, .12, 1.1, 6.3, Mt(TX.paper), -4.4, .55, 0); box(sG, .12, 1.1, 6.3, Mt(TX.paper), 4.4, .55, 0); box(sG, .12, 1.1, 6.3, Mt(TX.paper), 0, .55, 0);
box(sG, 30, .05, 30, M('#140A06'), 0, -.1, 0);
const HB = []; for (let i = 0; i < 12; i++) HB.push({ g: carton(sG, 0, 0, 0, .8, i % 4), r: i % 4, k: Math.floor(i / 4) });
const sofaG = sofa(sG, 2.2, .05, 2.2); sofaG.scale.setScalar(.6);

// H · Pizza in der neuen Wohnung, Neon ANGEKOMMEN
const sH = set(600);
box(sH, 10, .1, 8, Mt(TX.wood), 0, -.05, 0); plane(sH, 10, 3.4, Mt(TX.plaster), 0, 1.7, -2.6); plane(sH, 8, 3.4, Mt(TX.plaster), -3.6, 1.7, 0, Math.PI / 2); box(sH, 10, .5, .06, Mt(TX.panel), 0, .25, -2.57);
const winH = box(sH, 1.6, 1.4, .05, E('#1A2A50'), 2.6, 1.5, -2.55); for (let i = 0; i < 9; i++) box(sH, .12, .12, .02, E('#FFD070'), 2.0 + (i % 3) * .4, 1.1 + Math.floor(i / 3) * .35, -2.52);
box(sH, 1.7, .08, .1, M(P.woodLt), 2.6, .78, -2.5);
const neon = plane(sH, 2.6, .56, E('#FFFFFF', led('ANGEKOMMEN', 150, 28, '#FF4AA0', { bg: '#1A0810', size: 20, frame: '#FF4AA0' })), .5, 2.3, -2.55);
for (let i = 0; i < 6; i++) carton(sH, -3 + (i % 3) * .7, Math.floor(i / 3) * .47, -2 + (i % 2) * .2, 1, i % 4);
const pizza = grp(sH, 0, .02, .6); box(pizza, .9, .05, .9, Mt(TX.kraft), 0, 0, 0); const pz = new THREE.Mesh(new THREE.CylinderGeometry(.4, .4, .04, 8), Mt(canvasTex(16, 16, g => { noise(g, 16, 16, '#E0A040', .15, 50); const r = rng(51); for (let i = 0; i < 14; i++) { g.fillStyle = r() > .5 ? '#B8281E' : '#3A7A2A'; g.fillRect(r() * 14 | 0, r() * 14 | 0, 2, 2); } }))); pz.position.y = .05; pizza.add(pz);
const lid = box(pizza, .9, .04, .9, Mt(TX.kraft), 0, .45, -.45); lid.rotation.x = -1.4;
const coupleA = person(sH, { x: -.75, z: .5, ry: .55, shirt: '#E8E4DA', pants: '#3A4A7A', hair: '#3A2014', mood: 'joy', seed: 2 });
const coupleB = person(sH, { x: .75, z: .5, ry: -.55, shirt: '#8E1E14', pants: '#2A2A3A', hair: '#D8B060', hairStyle: 'long', mood: 'joy', seed: 44 });
const lampH = grp(sH, -2.6, 0, -1.6); box(lampH, .08, 1.7, .08, M(P.gold), 0, .85, 0); box(lampH, .5, .4, .5, E('#FFD890'), 0, 1.8, 0); light(lampH, '#FFC080', 3, 9, .6, 1.6, 1.4);
const hearts = []; for (let i = 0; i < 7; i++) hearts.push(sprite(sH, HEART, .3));

// ---------- Kamera ----------
function look(px, py, pz, tx, ty, tz, fov = 50) { key.position.set(px + OX - 1.5, py + 2.5, pz + .5); key.target.position.set(tx + OX, ty, tz); cam.position.set(px + OX, py, pz); cam.fov = fov; cam.updateProjectionMatrix(); cam.lookAt(tx + OX, ty, tz); }
function env(fogCol, near, far, hemiSky, hemiInt) { hemiSky = '#FFE6CC'; scene.fog = new THREE.Fog(fogCol, near, far); scene.background = new THREE.Color(fogCol); hemi.color.set(hemiSky); hemi.intensity = hemiInt * 3; }

// ---------- Overlay V7: Pixelschrift nur am Objekt, Betonung mit Bildmitteln im Spielstil (Ring, ✕, Häkchen, Batterie) ----------
const OV = document.getElementById('ov'), O = OV.getContext('2d');
function ptext(s, x, y, size, col, align = 'center') {
  O.save(); O.font = `${size}px ${PXF}`; O.textAlign = align; O.textBaseline = 'middle'; const k = Math.max(3, Math.round(size / 14));
  O.fillStyle = '#0B0B0B'; for (let dx = -k; dx <= k + 3; dx += 1) for (let dy = -k; dy <= k + 3; dy += 1) if (Math.abs(dx) === k || Math.abs(dy) === k || dx > k || dy > k) O.fillText(s, x + dx, y + dy);
  O.fillStyle = col; O.fillText(s, x, y); O.restore(); }
// Zeile als Ganzes (Casino-Zeile, nur für den Firmennamen): [[wort, farbe]], hart eingesetzt ab t0
function line(words, cx, y, size, t, t0) {
  if (t < t0) return; O.save(); O.font = `${size}px ${PXF}`; const sp = O.measureText(' ').width, ws = words.map(w => O.measureText(w[0]).width); O.restore();
  let x = cx - (ws.reduce((a, b) => a + b, 0) + sp * (ws.length - 1)) / 2; words.forEach((w, i) => { ptext(w[0], x, y, size, w[1], 'left'); x += ws[i] + sp; }); }
// 3D-Punkt (lokal im Objekt) -> Bildschirm, damit Markierungen am Objekt kleben
const _v = new THREE.Vector3();
function scr(obj, dx = 0, dy = 0, dz = 0) { obj.updateWorldMatrix(true, false); cam.updateMatrixWorld(); _v.set(dx, dy, dz).applyMatrix4(obj.matrixWorld).project(cam); return [(_v.x + 1) / 2 * W, (1 - _v.y) / 2 * H]; }
// Pixelblöcke mit schwarzer Kontur (wie die Schrift)
function pix(pts, s, col) { const q = Math.max(4, Math.round(s)); O.fillStyle = '#0B0B0B'; pts.forEach(([x, y]) => O.fillRect(Math.round(x - q / 2) - 4, Math.round(y - q / 2) - 4, q + 8, q + 8));
  O.fillStyle = col; pts.forEach(([x, y]) => O.fillRect(Math.round(x - q / 2), Math.round(y - q / 2), q, q)); }
// Pixel-Ring: zieht sich in 0,25 s zu (fertig bei tw), danach Zielmarke gelb/weiß
function pring(t, tw, x, y, r) { if (t < tw - .25) return; const k = eo(lin(t, tw - .25, tw)), rr = r * (1.9 - .9 * k);
  const n = Math.max(16, Math.round(2 * Math.PI * rr / 24)), pts = []; for (let i = 0; i < n; i++) { const a = i / n * Math.PI * 2; pts.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
  pix(pts, 12, t > tw && Math.floor((t - tw) * 4) % 2 ? P.white : P.yel); }
// Grünes Pixel-Häkchen, springt ab tw-0,2 ein (fertig bei tw)
function pcheck(t, tw, x, y, s) { if (t < tw - .2) return; s *= back(lin(t, tw - .2, tw)); const pts = [];
  for (let i = 0; i <= 3; i++) pts.push([x - s * .45 + i * s * .12, y - s * .1 + i * s * .12]); for (let i = 1; i <= 7; i++) pts.push([x - s * .09 + i * s * .09, y + s * .26 - i * s * .1]); pix(pts, s / 6, '#3CD35A'); }
// Batterie-Anzeige statt des Worts „KRAFT“: k = Ladung 0..1
function battery(t, x, y, k) { const w = 300, h = 116;
  O.fillStyle = '#0B0B0B'; O.fillRect(x - 10, y - 10, w + 20, h + 20); O.fillRect(x + w + 4, y + h * .3 - 8, 30, h * .4 + 16);
  O.fillStyle = P.white; O.fillRect(x - 4, y - 4, w + 8, h + 8); O.fillRect(x + w + 4, y + h * .3, 18, h * .4); O.fillStyle = '#0B0B0B'; O.fillRect(x + 6, y + 6, w - 12, h - 12);
  const n = Math.max(1, Math.ceil(5 * k - 1e-6)); for (let i = 0; i < n; i++) { O.fillStyle = n <= 1 ? (Math.floor(t * 5) % 2 ? '#E8243A' : '#5A0E0A') : n <= 2 ? '#E8243A' : '#3CD35A'; O.fillRect(x + 16 + i * 54, y + 16, 44, h - 32); } }
// Handy: Name + rotes ✕ je Absage (statt „BIN KRANK / KANN NICHT“)
function drawPhone(t) { const c = phoneScr.userData.canvas, g = c.getContext('2d'); g.fillStyle = '#10141C'; g.fillRect(0, 0, 40, 72); g.fillStyle = '#2A3448'; g.fillRect(0, 0, 40, 8); g.font = `6px ${PXF}`; g.fillStyle = '#FFFFFF'; g.textAlign = 'left'; g.fillText('CHAT', 2, 6);
  [['TOM', K.freunde, '#2DBE6C'], ['LISA', K.haben, '#2D8BE8'], ['BEN', K.abgesagt, '#E8A020']].forEach(([n, tw, col], i) => { if (t < tw - .45) return; const y = 11 + i * 20;
    g.fillStyle = '#E8E4DA'; g.fillRect(2, y, 36, 17); g.fillStyle = col; g.fillRect(2, y, 3, 17); g.font = `7px ${PXF}`; g.fillStyle = '#10141C'; g.fillText(n, 7, y + 11);
    if (t >= tw - .12) { g.fillStyle = '#E8243A'; for (let k = 0; k < 11; k++) { g.fillRect(25 + k, y + 3 + k, 2, 2); g.fillRect(35 - k, y + 3 + k, 2, 2); } } });
  phoneScr.needsUpdate = true; }
function drawClock(t) { const c = clockTex.userData.canvas, g = c.getContext('2d'); g.fillStyle = '#140A06'; g.fillRect(0, 0, 48, 20); const m = Math.floor(mix(17 * 60 + 12, 19 * 60 + 58, eo(lin(t, K.wagen - .2, K.zurueck))));
  g.font = `16px ${PXF}`; g.fillStyle = m > 19 * 60 + 30 ? '#FF3A2A' : P.yel; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(`${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}`, 24, 11); clockTex.needsUpdate = true; }
const flatAnchor = grp(sB, .47, .45, -2.4);   // Mitte der flachen Kartons (für den Ring)

// ================= Einstellungen (harte Schnitte wie im Original, alle aus K) =================
const T = CUT;
function shot(t) {
  let s = 0; while (s + 1 < T.length && t >= T[s + 1]) s++;
  const u = lin(t, T[s], T[s + 1] ?? DUR);
  O.clearRect(0, 0, W, H); SNAP.value.set(RW / 2.2, RH / 2.2);
  if (s === 0) { // Treppenhaus, Totale von unten: LED „SAMSTAG 08:00“ springt an, Ring um das Aufzug-Schild
    vis(sA); env('#0E0604', 6, 22, '#FFD2A0', .5);
    pose(man, t, { push: 1 }); man.body.rotation.x = -.12; man.mood('stress'); man.g.position.set(3.95, 2.4, -.8); man.g.rotation.y = -1.5;
    sofaA.position.set(2.55 + Math.sin(t * 7) * .03, 2.05, -.75); sofaA.rotation.set(0, .42, .5 + Math.sin(t * 5) * .02);
    bangA.visible = false; lampA1.intensity = (3.2 + Math.sin(t * 40) * .3) * LSC;
    const ledOn = t >= K.samstag || (t > K.samstag - .25 && Math.floor(t * 30) % 3 !== 0); ledSA.material.color.set(ledOn ? '#FFFFFF' : '#2A1A10');
    const px = mix(-3.6, -2.9, u); look(px, mix(1.1, 1.3, u), 3.6, mix(.4, .1, u), 2.0, -1.2, 58);
    render();
    const [lx, ly] = scr(liftSign), [ex] = scr(liftSign, .62, 0, 0); pring(t, K.aufzug, lx, ly, Math.abs(ex - lx));
  } else if (s === 1) { // Sofa steckt fest – nah, „!“
    vis(sA); env('#0E0604', 4, 16, '#FFD2A0', .5);
    const shove = Math.max(0, Math.sin(t * 6)) * .06;
    pose(man, t, { push: 1 }); man.body.rotation.x = -.12 - shove * 2; man.mood(t > K.fest - .2 ? 'shock' : 'stress'); man.g.position.set(3.95, 2.4, -.8); man.g.rotation.y = -1.5;
    sofaA.position.set(2.55 + Math.sin(t * 9) * .02, 2.05, -.75); sofaA.rotation.set(0, .42, .5);
    bangA.visible = t > K.fest - .2; bangA.position.set(3.9, 4.72 + Math.sin(t * 8) * .04, -.6); bangA.scale.set(.25, .5 * (t > K.fest - .2 ? Math.max(.3, back(lin(t, K.fest - .2, K.fest))) : 1), 1);
    look(mix(1.8, 2.0, u), mix(4.1, 4.2, u), mix(1.9, 1.6, u), 3.5, 3.85, -.8, 50);
    render();
  } else if (s === 2) { // nichts gepackt: Wohnzimmer voll, Kartons flach -> Ring um die flachen Kartons
    vis(sB); env('#0E0604', 6, 18, '#FFD2A0', .55); lampBL.intensity = 5 * LSC;
    man2.g.position.set(-.85, 0, -.5); man2.g.rotation.y = .2; pose(man2, t, { slump: .6 }); man2.mood('sad'); phone.visible = false; handB.visible = false;
    look(mix(3.4, 3.0, u), 1.7, mix(3.4, 3.1, u), -1.2, 1.2, -2.4, 55);
    render();
    const [fx, fy] = scr(flatAnchor), [ex] = scr(flatAnchor, .75, 0, 0); pring(t, K.nichts, fx, fy, Math.abs(ex - fx));
  } else if (s === 3) { // Handy: drei Absagen, je ein rotes ✕
    vis(sB); env('#0E0604', 3, 12, '#FFD2A0', .6); man2.g.visible = false; phone.visible = true; handB.visible = true;
    const jolt = t > K.abgesagt - .12 ? Math.sin((t - K.abgesagt) * 60) * .04 * (1 - lin(t, K.abgesagt, K.abgesagt + .35)) : 0;
    drawPhone(t); phone.position.set(.1 + jolt * .5, 1.3, .1); phone.rotation.set(-.15, .1, .05 + Math.sin(t * 2) * .02 + jolt); handB.position.set(.1 + jolt * .5, 1.02, .08); handB.rotation.copy(phone.rotation);
    look(.35, 1.55, mix(1.05, .95, u), .1, 1.3, .1, 50);
    render(); man2.g.visible = true;
  } else if (s === 4) { // Mietwagen, Uhr rast, RÜCKGABE-Schild blinkt auf „zurück“
    vis(sC); env('#1A0E14', 12, 45, '#FFB890', .5); khT.visible = false; van.visible = true; liftG.visible = false; crew.forEach(c => c.g.visible = false); priceA.visible = priceB.visible = false;
    drawClock(t); clockC.visible = true; vanTag.visible = true; vanTag.scale.setScalar(1.8); vanTag.position.set(-.7, 3.6, 1.2); vanTag.rotation.y = .85;
    vanTag.material.color.set(t > K.zurueck - .2 && Math.floor((t - K.zurueck + .2) * 7) % 2 === 1 ? '#5A2018' : '#FFFFFF');
    look(mix(6.5, 5.8, u), 1.6, mix(9, 8.2, u), 0, 2.2, 1.8, 50);
    render();
  } else if (s === 5) { // Montag: müdes Gesicht neben dem Kalender „MO“, Batterie läuft leer
    vis(sB); env('#0E0604', 3, 12, '#FFD2A0', .6); phone.visible = false; handB.visible = false; lampBL.intensity = 2 * LSC;
    man2.g.visible = true; man2.g.position.set(-.62, 0, -1.6); man2.g.rotation.y = .3; pose(man2, t, { slump: .4 + .3 * u }); man2.mood(t > K.job - .3 ? 'tired' : 'sad');
    look(mix(-.1, 0, u), 2.0, mix(-.1, -.45, u), -.12, 1.95, -2.6, 46);
    render();
    const [cx, cy] = scr(cal, 0, .1, 0), [ex] = scr(cal, .41, .1, 0); pring(t, K.montag, cx, cy, Math.abs(ex - cx));
    battery(t, 1520, 86, 1 - .8 * lin(t, K.montag + .3, K.job));
  } else if (s === 6) { // Kistenheld kommt: Licht an, Wagen fährt ein und steht auf dem Namen, Crew
    vis(sC); env('#1A0E14', 14, 50, '#FFC8A0', .75); van.visible = false; clockC.visible = false; khT.visible = true; liftG.visible = false; priceA.visible = priceB.visible = false;
    const drive = eo(lin(t, K.mit - .27, K.kistenheld)); khT.position.set(mix(-9.5, -1, drive), 0, 2.4);
    crew.forEach((c, i) => { const k = eo(lin(t, K.anders - .5 + i * .12, K.anders + .1 + i * .12)); c.g.visible = t > K.anders - .5 + i * .12; c.g.position.set(-5.4 + i * 1.1, 0, mix(2.4, 4.8, k)); c.g.rotation.y = .1; pose(c, t, { walk: 1 - k, ph: i }); c.mood('happy'); });
    const on = t > K.kistenheld - .25; lanterns.forEach(L => L.intensity = (on ? 7 : 1.5) * LSC); WINS.forEach(w => w.wm.color.set(on || w.on ? '#FFB85A' : '#1A1418'));
    look(mix(-1.2, -1.8, u), 1.5, mix(10.5, 9.4, u), -3.6, 1.7, 3.6, 50);
    render();
  } else if (s === 7) { // Draufsicht: 100 Kartons an 1 Tag
    vis(sD); env('#0E0604', 8, 30, '#FFD2A0', .7);
    const a0 = K.n100 - .3, a1 = K.tag, n = Math.floor(mix(0, 100, lin(t, a0, a1)));
    GRID.forEach((b, i) => { const t0 = a0 + (a1 - a0) * i / 100, k = back(lin(t, t0, t0 + .15)); b.visible = k > 0; b.scale.setScalar(.95 * Math.max(.01, k)); });
    crewD.forEach((c, i) => { c.g.position.set(mix(-3, 3, (u + i * .5) % 1), 0, i ? 2.9 : -3.6); c.g.rotation.y = Math.PI / 2; pose(c, t, { walk: 1, carry: 1, ph: i }); });
    look(0, 10.5 - u * .8, .3, 0, 0, -.2, 50);
    render();
    if (t > K.n100 - .25) ptext('100', 960, 190, 150 * (.6 + .4 * back(lin(t, K.n100 - .25, K.n100))), P.yel);
    O.fillStyle = '#0B0B0B'; O.fillRect(650, 300, 520, 40); O.fillStyle = P.yel; O.fillRect(657, 307, 506 * n / 100, 26);
    if (t > K.tag - .2) ptext('1 TAG', 1195, 320, 84 * (.6 + .4 * back(lin(t, K.tag - .2, K.tag))), P.white, 'left');
  } else if (s === 8) { // Etiketten: jeder Karton sein Zimmer, das letzte auf „beschriftet“
    vis(sE); env('#0E0604', 3, 12, '#FFD2A0', .6);
    const e0 = K.jeder - .2, st = (K.beschriftet - .05 - K.jeder) / 3;
    labE.forEach((L, i) => { const b = stackE[5 + i % 3 + (i === 3 ? 3 : 0)], t0 = e0 + i * st, k = eo(lin(t, t0, t0 + .2)); L.visible = t > t0; L.scale.setScalar(1.7); L.position.set(b.position.x, b.position.y + .25, b.position.z + .26 + (1 - k) * .6); L.rotation.y = (1 - k) * .8; });
    const act = Math.min(3, Math.floor(clamp((t - e0) / st, 0, 3.99))), tb = stackE[5 + act % 3 + (act === 3 ? 3 : 0)];
    handE.position.set(tb.position.x + .05, tb.position.y + .33 + Math.max(0, Math.sin(t * 14)) * .06, tb.position.z + .42); handE.rotation.set(-.6, 0, 0);
    pose(crewE, t, { carry: .6 }); crewE.mood('happy');
    look(mix(-.6, -.2, u), 1.5, mix(2.8, 2.5, u), -.4, .7, -1.2, 50);
    render();
  } else if (s === 9) { // Möbellift: Sofa fährt hoch, durchs Fenster
    vis(sC); env('#1A0E14', 14, 55, '#FFC8A0', .75); van.visible = false; clockC.visible = false; khT.visible = true; khT.position.set(-1, 0, 2.4); liftG.visible = true; priceA.visible = priceB.visible = false;
    crew.forEach((c, i) => { c.g.visible = i < 2; c.g.position.set(2.5 + i * 1.2, 0, 3.4); c.g.rotation.y = -.3; pose(c, t, { wave: i ? .7 : 0, ph: i }); c.mood('happy'); });
    liftG.position.set(-1.6, 2.3, .2); liftArm.rotation.set(0, 0, 0); liftG.rotation.x = -.3;
    const up = eio(lin(t, K.lift - .5, K.fenster)), into = eio(lin(t, K.fenster, K.fenster + .4)); liftPlat.position.set(0, mix(.3, 9.3, up), 0); liftPlat.rotation.x = .3; sofaC.position.z = mix(0, -1.4, into); sofaC.rotation.y = 0;
    WINS.forEach(w => w.wm.color.set('#FFB85A'));
    look(mix(5, 3.6, up), mix(3.5, 10.2, up), mix(11, 6, up), -1.6, mix(3, 10.8, up), mix(0, -2.6, up), 50);
    render();
  } else if (s === 10) { // Puppenhaus: alles im richtigen Raum -> Licht + grünes Häkchen je Raum, das letzte auf „Raum“
    vis(sG); env('#0E0604', 10, 30, '#FFD2A0', .45);
    HB.forEach(b => { const t0 = K.abends + .1 + (b.r * .22 + b.k * .08) * 1.1, k = eio(lin(t, t0, t0 + .6)); const [rx, rz] = RM[b.r]; const tx = rx + (b.k - 1) * .8, tz = rz + (b.r < 2 ? -.5 : .4);
      b.g.position.set(mix(0, tx, k), Math.sin(Math.PI * k) * .9, mix(4.8, tz, k)); b.g.rotation.y = (1 - k) * 2; });
    const cw = i => K.raum - .75 + i * .25;
    RM.forEach((r, i) => { const on = lin(t, cw(i) - .2, cw(i) - .1); roomL[i].intensity = 9 * on * LSC; roomS[i].visible = on > 0; });
    look(0, mix(8.6, 8, u), mix(7.2, 6.6, u), 0, 0, .2, 50);
    render();
    RM.forEach((r, i) => { const [x, y] = scr(roomS[i], .85, 0, 0); pcheck(t, cw(i), x, y, 66); });
  } else if (s === 11) { // Pizza, Herzen seitlich, Zoom aufs Neon ANGEKOMMEN
    vis(sH); env('#0E0604', 4, 14, '#FFD2A0', .55);
    pose(coupleA, t, { sit: 1, eat: 1 }); pose(coupleB, t, { sit: 1, eat: 1, ph: 1.5 }); coupleA.mood('joy'); coupleB.mood(t > K.wohnung - .1 ? 'joy' : 'happy');
    neon.material.color.set(t > K.angekommen - .25 ? (t < K.angekommen && Math.floor(t * 24) % 2 ? '#301018' : (Math.floor(t * 6) % 9 ? '#FFFFFF' : '#C88AA8')) : '#301018');
    hearts.forEach((h, i) => { const q = ((t - K.wohnung + .3) * .5 + i / 7) % 1; h.visible = t > K.wohnung - .3; h.position.set((i % 2 ? 1.7 : -1.35) + ((i * .23) % .4) + Math.sin(t * 2 + i) * .12, 1.3 + q * 1.6, .6); h.scale.set(.34 * Math.sin(Math.PI * q) + .01, .3 * Math.sin(Math.PI * q) + .01, 1); });
    const z = eio(lin(t, K.angekommen - .35, K.angekommen));
    look(mix(mix(0, .15, u), .35, z), mix(mix(1.5, 1.45, u), 1.85, z), mix(mix(3.6, 3.2, u), 2.4, z), mix(0, .4, z), mix(1.05, 1.9, z), mix(-.4, -2.55, z), mix(48, 44, z));
    render();
  } else { // Schluss: Wagen, Crew winkt; Name als Casino-Zeile, Angebot als LED-Tafel am Haus, Kontakt
    vis(sC); env('#1A0E14', 14, 55, '#FFC8A0', .8); van.visible = false; clockC.visible = false; khT.visible = true; khT.position.set(-1, 0, 2.4); liftG.visible = false;
    crew.forEach((c, i) => { c.g.visible = true; c.g.position.set(-5.8 + i * 1.15, 0, 4.6 + (i % 2) * .2); c.g.rotation.y = .15; pose(c, t, { wave: 1, ph: i * .8 }); c.mood('joy'); });
    priceA.visible = false; priceB.visible = t > K.kostenlose - .25 && !(t < K.kostenlose && Math.floor(t * 16) % 2); priceB.position.set(-2.2, 6.7, 1.4); priceB.scale.setScalar(1.3);
    lanterns.forEach(L => L.intensity = 7 * LSC); WINS.forEach(w => w.wm.color.set('#FFB85A'));
    look(mix(-1.2, -1.8, u), 2.6, mix(13.5, 12.4, u), -2.2, 3.6, 2.4, 50);
    render();
    line([['KISTENHELD', P.orange], ['UMZÜGE', P.white]], 960, 900, 110, t, K.schluss - .12);
    if (t > K.fester - .2) ptext('kistenheld-umzuege.de  ·  0621 43 21 00', 960, 1012, 50, P.white);
  }
  post.uniforms.uFade.value = Math.min(lin(t, 0, .15), 1 - lin(t, DUR - .45, DUR));
  renderer.render(postScene, postCam);
  if (post.uniforms.uFade.value < 1) { O.save(); O.globalCompositeOperation = 'destination-out'; O.globalAlpha = 1 - post.uniforms.uFade.value; O.fillRect(0, 0, W, H); O.restore(); }
}
function render() { renderer.setRenderTarget(rt); renderer.render(scene, cam); renderer.setRenderTarget(null); }

window.FILM = { duration: DUR, width: W, height: H, ready: (async () => { await document.fonts.load('40px PX'); await document.fonts.ready;
  // Texturen mit Schrift nach dem Laden der Schrift neu zeichnen: alles einmal neu aufbauen ist am einfachsten → Seite lädt Schrift vor dem Modul
  shot(0); return true; })(), seek(t) { shot(t); } };
