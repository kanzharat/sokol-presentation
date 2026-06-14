# Builds sokol-deck.html — full investor deck (21 slides, 4 blocks, morph transitions).
# Style G: full-bleed photos + telemetry/HUD. Track block = inner morph carousel (official contours).
import json, re, os

ROOT = r"C:\Users\user\presentation"
BASECSS = open(r"C:\Users\user\.claude\skills\frontend-slides\viewport-base.css", encoding="utf-8").read()

# ---------- official tracks (same data pipeline as components/_build_roads.py) ----------
t = json.load(open(r"C:\Users\user\AppData\Local\Temp\sokol_svg\tracks.json", encoding="utf-8"))
def trk(key, render, sw):
    v = t[key]
    return {"vb": v["viewBox"], "paths": v["paths"], "render": render, "sw": sw}

TRACKS = [
 dict(id="ring",  c="#2aa8ff", kic="TRACK 01 · MAIN CIRCUIT", nm="Main Circuit", en="Sokol International Circuit",
      desc="The flagship circuit for cars and motorcycles, designed by Hermann Tilke. Ready to host MotoGP, WTCC, DTM and Superbike rounds.",
      specs=[["4,495 m","total length"],["15 m","track width"],["300+ km/h","top speed on the straight"],["5 / 8","right / left corners"]],
      **trk("main-circuit","stroke",420)),
 dict(id="drag",  c="#ff8c42", kic="TRACK 02 · DRAG STRIP", nm="Drag Strip", en="Drag Racing Strip",
      desc="A 402 m strip with safety barriers and professional timing. Return lanes keep the runs going without delays.",
      specs=[["402 m","drag strip"],["866 m","total length"],["348 m","braking zone"],["2,500–3,000","grandstand seats"]],
      **trk("drag-strip","fill",0)),
 dict(id="drift", c="#8b7bff", kic="TRACK 03 · DRIFT ARENA", nm="Drift Arena", en="Drift Arena",
      desc="A purpose-built arena for controlled slides with dedicated barriers and run-off zones. Home to the national drift championship.",
      specs=[["16,000 m²","arena area"],["up to 1,500","grandstand seats"],["15+","events per year"],["FIA","safety standards"]],
      **trk("drift-arena","stroke",360)),
 dict(id="kart",  c="#34d058", kic="TRACK 04 · KARTING", nm="Karting Track", en="Kartodrome",
      desc="A compact racing kart circuit — almost 3× shorter than the Main Circuit. The country's only telemetry-equipped kartodrome: 7 layouts and 12 pit boxes.",
      specs=[["1,650 m","track length"],["10 m","width"],["14 / 10","right / left corners"],["7","layouts"]],
      **trk("kartodrom","fill",0)),
 dict(id="moto",  c="#ed2d91", kic="TRACK 05 · MOTOCROSS", nm="Motocross", en="Motocross Track", gen=True,
      desc="A dirt motocross track with jumps, berms and spectator zones along the key sections. A venue for national and regional rounds.",
      specs=[["~1,500 m","lap length"],["dirt","surface"],["12+","jumps & waves"],["MX1 / MX2","classes"]],
      **trk("motocross","stroke",420)),
 dict(id="off",   c="#98ca48", kic="TRACK 06 · OFF-ROAD", nm="Off-road", en="Off-road Park", gen=True,
      desc="An off-road proving ground with natural terrain: climbs, descents and rocky sections. A format for 4×4 and ATV test drives and corporate programmes.",
      specs=[["4×4 / ATV","vehicle formats"],["terrain","natural obstacles"],["test drives","partner programmes"],["all year","season"]],
      **trk("offroad","stroke",470)),
]

def mini_svg(tr, size=150):
    body = "".join(
        f'<path d="{d}" fill="{tr["c"]}" fill-rule="evenodd"/>' if tr["render"]=="fill"
        else f'<path d="{d}" fill="none" stroke="{tr["c"]}" stroke-width="{tr["sw"]*2.2}" stroke-linecap="round" stroke-linejoin="round"/>'
        for d in tr["paths"])
    return f'<svg viewBox="{tr["vb"]}" preserveAspectRatio="xMidYMid meet" style="width:{size}px;height:{int(size*.72)}px;overflow:visible">{body}</svg>'

MINIS = "".join(
    f'<div class="mini rv d{i+2}">{mini_svg(tr, 185)}<span class="mname">{tr["nm"]}</span>'
    + ('<span class="tlkb">TILKE</span>' if i == 0 else '<span class="tlkb gray">SOKOL TEAM</span>')
    + '</div>'
    for i, tr in enumerate(TRACKS))

# ---------- scattered racing logos for the events drum ----------
import re as _re
def _svg_logo(slug):
    p = rf"C:\Users\user\presentation\assets\logos\{slug}.svg"
    s = open(p, encoding="utf-8").read()
    s = _re.sub(r'\s(width|height)="[^"]*"', '', s)  # keep original brand colour
    return s
# (type, content, x%, y%, size_px, opacity, rotate_deg) — real brand SVGs + event wordmarks
SCATTER = [
 # real logo files (white-on-dark, supplied by client) + text plaques for the rest
 ('img','real-timeattack', 14,15,235,1,-3),
 ('img','real-gorilladrift',29,13,165,1, 0),
 ('img','real-dragwars',   88,16,200,1, 4),
 ('word','SMP KARTING',    10,42,  0,.85,-2),
 ('img','real-burnoutz',   89,44,255,1, 2),
 ('img','real-aagc',       14,64,225,1,-2),
 ('img','real-sbk',        87,66,150,1, 2),
]
def _logo_html():
    out=[]
    for t,c,x,y,sz,op,rot in SCATTER:
        st=f"left:{x}%;top:{y}%;transform:translate(-50%,-50%) rotate({rot}deg);opacity:{op}"
        if t=='img':
            out.append(f'<div class="dlg" style="{st};width:{sz}px"><img src="assets/logos/{c}.png" alt=""></div>')
        elif t=='svg':
            out.append(f'<div class="dlg" style="{st};width:{sz}px">{_svg_logo(c)}</div>')
        elif t=='gorilla':
            out.append(f'<div class="dlg dge" style="{st}"><span class="m">🦍</span><span class="t">GORILLA<small>ENERGY</small></span></div>')
        else:
            out.append(f'<div class="dlg dlw" style="{st}">{c}</div>')
    return "".join(out)
DRUMLOGOS = _logo_html()

# ---------- racing tachometer gauge for the events drum ----------
import math as _m
def _drum_gauge():
    cx=cy=350
    YRS=['2016','2019','2024','2025','2026']
    ANG=[-105,-52,0,52,105]
    def pol(r,th):
        a=_m.radians(th); return (cx+r*_m.sin(a), cy-r*_m.cos(a))
    parts=[]
    parts.append('<svg viewBox="0 0 700 700" xmlns="http://www.w3.org/2000/svg">')
    parts.append('<defs><linearGradient id="gaugeg" x1="0" y1="1" x2="1" y2="0">'
                 '<stop offset="0" stop-color="#2aa8ff"/><stop offset=".55" stop-color="#ff8c42"/><stop offset="1" stop-color="#ff3b3b"/></linearGradient></defs>')
    # outer faint ring + recessed channel = hollow drum feel
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="318" fill="none" stroke="#161d2c" stroke-width="44"/>')
    # dark base arc (240deg, open bottom)
    s=pol(296,-120); e=pol(296,120)
    parts.append(f'<path d="M {s[0]:.1f} {s[1]:.1f} A 296 296 0 1 1 {e[0]:.1f} {e[1]:.1f}" fill="none" stroke="#222c40" stroke-width="26" stroke-linecap="round"/>')
    # racing gradient arc
    parts.append(f'<path d="M {s[0]:.1f} {s[1]:.1f} A 296 296 0 1 1 {e[0]:.1f} {e[1]:.1f}" fill="none" stroke="url(#gaugeg)" stroke-width="8" stroke-linecap="round" opacity=".9"/>')
    # minor ticks
    for k in range(-120,121,10):
        a,b=pol(305,k),pol(285,k)
        parts.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#46546f" stroke-width="2"/>')
    # major ticks + year labels at each year angle
    for i,(yr,th) in enumerate(zip(YRS,ANG)):
        a,b=pol(312,th),pol(276,th)
        parts.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#7e8aa6" stroke-width="5"/>')
        lx,ly=pol(232,th)
        parts.append(f'<text class="dyl" id="dyl{i}" x="{lx:.1f}" y="{ly+14:.1f}" text-anchor="middle" font-family="Orbitron, sans-serif" font-weight="900" font-size="34" fill="#5d6b8a">{yr}</text>')
    # needle (points up by default; rotated by JS to active year)
    parts.append('<g id="dneedle">'
                 f'<polygon points="{cx-10},{cy+28} {cx+10},{cy+28} {cx+4},{cy-250} {cx-4},{cy-250}" fill="#ff8c42"/>'
                 f'<circle cx="{cx}" cy="{cy}" r="16" fill="#ff8c42"/></g>')
    # hub: hollow center with the active year
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="86" fill="#0a0d15" stroke="#2a3450" stroke-width="2"/>')
    parts.append(f'<text id="dyear" x="{cx}" y="{cy+20}" text-anchor="middle" font-family="Orbitron, sans-serif" font-weight="900" font-size="62" fill="#fff">2016</text>')
    parts.append('</svg>')
    return "".join(parts)
DRUMGAUGE = _drum_gauge()

# ---------- official full map ----------
svg = open(r"C:\Users\user\AppData\Local\Temp\sokol_svg\full_map.svg", encoding="utf-8").read()
svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.S)
ZONES = {"main_circle":"ring","karting":"kart","drag_strip":"drag","drift_arena":"drift","motocross":"moto",
         "offroad":"off","paintball":"paint","museum":"museum","hotel_restaurant":"hotel","parking":"park","sokol_roads":"road"}
for gid, z in ZONES.items():
    svg = svg.replace(f'<g id="{gid}"', f'<g id="{gid}" class="mz" data-mz="{z}"')
svg = svg.replace("<svg id=", '<svg preserveAspectRatio="xMidYMid meet" id=', 1)

HTML = r"""<!DOCTYPE html>
<!-- ============================================================
     SOKOL INTERNATIONAL CIRCUIT — investor deck (RU/EN, speaker-led)
     Style G: full-bleed photo + telemetry/HUD · 21 slides · 4 blocks
     Morph transitions; Block B tracks = inner morph carousel with
     OFFICIAL sokol.kz contours. Built by _build_deck.py
     Keys: ← → / Space · E = edit mode · Ctrl+S = save edited copy
     ============================================================ -->
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SOKOL INTERNATIONAL CIRCUIT — FIA Visit</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Play:wght@400;700&family=Russo+One&family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
/* === MANDATORY FIXED-STAGE BASE (viewport-base.css, full) === */
__BASECSS__

/* === DECK THEME === */
:root{--stage-bg:#000;--slide-bg:#0a0a0f;--night:#0a0a0f;--primary:#115ffc;--accent:#ff5733;--warm:#ff8c42;
 --ink:#f4f6ff;--muted:#8a91a6;--en:#a9b8dc;--line:#222a3a;--mono:'JetBrains Mono',monospace}
.slide{font-family:'Inter',sans-serif;color:var(--ink);background:var(--slide-bg)}

/* === MORPH SLIDE TRANSITIONS === */
.slide{transition:opacity .65s ease,transform .65s cubic-bezier(.45,.05,.18,1),filter .65s ease;transform:scale(.965);filter:blur(12px)}
.slide.active{transform:scale(1);filter:blur(0)}
.slide.leaving{visibility:visible;opacity:0;transform:scale(1.06);filter:blur(10px);z-index:2;pointer-events:none}
.notrans .slide{transition:none}

/* === REVEAL === */
.rv{opacity:0;transform:translateY(26px)}
.slide.active .rv{animation:rvup .6s cubic-bezier(.2,.8,.2,1) forwards}
.slide.active .d1{animation-delay:.1s}.slide.active .d2{animation-delay:.2s}.slide.active .d3{animation-delay:.3s}
.slide.active .d4{animation-delay:.4s}.slide.active .d5{animation-delay:.5s}.slide.active .d6{animation-delay:.6s}.slide.active .d7{animation-delay:.7s}
@keyframes rvup{to{opacity:1;transform:translateY(0)}}
.notrans .rv,.notrans .slide.active .rv{animation:none;opacity:1;transform:none}

/* === HUD CHROME: slide number only (prominent, top-right) === */
.hud{position:absolute;top:34px;right:54px;z-index:40;display:flex;align-items:baseline;gap:6px;pointer-events:none;
 padding:10px 20px;border:1px solid #2a3650;border-radius:12px;background:rgba(10,13,22,.78);backdrop-filter:blur(4px)}
.hud .cnt{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:34px;color:#fff;letter-spacing:.04em;line-height:1}
.hud .cnt span{color:#5d6b8a;font-size:20px;font-weight:700}
.ticks::before,.ticks::after{content:"";position:absolute;width:26px;height:26px;border:2px solid rgba(255,255,255,.28);z-index:39}
.ticks::before{left:24px;top:104px;border-right:0;border-bottom:0}
.ticks::after{right:24px;bottom:24px;border-left:0;border-top:0}
.scan{position:absolute;left:0;right:0;height:120px;z-index:5;pointer-events:none;opacity:.5;
 background:linear-gradient(180deg,transparent,rgba(17,95,252,.07),transparent);animation:scanmv 7s linear infinite}
@keyframes scanmv{0%{top:-120px}100%{top:1080px}}
.notrans .scan{animation:none;top:400px}
.grid-tel{display:none;position:absolute;inset:0;z-index:4;pointer-events:none;opacity:.16;
 background:linear-gradient(transparent 95%,rgba(140,170,255,.5) 95%) 0 0/100% 108px,
            linear-gradient(90deg,transparent 95%,rgba(140,170,255,.5) 95%) 0 0/108px 100%}

/* === SHARED === */
.bgimg{position:absolute;inset:0;background-size:cover;background-position:center;z-index:0}
.dim{position:absolute;inset:0;z-index:1;background:linear-gradient(110deg,rgba(7,8,13,.93) 30%,rgba(7,8,13,.55) 60%,rgba(7,8,13,.35))}
.dim.full{background:linear-gradient(180deg,rgba(7,8,13,.72),rgba(7,8,13,.82))}
.wrap{position:absolute;inset:0;z-index:10;padding:150px 120px 110px}
.kic{font-family:var(--mono);font-size:17px;letter-spacing:.34em;color:#74a9ff;text-transform:uppercase;text-shadow:0 1px 10px rgba(5,8,16,.8)}
.kic.blue{color:#6ea8ff}
h1.big{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:88px;line-height:1.02;text-transform:uppercase;margin:18px 0 10px}
h1.giant{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:128px;line-height:.98;text-transform:uppercase;margin:22px 0 14px;
 color:transparent;-webkit-text-stroke:2.5px #fff;text-shadow:0 0 44px rgba(17,95,252,.5)}
h1 .fill{color:#fff;-webkit-text-stroke:0}
.en-sub{font-family:'Play';font-size:28px;color:var(--en);letter-spacing:.06em}
.lead{font-weight:300;font-size:27px;line-height:1.6;color:#c9cedd;max-width:900px}
.chips{display:flex;gap:18px;flex-wrap:wrap;margin-top:46px}
.chip{border:1px solid #2a3650;background:rgba(13,18,30,.72);border-radius:12px;padding:18px 26px;font-size:21px;color:#dfe5f2}
.chip b{color:#fff;font-family:'Orbitron','Russo One',sans-serif;font-weight:700;font-size:23px;display:block;margin-bottom:4px}
.chip i{display:block;font-style:normal;font-size:19px;color:var(--en);letter-spacing:.04em;margin-top:8px}
.genb{display:inline-block;font-family:var(--mono);font-size:14px;letter-spacing:.16em;text-transform:uppercase;
 color:#ffb84d;border:1px dashed rgba(255,184,77,.5);border-radius:6px;padding:7px 14px}
.spec{border-left:4px solid var(--primary);padding-left:18px}
.spec b{display:block;font-family:'Orbitron','Russo One',sans-serif;font-weight:700;font-size:38px;color:#fff}
.spec span{font-size:17px;color:var(--muted)}
.photo{border-radius:18px;background-size:cover;background-position:center;border:1px solid #2a3346;box-shadow:0 30px 70px rgba(0,0,0,.55)}

/* === TITLE / FINAL === */
.s-title .hero{position:absolute;left:120px;bottom:200px;z-index:10;max-width:1500px}
.s-title .giant{text-shadow:none}
.s-final .hud{display:none}
.s-title .logo-top{position:absolute;top:110px;left:120px;z-index:10;height:110px;width:auto;max-width:none}
.tick-line{position:absolute;left:0;right:0;bottom:64px;z-index:12;overflow:hidden;border-top:1px solid #232c40;border-bottom:1px solid #232c40;
 background:rgba(8,10,16,.82);height:58px;display:flex;align-items:center}
.tick-line .in{display:flex;gap:64px;white-space:nowrap;font-family:var(--mono);font-size:17px;letter-spacing:.3em;color:#9fb4dd;
 text-transform:uppercase;width:100%;justify-content:center}
.tick-line .in i{color:var(--accent);font-style:normal}
/* === PHOTO CARDS (consolidated infrastructure) === */
.pgrid{display:flex;gap:26px;margin-top:54px}
.pcard{flex:1;border:1px solid #2a3650;border-radius:16px;background:rgba(13,18,30,.72);overflow:hidden}
.pcard .pimg{height:215px;background-size:cover;background-position:center;border-bottom:1px solid #2a3346}
.pcard .pimg.ph{display:flex;align-items:center;justify-content:center;border-bottom:1px dashed rgba(255,184,77,.45);
 color:#ffb84d;font-family:var(--mono);font-size:13px;letter-spacing:.2em;background:#0d1220}
.pcard .pbody{padding:20px 22px}
.pcard b{font-family:'Russo One',sans-serif;font-weight:400;font-size:23px;color:#fff;display:block;margin-bottom:8px}
.pcard span{font-size:18px;color:#aab3c8;line-height:1.45;display:block}
/* === DUO: two big facility cards per slide === */
.duo{display:flex;gap:44px;margin-top:54px}
.dcard{flex:1;border:1px solid #2a3650;border-radius:18px;overflow:hidden;background:rgba(13,18,30,.72)}
.dcard .dimg{height:470px;background-size:cover;background-position:center;border-bottom:1px solid #2a3346}
.dcard .dimg.ph{display:flex;align-items:center;justify-content:center;border-bottom:1px dashed rgba(255,184,77,.45);
 color:#ffb84d;font-family:var(--mono);font-size:15px;letter-spacing:.22em;background:#0d1220}
.dcard .dbody{padding:28px 34px}
.dcard .dbody{padding:24px 32px 28px}
.dcard b{font-family:'Russo One',sans-serif;font-weight:400;font-size:30px;color:#fff;display:block;margin-bottom:12px}
.dcard span{font-size:22px;color:#aab3c8;line-height:1.5;display:block}
.dcard ul{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:1fr 1fr;gap:7px 22px}
.dcard li{font-size:19px;color:#bcc6dd;line-height:1.35;padding-left:18px;position:relative}
.dcard li::before{content:"";position:absolute;left:0;top:9px;width:7px;height:7px;border-radius:50%;background:var(--accentc,#5e9bff)}
/* === LEISURE statement intro === */
.s-leisure-intro .big{font-size:96px}
/* === BIRD-STYLE: giant word + cut-out subject popping over letters (ref: BIRDS) === */
.s-bird{background:radial-gradient(135% 120% at 30% 35%,var(--bg1,#13202c),#070b10 72%)}
.bird-word{position:absolute;left:90px;top:300px;z-index:2;white-space:pre;
 font-family:'Orbitron','Russo One',sans-serif;font-weight:900;line-height:.8;color:#fff;
 letter-spacing:-.02em;text-transform:uppercase;text-shadow:0 0 70px rgba(0,0,0,.55)}
.bird-cut{position:absolute;bottom:44px;left:300px;width:900px;z-index:3;filter:drop-shadow(0 30px 55px rgba(0,0,0,.65));pointer-events:none}
.bird-cut img{width:100%;height:auto;display:block}
.bird-cut{opacity:0;transform:translateY(70px) scale(.96)}
.slide.active .bird-cut{animation:cutin .85s .12s cubic-bezier(.2,.85,.25,1) forwards}
@keyframes cutin{to{opacity:1;transform:translateY(0) scale(1)}}
.notrans .bird-cut{opacity:1;transform:none;animation:none}
.bird-photo{position:absolute;left:430px;top:120px;bottom:120px;width:560px;z-index:3;background-size:cover;background-position:center;
 border-radius:8px;box-shadow:0 40px 100px rgba(0,0,0,.7)}
.bird-info{position:absolute;right:90px;top:50%;transform:translateY(-50%);width:560px;z-index:4}
.bird-info .kic{color:var(--accentc,#74a9ff)}
.bird-info .big{font-size:80px;color:#fff;-webkit-text-stroke:0;margin:12px 0 0}
.bird-info .blogo{display:block;height:92px;width:auto;max-width:540px;margin:16px 0 4px;object-fit:contain;object-position:left}
.bird-info .accent{height:5px;width:90px;background:var(--accentc,#115ffc);border-radius:3px;margin:22px 0}
.birdfacts{display:flex;flex-direction:column;gap:16px}
.birdfacts>div{font-size:23px;color:#c9cedd;line-height:1.5}
.birdfacts b{color:#fff}
/* bird transition = horizontal push */
.s-bird{transform:translateX(90px);filter:none}
.s-bird.active{transform:translateX(0);filter:none}
.s-bird.leaving{transform:translateX(-90px);filter:none;opacity:0}
.notrans .s-bird{transform:none}
/* === EVENTS DRUM (rotating year dial) === */
.s-drum{overflow:hidden}
.drum-logos{position:absolute;inset:0;z-index:2;pointer-events:none}
.dlg{position:absolute;display:flex;align-items:center;justify-content:center}
.dlg svg,.dlg img{width:100%;height:auto;display:block}
.dlg.dlw{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:26px;letter-spacing:.04em;
 color:#cdd6e8;text-transform:uppercase;white-space:nowrap;border:1px solid #2c3850;border-radius:10px;padding:12px 20px;background:rgba(16,21,32,.55)}
.dlg.dge{display:flex;align-items:center;gap:12px;background:#0d1410;border:1.5px solid #6cc24a;border-radius:13px;padding:11px 20px;box-shadow:0 0 22px rgba(108,194,74,.25)}
.dge .m{font-size:36px;line-height:1}
.dge .t{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:25px;color:#7cd14f;letter-spacing:.03em;line-height:.92;text-transform:uppercase}
.dge .t small{display:block;font-size:11px;letter-spacing:.36em;color:#cfe8c0;font-weight:400}
.drum-center{position:absolute;left:50%;top:202px;transform:translate(-50%,-50%);z-index:10;text-align:center}
.drum-center .dc-num{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:94px;color:#fff;line-height:.9;transition:opacity .4s}
.drum-center .dc-lbl{font-family:'Russo One',sans-serif;font-size:26px;color:var(--warm);letter-spacing:.06em;margin-top:6px;text-transform:uppercase}
.drum-center .dc-vis{font-size:24px;color:#bcc6dd;margin-top:16px}
.drum-center .dc-vis b{font-family:'Orbitron','Russo One',sans-serif;font-weight:700;color:#fff;font-size:28px}
.drum-center .dc-up{display:inline-block;margin-top:14px;font-family:var(--mono);font-size:15px;letter-spacing:.12em;background:var(--warm);color:#0a0a0f;border-radius:6px;padding:7px 14px}
/* racing tachometer gauge (hollow) */
.drum-gauge{position:absolute;left:50%;top:322px;transform:translateX(-50%);width:900px;height:900px;z-index:6}
.drum-gauge svg{width:100%;height:100%;overflow:visible}
.drum-gauge #dneedle{transform-box:view-box;transform-origin:350px 350px;transition:transform .7s cubic-bezier(.3,.85,.3,1)}
.notrans .drum-gauge #dneedle{transition:none}
.drum-gauge .dyl{transition:fill .4s}

/* === DIVIDERS === */
.s-div .num{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:480px;line-height:1;color:transparent;-webkit-text-stroke:2px rgba(110,150,255,.33);
 position:absolute;right:90px;top:50%;transform:translateY(-50%);z-index:2}
.s-div .wrap{display:flex;flex-direction:column;justify-content:center}
.minis{display:flex;flex-wrap:wrap;justify-content:center;gap:30px 34px;margin-top:44px;width:1000px}
.mini{display:flex;flex-direction:column;align-items:center;gap:14px;width:215px}
.mini .mname{font-family:'Russo One',sans-serif;font-size:24px;letter-spacing:.02em;color:#eef2fb;text-align:center}
.mini .tlkb{font-family:var(--mono);font-size:13px;letter-spacing:.14em;color:#0a0a0f;background:var(--warm);border-radius:5px;padding:5px 13px;font-weight:600}
.mini .tlkb.gray{background:#26314a;color:#9aa6c2;font-weight:400}

/* === LOCATION: satellite zoom -> drone video === */
.zoomfx{position:absolute;inset:0;overflow:hidden;background:#05080c;z-index:1}
.zl{position:absolute;left:50%;top:50%;width:2304px;height:1296px;max-width:none;max-height:none;background-size:cover;background-position:center;
 transform:translate(-50%,-50%) scale(.25);opacity:0;will-change:transform,opacity}
.zl.zvid{width:1920px;height:1080px}
.zl.zvid video{width:1920px;height:1080px;max-width:none;max-height:none;object-fit:cover;display:block}
/* cloud deck the camera descends through */
.zcl{position:absolute;left:50%;top:50%;width:2304px;height:1296px;max-width:none;max-height:none;background-size:cover;
 transform:translate(-50%,-50%) scale(.6);opacity:0;pointer-events:none;z-index:15;will-change:transform,opacity}
.zwhite{position:absolute;inset:0;z-index:16;pointer-events:none;opacity:0;
 background:radial-gradient(120% 95% at 50% 42%,#f2f5fa,#ccd6e2);will-change:opacity}
.zdot{position:absolute;left:50%;top:50%;width:22px;height:22px;border-radius:50%;background:var(--accent);z-index:20;
 transform:translate(-50%,-50%);box-shadow:0 0 0 0 rgba(255,87,51,.65);animation:pl 2s ease-out infinite;transition:opacity .5s}
@keyframes pl{70%{box-shadow:0 0 0 46px rgba(255,87,51,0)}100%{box-shadow:0 0 0 0 rgba(255,87,51,0)}}
.zlab{position:absolute;left:50%;bottom:34px;transform:translateX(-50%);white-space:nowrap;font-family:var(--mono);font-size:16px;
 letter-spacing:.2em;color:#fff;background:rgba(10,12,18,.85);border:1px solid var(--accent);border-radius:8px;padding:9px 16px}
.locgrad{position:absolute;inset:0;z-index:5;pointer-events:none;opacity:0;transition:opacity .8s ease;
 background:linear-gradient(180deg,rgba(7,8,13,.5),transparent 28%,transparent 55%,rgba(7,8,13,.84))}
.s-loc.done .locgrad{opacity:1}
.lockic{position:absolute;left:120px;top:150px;z-index:10}
.locinfo{position:absolute;left:120px;bottom:110px;z-index:10;opacity:0;transform:translateY(34px);transition:opacity .7s ease,transform .7s ease}
.s-loc.done .locinfo{opacity:1;transform:translateY(0)}
.notrans .locinfo,.notrans .locgrad{transition:none}
.zattr{position:absolute;right:18px;bottom:14px;z-index:10;font-family:var(--mono);font-size:10px;color:#5a6378;letter-spacing:.08em}

/* === MAP SLIDE === */
.s-map .mapbox{position:absolute;right:90px;top:150px;bottom:110px;width:1010px;z-index:10;border:1px solid var(--line);border-radius:18px;
 background:radial-gradient(120% 100% at 30% 10%,#17202f,#0c111c 70%);padding:24px}
.s-map .mapbox svg{width:100%;height:100%}
.mz{transition:opacity .4s,filter .4s}
.s-map.cyc .mz:not(.mhl){opacity:.13}
.mz.mhl{filter:drop-shadow(0 0 8px rgba(255,255,255,.4))}
.mleg{position:absolute;left:120px;top:430px;z-index:10;width:470px}
.mleg .mi{display:flex;align-items:center;gap:16px;padding:13px 18px;border-radius:10px;font-size:22px;color:#cdd5e8;transition:.3s;border:1px solid transparent}
.mleg .mi i{width:18px;height:18px;border-radius:5px;flex:0 0 auto}
.mleg .mi.on{background:rgba(17,95,252,.13);border-color:#2a3650;color:#fff;transform:translateX(10px)}

/* === COUNTERS === */
.cgrid{display:grid;grid-template-columns:1fr 1fr;gap:54px 80px;margin-top:70px;max-width:1500px}
.cnum b{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:120px;color:#fff;line-height:1}
.cnum b em{font-style:normal;color:var(--warm);font-size:64px}
.cnum>span{display:block;margin-top:10px;font-size:23px;color:var(--muted);letter-spacing:.05em}

/* === MORPH TRACKS (inner carousel) === */
.s-morph .layer{position:absolute;top:54%;left:62%;width:880px;height:704px;transform-origin:center;will-change:transform,filter,opacity;
 pointer-events:none;transition:transform .9s cubic-bezier(.45,.05,.18,1),filter .9s ease,opacity .9s ease;z-index:8}
.s-morph .layer svg{width:100%;height:100%;overflow:visible;max-width:none;max-height:none}
.s-morph .layer .tk{filter:none}
.s-morph .layer.p0{transform:translate(-50%,-50%) scale(1);filter:none;opacity:1;z-index:30}
.s-morph .layer.p1{transform:translate(-8%,-72%) scale(.55);filter:blur(7px) brightness(.7) saturate(.85);opacity:.45;z-index:20}
.s-morph .layer.p2{transform:translate(28%,-86%) scale(.38);filter:blur(12px) brightness(.5);opacity:.25;z-index:10}
.s-morph .layer.hid{transform:translate(48%,-95%) scale(.3);filter:blur(16px);opacity:0;z-index:5}
.s-morph .layer.out{transform:translate(-115%,-28%) scale(1.18);filter:blur(10px) brightness(.55);opacity:0;z-index:35}
.notrans .s-morph .layer{transition:none}
.minfo{position:absolute;left:120px;top:50%;transform:translateY(-50%);width:640px;z-index:32}
.minfo .nm{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:74px;line-height:.98;text-transform:uppercase;margin:14px 0 6px}
.minfo .en{font-family:'Play';color:var(--muted);font-size:24px;letter-spacing:.06em;margin-bottom:26px}
.minfo .desc{font-weight:300;color:#c9cedd;font-size:22px;line-height:1.6;margin-bottom:34px}
.minfo .sgrid{display:grid;grid-template-columns:1fr 1fr;gap:22px 34px}
.minfo .spec b{font-size:33px}.minfo .spec span{font-size:16px}
.minfo .a{opacity:0;transform:translateY(18px);animation:rvup .6s cubic-bezier(.2,.8,.2,1) forwards}
.minfo .a1{animation-delay:.12s}.minfo .a2{animation-delay:.2s}.minfo .a3{animation-delay:.28s}.minfo .a4{animation-delay:.36s}.minfo .a5{animation-delay:.44s}
.notrans .minfo .a{animation:none;opacity:1;transform:none}
.mdots{position:absolute;left:50%;bottom:42px;transform:translateX(-50%);display:flex;gap:10px;z-index:33}
.mdots i{width:9px;height:9px;border-radius:50%;background:#2c3346;transition:.3s}
.mdots i.on{background:var(--primary);width:28px;border-radius:5px}

/* === CHAMPS === */
.chgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:26px;margin-top:64px}
.ch{border:1px solid #2a3650;border-radius:14px;background:rgba(13,18,30,.7);padding:30px 26px;position:relative;overflow:hidden}
.ch b{font-family:'Orbitron','Russo One',sans-serif;font-weight:700;font-size:30px;color:#fff;display:block}
.ch span{font-family:var(--mono);font-size:14px;color:var(--muted);letter-spacing:.14em;text-transform:uppercase;display:block;margin-top:10px}
.ch.star{border-color:rgba(255,140,66,.6);background:linear-gradient(140deg,rgba(255,140,66,.14),rgba(13,18,30,.7) 55%)}
.ch.star::after{content:"FIA";position:absolute;right:14px;top:14px;font-family:var(--mono);font-weight:600;
 font-size:13px;letter-spacing:.18em;background:var(--warm);color:#0a0a0f;padding:4px 12px;border-radius:6px}

/* === BARS (component 05: name | pill bar | count-up value) === */
.crow{display:grid;grid-template-columns:330px 1fr 270px;align-items:center;gap:34px;margin:30px 0}
.crow .name{font-weight:500;color:#cfd5e6;font-size:25px}
.crow .name small{display:block;font-family:var(--mono);font-size:13px;color:var(--muted);letter-spacing:.14em;text-transform:uppercase;margin-top:4px}
.crow .track{height:34px;background:rgba(122,140,200,.10);border-radius:30px;overflow:hidden;position:relative}
.crow .fill{height:100%;width:0;border-radius:30px;transition:width 1.6s cubic-bezier(.2,.8,.2,1)}
.crow .val{font-family:'Orbitron','Russo One',sans-serif;font-weight:700;color:#fff;font-size:36px;text-align:right;font-variant-numeric:tabular-nums}
.crow .val small{color:var(--muted);font-family:'Inter';font-weight:400;font-size:.6em;letter-spacing:.08em}

/* === C-block photo slides === */
.ph-r{position:absolute;right:110px;top:190px;bottom:150px;width:820px;z-index:10}
.ph-r .photo{position:absolute;inset:0}
.ph-r .photo.sm{inset:auto -40px -56px auto;width:380px;height:280px;border:3px solid #0a0a0f}
.facts{margin-top:40px;display:flex;flex-direction:column;gap:18px;max-width:720px}
.fact{display:flex;gap:16px;align-items:baseline;font-size:23px;color:#d6dcea}
.fact::before{content:"//";font-family:var(--mono);color:var(--primary);font-weight:600}
.fact b{color:#fff}
.fact .fen{display:block;font-size:19px;color:var(--en);margin-top:4px}
.fact>div{display:flex;flex-direction:column}
.s-owner .facts{gap:30px;margin-top:34px;max-width:920px}
.s-owner .fact{font-size:25px;line-height:1.5}
.wl .en2{display:block;font-size:23px;color:var(--en);margin-top:5px}

/* === D-block === */
.cards{display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:56px;max-width:980px}
.card{border:1px solid #2a3650;border-radius:16px;background:rgba(13,18,30,.72);padding:32px}
.card b{font-family:'Orbitron','Russo One',sans-serif;font-weight:700;font-size:26px;color:#fff;display:block;margin-bottom:12px}
.card p{font-size:19px;color:#aab3c8;line-height:1.55;font-weight:300}
.card .tagm{font-family:var(--mono);font-size:13px;color:var(--warm);letter-spacing:.22em;display:block;margin-bottom:14px}
/* donut */
.don{position:absolute;left:150px;top:54%;transform:translateY(-50%);width:660px;height:660px;z-index:10}
.don svg{width:100%;height:100%;transform:rotate(-90deg)}
.don circle{fill:none;stroke-width:34;stroke-dasharray:0 1000;transition:stroke-dasharray 1.2s cubic-bezier(.2,.8,.2,1)}
.don .ctr{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.don .ctr b{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:58px;color:#fff}
.don .ctr span{font-size:19px;color:var(--muted);max-width:300px}
.dleg{position:absolute;right:120px;top:50%;transform:translateY(-50%);width:760px;z-index:10}
.dleg .dl{display:flex;align-items:center;gap:18px;padding:17px 0;border-bottom:1px solid #1d2538;font-size:24px;color:#d6dcea}
.dleg .dl i{width:18px;height:18px;border-radius:5px}
.dleg .dl b{margin-left:auto;font-family:'Orbitron','Russo One',sans-serif;color:#fff;font-size:27px}
/* why list */
.why{display:flex;flex-direction:column;gap:0;margin-top:46px;max-width:1480px}
.wl{display:flex;align-items:center;gap:38px;padding:30px 0;border-bottom:1px solid #1d2538;font-size:33px;color:#e6eaf5}
.wl:first-child{border-top:1px solid #1d2538}
.wl .n{font-family:'Orbitron','Russo One',sans-serif;font-weight:900;font-size:44px;color:transparent;-webkit-text-stroke:1.6px #4d7dff;flex:0 0 90px}
.wl b{color:#fff}
/* final */
.s-final .ctr-wrap{position:absolute;inset:0;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
.s-final .lgB{height:190px;mix-blend-mode:screen;max-width:none}
.contacts{display:flex;gap:34px;margin-top:60px;font-family:var(--mono);font-size:21px;letter-spacing:.12em;color:#bccaea}
.contacts span{border:1px solid #2a3650;border-radius:10px;padding:16px 28px;background:rgba(13,18,30,.7)}

/* === CONTROLS (outside stage) === */
.deck-controls{display:flex;gap:14px;left:auto;right:24px;bottom:18px;transform:none}
.nbtn{width:52px;height:52px;border-radius:50%;border:1px solid #2a3146;background:rgba(14,17,28,.85);color:#cfd5e6;font-size:21px;cursor:pointer;transition:.15s}
.nbtn:hover{border-color:var(--primary);color:#fff}
.ehint{position:fixed;right:18px;bottom:18px;z-index:1000;font-family:var(--mono);font-size:11px;color:#4a5366;letter-spacing:.1em}
.dlbtn{position:fixed;left:18px;bottom:16px;z-index:1000;display:flex;align-items:center;gap:9px;text-decoration:none;
 font-family:var(--mono);font-size:12px;letter-spacing:.14em;color:#cfd5e6;border:1px solid #2a3146;border-radius:9px;
 padding:9px 16px;background:rgba(14,17,28,.85);transition:.15s}
.dlbtn:hover{border-color:var(--primary);color:#fff;background:rgba(17,95,252,.18)}
.dlbtn b{color:var(--warm);font-weight:600}
.export .dlbtn{display:none!important}
/* edit mode */
.edbar{position:fixed;top:0;left:0;right:0;z-index:3000;display:none;align-items:center;justify-content:center;gap:14px;
 height:46px;background:linear-gradient(90deg,#ff8c42,#ff5733);color:#0a0a0f;font-family:var(--mono);font-size:14px;
 letter-spacing:.12em;text-transform:uppercase;font-weight:600;box-shadow:0 6px 24px rgba(0,0,0,.5)}
body.editing .edbar{display:flex}
body.editing .deck-viewport{outline:3px solid #ff8c42;outline-offset:-3px}
body.editing [contenteditable] :hover,body.editing .wrap :hover{outline:1px dashed rgba(255,140,66,.55)}
body.editing .deck-controls{display:none}
@media (prefers-reduced-motion:reduce){.scan,.pulse,.tick-line .in{animation:none!important}}
/* export helpers (?export=1 / ?bare=1 / ?textonly=1) — used by the PPTX build pipeline */
.export .deck-controls,.export .ehint,.export .edbar{display:none!important}
.bare .s-morph .layer,.bare #minfo,.bare #mdots{display:none!important}
.textonly,.textonly body{background:none!important}
.textonly .slide,.textonly .deck-stage{background:none!important}
.textonly .s-loc .zoomfx,.textonly .s-loc .locgrad,.textonly .s-loc .zattr,.textonly .s-loc .hud,
.textonly .s-loc .prog,.textonly .s-loc .ticks,.textonly .deck-viewport{background:none!important}
.textonly .s-loc .zoomfx,.textonly .s-loc .locgrad,.textonly .s-loc .zattr,.textonly .s-loc .hud,.textonly .s-loc .prog{display:none!important}
.textonly .locinfo{opacity:1!important;transform:none!important}
.infoonly,.infoonly body,.infoonly .slide,.infoonly .deck-stage,.infoonly .deck-viewport{background:none!important}
.infoonly .s-morph .layer,.infoonly #mdots,.infoonly .hud,.infoonly .prog,.infoonly .ticks{display:none!important}
</style>
</head>
<body>
<div class="deck-viewport"><div class="deck-stage" id="stage">

<!-- ============ A1 · TITLE ============ -->
<section class="slide s-title" data-block="0">
  <div class="bgimg" style="background-image:url('assets/aerial-dusk.jpg')"></div>
  <div class="dim" style="background:linear-gradient(180deg,rgba(6,7,11,.62),rgba(6,7,11,.5) 38%,rgba(6,7,11,.95))"></div>
  <div class="grid-tel"></div><div class="scan"></div><div class="ticks"></div>
  <img class="logo-top rv d1" src="assets/logo.svg" alt="Sokol">
  <div class="hero">
    <h1 class="giant rv d3">SOKOL<br><span class="fill">INTERNATIONAL</span> CIRCUIT</h1>
    <div class="en-sub rv d4">World-class motorsport in the heart of Eurasia</div>
  </div>
  <div class="tick-line"><div class="in">
    <span>MotoGP <i>//</i></span><span>FIM Superbike <i>//</i></span><span>WTCC <i>//</i></span><span>DTM <i>//</i></span><span>Formula E <i>//</i></span><span>Formula 2 · 3 <i>//</i></span><span>WEC <i>//</i></span><span>Drift series</span>
  </div></div>
</section>

<!-- ============ A2 · OWNER ============ -->
<section class="slide s-owner" data-block="0">
  <div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap" style="width:1000px">
    <div class="kic rv d1">THE OWNER</div>
    <h1 class="big rv d2" style="font-size:68px">Dostan<br>Ibragimov</h1>
    <div class="en-sub rv d2">Owner, Sokol International Circuit</div>
    <div class="genb rv d3" style="margin-top:26px">⚠ placeholder copy — final bio to follow</div>
    <div class="facts">
      <div class="fact rv d3"><div><span>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore</span></div></div>
      <div class="fact rv d4"><div><span>Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo</span></div></div>
      <div class="fact rv d4"><div><span>Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur</span></div></div>
      <div class="fact rv d5"><div><span>Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim</span></div></div>
    </div>
  </div>
  <div class="ph-r rv d3" style="width:560px">
    <div class="photo" style="display:flex;align-items:center;justify-content:center;background:linear-gradient(150deg,#131a2a,#0b0f1a)">
      <div style="text-align:center">
        <img src="assets/logo.svg" style="height:90px;width:auto" alt="">
        <div class="genb" style="display:block;margin-top:26px">⚠ owner photo — to be added</div>
      </div>
    </div>
  </div>
</section>

<!-- ============ A3 · PURPOSE ============ -->
<section class="slide s-purpose" data-block="0">
  <div class="bgimg" style="background-image:url('assets/aerial-gold.jpg')"></div>
  <div class="dim"></div><div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap">
    <div class="kic rv d1">WHY SOKOL WAS BUILT · THE PURPOSE</div>
    <h1 class="big rv d2" style="max-width:1500px">A <span style="color:#5e9bff">world-class arena</span><br>for Kazakhstan</h1>
    <div class="en-sub rv d3">The story behind the project</div>
    <div class="chips" style="margin-top:44px;max-width:1560px">
      <div class="chip rv d4" style="max-width:470px"><b>A dream of big motorsport</b><i>the Main Circuit commissioned from Hermann Tilke back in 2013 — to bring world racing series to Kazakhstan</i></div>
      <div class="chip rv d5" style="max-width:470px"><b>Sport instead of streets</b><i>a safe alternative to street racing and a driver school from childhood</i></div>
      <div class="chip rv d6" style="max-width:470px"><b>A legacy for the country</b><i>infrastructure, jobs and a destination for the south of Kazakhstan</i></div>
    </div>
  </div>
</section>

<!-- ============ A4 · SCALE OF SOKOL ============ -->
<section class="slide s-manifest" data-block="0">
  <div class="bgimg" style="background-image:url('assets/aerial-lake.jpg')"></div>
  <div class="dim"></div><div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap">
    <div class="kic rv d1">FIA GRADE 2 · BUILT TO STANDARD</div>
    <h1 class="big rv d2" style="max-width:1560px">Kazakhstan's only <span style="color:#5e9bff">FIA Grade 2</span> circuit</h1>
    <div class="en-sub rv d3">Every facility the FIA circuit standard requires — already on site</div>
    <div class="chips">
      <div class="chip rv d4"><b>Pit buildings</b><i>team garages with direct pit-lane access</i></div>
      <div class="chip rv d4"><b>Own medical centre</b><i>permanent, on-site — per FIA Appendix O</i></div>
      <div class="chip rv d5"><b>Race control</b><i>full-circuit camera monitoring</i></div>
      <div class="chip rv d5"><b>Safety systems</b><i>barriers, run-off zones, marshal posts</i></div>
      <div class="chip rv d6"><b>Timing & telemetry</b><i>professional timekeeping infrastructure</i></div>
    </div>
  </div>
</section>

<!-- ============ A3 · LOCATION (satellite zoom -> drone video) ============ -->
<section class="slide s-loc" data-block="0">
  <div class="zoomfx" id="zoomfx">
    <div class="zl" style="background-image:url('assets/zoom/z06.jpg')"></div>
    <div class="zl" style="background-image:url('assets/zoom/z08.jpg')"></div>
    <div class="zl" style="background-image:url('assets/zoom/z10.jpg')"></div>
    <div class="zl" style="background-image:url('assets/zoom/z12.jpg')"></div>
    <div class="zl" style="background-image:url('assets/zoom/z14.jpg')"></div>
    <div class="zl" style="background-image:url('assets/zoom/z16.jpg')"></div>
    <div class="zl zvid"><video id="dronev" src="assets/sokol-drone.mp4" poster="assets/sokol-drone-poster.jpg" muted loop playsinline preload="auto"></video></div>
    <div class="zcl" id="zcl1" style="background-image:url('assets/zoom/cloud-a.png')"></div>
    <div class="zcl" id="zcl2" style="background-image:url('assets/zoom/cloud-b.png')"></div>
    <div class="zwhite" id="zwhite"></div>
    <div class="zdot" id="zdot"><span class="zlab">SOKOL INTERNATIONAL CIRCUIT</span></div>
  </div>
  <div class="locgrad"></div>
  <div class="ticks"></div>
  <div class="lockic kic">LOCATION</div>
  <div class="locinfo">
    <h1 class="big" style="font-size:58px">Next door to Almaty</h1>
    <div class="en-sub">Trans-Kazakhstan highway · Almaty region</div>
    <div class="chips" style="margin-top:26px">
      <div class="chip"><b>A racing town</b><i>a self-contained town with its own infrastructure</i></div>
      <div class="chip"><b>76 km</b><i>from Almaty</i></div>
      <div class="chip"><b>205 ha</b><i>of own grounds</i></div>
    </div>
  </div>
  <div class="zattr">Imagery © Esri · Maxar</div>
</section>

<!-- ============ B0 · SIX CIRCUITS + TILKE (merged) ============ -->
<section class="slide s-tilke" data-block="1">
  <div class="grid-tel"></div><div class="scan"></div><div class="ticks"></div>
  <!-- Tilke photo + credentials, right side -->
  <div style="position:absolute;right:120px;top:150px;width:380px;z-index:10" class="rv d3">
    <div class="photo" style="width:380px;height:430px;background-image:url('assets/tilke.jpg');background-position:top center"></div>
    <div style="font-family:'Russo One',sans-serif;font-size:24px;color:#fff;margin-top:18px">Hermann Tilke</div>
    <div style="font-family:var(--mono);font-size:14px;color:#9fb4dd;letter-spacing:.1em;margin-top:6px;line-height:1.5">ARCHITECT OF F1 CIRCUITS:<br>Bahrain · Abu Dhabi · Shanghai · Austin</div>
  </div>
  <div class="wrap" style="width:1080px">
    <div class="kic rv d1">THE CIRCUITS</div>
    <h1 class="big rv d2" style="font-size:74px">Six circuits —<br>one venue</h1>
    <div class="en-sub rv d3" style="max-width:980px;font-size:25px;line-height:1.5">The flagship <b style="color:var(--warm)">Main Circuit</b> is designed by <b style="color:#fff">Hermann Tilke</b>, the architect of modern Formula 1 tracks. The five supporting circuits were engineered by the Sokol team.</div>
    <div class="minis rv d5" style="margin-top:70px">__MINIS__</div>
  </div>
</section>

<!-- ============ B2 · MORPH TRACKS ============ -->
<section class="slide s-morph" data-block="1" id="smorph">
  <div class="ticks"></div>
  <div class="minfo" id="minfo"></div>
  <div class="mdots" id="mdots"></div>
</section>

<!-- ============ B3 · EVENTS TIMELINE ============ -->
<section class="slide s-drum" id="sdrum" data-block="1">
  <div class="ticks"></div>
  <div class="drum-logos">__DRUMLOGOS__</div>
  <div class="drum-center" id="drumCenter"></div>
  <div class="drum-gauge">__DRUMGAUGE__</div>
  <div class="genb" style="position:absolute;left:120px;bottom:34px;z-index:10">⚠ attendance figures illustrative · some event logos still placeholders</div>
</section>

<!-- ============ B4 · EVENT VIDEO (placeholder) ============ -->
<section class="slide s-evvideo" data-block="1">
  <div class="bgimg" style="background-image:url('assets/drift-duo.jpg')"></div>
  <div class="dim full"></div><div class="ticks"></div>
  <div class="ctr-wrap" style="position:absolute;inset:0;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div style="width:150px;height:150px;border-radius:50%;border:3px solid rgba(255,255,255,.75);display:flex;align-items:center;justify-content:center;font-size:54px;color:#fff;background:rgba(10,12,18,.45)" class="rv d1">▶</div>
    <h1 class="big rv d2" style="font-size:58px;margin-top:36px">Sokol in motion</h1>
    <div class="en-sub rv d3">Event highlights</div>
    <div class="genb rv d4" style="margin-top:30px">⚠ video placeholder — clip to be added</div>
  </div>
</section>

<!-- ============ C1 · FACILITIES: PIT + RACE CONTROL ============ -->
<section class="slide s-teams" data-block="2">
  <div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap">
    <div class="kic rv d1">FIA GRADE 2 · THE COMPLEX</div>
    <h1 class="big rv d2" style="font-size:58px">Main pit building & paddock</h1>
    <div class="duo">
      <div class="dcard rv d3"><div class="dimg" style="background-image:url('assets/pit-building.jpg')"></div><div class="dbody"><b>Main pit building</b><ul><li>Team garages</li><li>Race Control</li><li>Timing rooms</li><li>VIP suites</li><li>Press centre</li><li>Race direction & stewards</li></ul></div></div>
      <div class="dcard rv d4"><div class="dimg ph">PHOTO</div><div class="dbody"><b>Paddock</b><ul><li>Racing teams</li><li>Technical trailers</li><li>Service vehicles</li><li>Scrutineering</li></ul></div></div>
    </div>
  </div>
</section>

<!-- ============ C2 · MEDICAL + FIRE & RESCUE ============ -->
<section class="slide s-teams" data-block="2">
  <div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap">
    <div class="kic rv d1">FIA GRADE 2 · SAFETY</div>
    <h1 class="big rv d2" style="font-size:58px">Medical & rescue on site</h1>
    <div class="duo">
      <div class="dcard rv d3"><div class="dimg ph">PHOTO</div><div class="dbody"><b>Medical centre</b><ul><li>Medical post</li><li>First-aid rooms</li><li>Casualty evacuation zone</li><li>Anti-doping room</li></ul></div></div>
      <div class="dcard rv d4"><div class="dimg ph">PHOTO</div><div class="dbody"><b>Fire & rescue service</b><ul><li>Fire trucks</li><li>Dedicated service building</li><li>Rapid track response</li><li>Rescue & intervention crews</li></ul></div></div>
    </div>
  </div>
</section>

<!-- ============ C3 · RACE CONTROL TOWER + GRANDSTAND ============ -->
<section class="slide s-teams" data-block="2">
  <div class="grid-tel"></div><div class="ticks"></div>
  <div class="wrap">
    <div class="kic rv d1">FIA GRADE 2 · CONTROL</div>
    <h1 class="big rv d2" style="font-size:58px">Race control & spectators</h1>
    <div class="duo">
      <div class="dcard rv d3"><div class="dimg ph">PHOTO</div><div class="dbody"><b>Race control tower</b><ul><li>Race Control</li><li>Timing</li><li>CCTV monitoring</li><li>Marshal communications</li><li>Safety systems control</li></ul></div></div>
      <div class="dcard rv d4"><div class="dimg ph">PHOTO</div><div class="dbody"><b>Main grandstand</b><ul><li>Principal viewing zone</li><li>Overlooks the main circuit</li><li>Spectator capacity</li><li>Hospitality areas</li></ul></div></div>
    </div>
  </div>
</section>

<!-- ============ C4 · LEISURE INTRO ============ -->
<section class="slide s-leisure-intro" data-block="2">
  <div class="bgimg" style="background-image:url('assets/drift-ice.jpg')"></div>
  <div class="dim full"></div><div class="ticks"></div>
  <div class="ctr-wrap" style="position:absolute;inset:0;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div class="kic rv d1" style="margin-bottom:18px">BEYOND RACING</div>
    <h1 class="big rv d2">Sokol — more<br>than a racetrack</h1>
    <div class="en-sub rv d3" style="margin-top:18px">A destination that lives all week long</div>
  </div>
</section>

<!-- ============ C5 · LEISURE PROMO (placeholder) ============ -->
<section class="slide s-evvideo" data-block="2">
  <div class="bgimg" style="background-image:url('assets/drift-smoke.jpg')"></div>
  <div class="dim full"></div><div class="ticks"></div>
  <div class="ctr-wrap" style="position:absolute;inset:0;z-index:10;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center">
    <div style="width:150px;height:150px;border-radius:50%;border:3px solid rgba(255,255,255,.75);display:flex;align-items:center;justify-content:center;font-size:54px;color:#fff;background:rgba(10,12,18,.45)" class="rv d1">▶</div>
    <h1 class="big rv d2" style="font-size:58px;margin-top:36px">Experience Sokol</h1>
    <div class="en-sub rv d3">Karting · hotel · museum · paintball</div>
    <div class="genb rv d4" style="margin-top:30px">⚠ promo video placeholder — clip to be added</div>
  </div>
</section>

<!-- ============ C6 · KARTING (bird, cutout) ============ -->
<section class="slide s-bird" data-block="2" style="--accentc:#34d058;--bg1:#10241a">
  <div class="ticks"></div>
  <div class="bird-word rv d1" style="font-size:240px">KA
RT</div>
  <div class="bird-cut" style="left:230px;width:1000px;bottom:90px"><img src="assets/cut-karting.png" alt=""></div>
  <div class="bird-info">
    <div class="kic rv d2">BEYOND RACING</div>
    <h1 class="big rv d3">Karting</h1>
    <div class="accent rv d3"></div>
    <div class="birdfacts">
      <div class="rv d4"><b>Live racing</b> — SMP Karting series rounds held at Sokol</div>
      <div class="rv d5">The country's only <b>telemetry-equipped</b> kart circuit · 1,650 m · 12 pit boxes</div>
      <div class="rv d6"><b>Driver school</b> — a junior pathway from karts to circuit racing</div>
    </div>
  </div>
</section>

<!-- ============ C7 · RACE HOTEL (bird, photo) ============ -->
<section class="slide s-bird" data-block="2" style="--accentc:#ff8c42;--bg1:#241a12">
  <div class="ticks"></div>
  <div class="bird-word rv d1" style="font-size:200px">HO
TEL</div>
  <div class="bird-photo rv d2" style="background-image:url('assets/hotel.jpg')"></div>
  <div class="bird-info">
    <div class="kic rv d2">BEYOND RACING</div>
    <img class="blogo rv d3" src="assets/logos/real-racehotel.png" alt="Sokol Race Hotel">
    <div class="accent rv d3"></div>
    <div class="birdfacts">
      <div class="rv d4"><b>42 rooms</b> by the pit lane · 3,400 m² trackside hotel</div>
      <div class="rv d5"><b>75-seat conference hall</b> for briefings and media</div>
      <div class="rv d6">Bar-restaurant · pools · sauna · Wi-Fi</div>
    </div>
  </div>
</section>

<!-- ============ C8 · MUSEUM (bird, cutout) ============ -->
<section class="slide s-bird" data-block="2" style="--accentc:#ff5733;--bg1:#24141a">
  <div class="ticks"></div>
  <div class="bird-word rv d1" style="font-size:200px">MUS
EUM</div>
  <div class="bird-cut" style="left:300px;width:880px;bottom:230px"><img src="assets/cut-museum.png" alt=""></div>
  <div class="bird-info">
    <div class="kic rv d2">BEYOND RACING</div>
    <img class="blogo rv d3" src="assets/logos/real-museum.png" alt="Sokol Museum">
    <div class="accent rv d3"></div>
    <div class="birdfacts">
      <div class="rv d4"><b>1,500 m²</b> of retro and sport cars, including a Formula 1 car</div>
      <div class="rv d5">Roof terrace overlooking the drag strip and drift arena</div>
      <div class="rv d6">18-hole mini golf · 29 parking spots</div>
    </div>
  </div>
</section>

<!-- ============ C9 · PAINTBALL (bird, cutout) ============ -->
<section class="slide s-bird" data-block="2" style="--accentc:#2aa8ff;--bg1:#11202c">
  <div class="ticks"></div>
  <div class="bird-word rv d1" style="font-size:160px">PAINT
BALL</div>
  <div class="bird-cut" style="left:360px;width:680px;bottom:80px"><img src="assets/cut-paintball.png" alt=""></div>
  <div class="bird-info">
    <div class="kic rv d2">BEYOND RACING</div>
    <img class="blogo rv d3" src="assets/logos/real-paintball.png" alt="Sokol Paintball">
    <div class="accent rv d3"></div>
    <div class="birdfacts">
      <div class="rv d4"><b>4.1 ha · 9 scenario maps</b></div>
      <div class="rv d5"><b>"Mansion"</b> — the legendary Counter-Strike map rebuilt for real</div>
      <div class="rv d6">Corporate tournaments and scenario games all year round</div>
    </div>
  </div>
</section>

<!-- ============ FINAL ============ -->
<section class="slide s-final" data-block="3">
  <div class="bgimg" style="background-image:url('assets/aerial-dusk2.jpg')"></div>
  <div class="dim full"></div><div class="grid-tel"></div><div class="scan"></div><div class="ticks"></div>
  <div class="ctr-wrap">
    <img class="lgB rv d1" src="assets/logo.svg" alt="Sokol" style="mix-blend-mode:normal;height:130px;width:auto">
    <h1 class="giant rv d2" style="font-size:92px;margin-top:40px"><span class="fill">Welcome to Sokol</span></h1>
    <div class="en-sub rv d3">Sokol International Circuit · Almaty, Kazakhstan</div>
    <div class="contacts">
      <span class="rv d4">@SOKOL_INTERNATIONAL_CIRCUIT</span>
      <span class="rv d5">www.sokol.kz</span>
      <span class="rv d6">Almaty, Kazakhstan</span>
    </div>
  </div>
</section>

</div></div>

<div class="edbar" id="edbar">✎ Режим правки · кликните в любой текст и редактируйте · Esc — выход · Ctrl+S — сохранить</div>
<div class="deck-controls"><button class="nbtn" id="bPrev">‹</button><button class="nbtn" id="bNext">›</button></div>
<div class="ehint">←→ листать · E править · CTRL+S сохранить</div>
<a class="dlbtn" href="sokol-deck.pptx" download="sokol-deck.pptx" title="Скачать копию в формате PowerPoint"><b>⬇</b> СКАЧАТЬ PPTX</a>

<script>
/* ============ DECK ENGINE ============ */
const Q=new URLSearchParams(location.search);
if(Q.has('noauto'))document.documentElement.classList.add('notrans');
['export','bare','textonly','infoonly'].forEach(p=>{if(Q.has(p))document.documentElement.classList.add(p);});
const NOTRANS=Q.has('noauto');
const stage=document.getElementById('stage');
const slides=[...document.querySelectorAll('.slide')];
const TOTAL=slides.length;

/* fixed-stage uniform scaling */
function fit(){
  const s=Math.min(innerWidth/1920,innerHeight/1080);
  stage.style.transform=`translate(${(innerWidth-1920*s)/2}px,${(innerHeight-1080*s)/2}px) scale(${s})`;
}
addEventListener('resize',fit);fit();

/* HUD cloned onto every slide: prominent slide number only */
slides.forEach((sl,i)=>{
  const hud=document.createElement('div');hud.className='hud';
  hud.innerHTML=`<span class="cnt">${String(i+1).padStart(2,'0')}<span>/${TOTAL}</span></span>`;
  sl.appendChild(hud);
});
/* ============ EVENTS DRUM (rotating year dial) ============ */
const EVENTS=[
 {yr:'2016', t:'Grand opening', d:'Karting & drag strip launched · guest of honour Jorge Lorenzo, 3× MotoGP champion', ev:'6', p:'5,000+', logos:['GRAND OPENING','JORGE LORENZO']},
 {yr:'2019', t:'Circuit completed', d:'Flagship circuit, pit buildings and core infrastructure finished', ev:'10', p:'15,000+', logos:['TRACK DAYS','TEST EVENTS']},
 {yr:'2024', t:'National series at home', d:'A full season of national motorsport at Sokol', ev:'35', p:'40,000+', logos:['SOKOL DRAG WARS','GORILLA DRIFT','KZ KARTING']},
 {yr:'2025', t:'Asia Auto Gymkhana', d:"Asia's biggest gymkhana championship — held with FIA support", ev:'48', p:'60,000+', logos:['ASIA GYMKHANA · FIA','RED BULL','GORILLA DRIFT','DRAG WARS']},
 {yr:'2026', t:'FIA Central Asia Drifting Cup', d:'25–27 September · TOP-32 tandem battles', ev:'50+', p:'80,000+ expected', up:true, logos:['FIA CADC','+ FULL SEASON']},
];
const sdrum=document.getElementById('sdrum'),drumCenter=document.getElementById('drumCenter');
const DRUM_ANG=[-105,-52,0,52,105];
const dneedle=sdrum.querySelector('#dneedle'),dyear=sdrum.querySelector('#dyear');
const dylEls=[...sdrum.querySelectorAll('.dyl')];
let eIdx=0;
function drumRender(){
  const e=EVENTS[eIdx];
  drumCenter.innerHTML=`<div class="dc-num">${e.ev}</div><div class="dc-lbl">events in ${e.yr}</div>
   <div class="dc-vis"><b>${e.p}</b> visitors</div>${e.up?'<div class="dc-up">UPCOMING</div>':''}`;
  if(dneedle)dneedle.style.transform='rotate('+DRUM_ANG[eIdx]+'deg)';
  if(dyear){dyear.textContent=e.yr;dyear.setAttribute('fill',e.up?'#ff8c42':'#fff');}
  dylEls.forEach((el,i)=>{el.setAttribute('fill',i===eIdx?(e.up?'#ff8c42':'#fff'):'#5d6b8a');});
}
drumRender();

/* ============ MORPH TRACKS (inner carousel) ============ */
const TRACKS=__TRACKS__;
const smorph=document.getElementById('smorph'),minfo=document.getElementById('minfo'),mdots=document.getElementById('mdots');
let mIdx=0,mPrev=-1;
TRACKS.forEach((r,i)=>{
  const el=document.createElement('div');el.className='layer hid';el.style.setProperty('--c',r.c);
  const body=r.paths.map(d=>r.render==='fill'
    ?`<path class="tk" d="${d}" fill="${r.c}" fill-rule="evenodd"/>`
    :`<path class="tk" d="${d}" fill="none" stroke="${r.c}" stroke-width="${r.sw}" stroke-linecap="round" stroke-linejoin="round"/>`).join('');
  el.innerHTML=`<svg viewBox="${r.vb}" preserveAspectRatio="xMidYMid meet">${body}</svg>`;
  smorph.insertBefore(el,minfo);
  const d=document.createElement('i');mdots.appendChild(d);
});
const mLayers=[...smorph.querySelectorAll('.layer')],mDots=[...mdots.children];
function mRender(){
  const r=TRACKS[mIdx];
  minfo.style.setProperty('--c',r.c);
  minfo.innerHTML=`${r.gen?'<div class="genb a a1" style="margin-bottom:18px">⚠ generated copy — replace with real data</div>':''}
   <div class="kic a a1" style="color:${r.c}">${r.kic}</div><div class="nm a a2">${r.nm}</div><div class="en a a3">${r.en}</div>
   <p class="desc a a4">${r.desc}${r.den?`<span style="display:block;font-size:20px;color:var(--en);margin-top:10px">${r.den}</span>`:''}</p>
   <div class="sgrid a a5">${r.specs.map(s=>`<div class="spec" style="border-color:${r.c}"><b>${s[0]}</b><span>${s[1]}</span></div>`).join('')}</div>`;
  mLayers.forEach((el,i)=>{
    const off=(i-mIdx+TRACKS.length)%TRACKS.length;
    el.classList.remove('p0','p1','p2','hid','out');
    if(i===mPrev&&off!==0)el.classList.add('out');
    else if(off===0)el.classList.add('p0');
    else if(off===1)el.classList.add('p1');
    else if(off===2)el.classList.add('p2');
    else el.classList.add('hid');
  });
  mDots.forEach((d,i)=>d.classList.toggle('on',i===mIdx));
}
function mGo(n){mPrev=mIdx;mIdx=n;mRender();}

/* ============ LOCATION: satellite zoom -> drone video ============ */
const locSlide=document.querySelector('.s-loc');
const ZL=[...locSlide.querySelectorAll('.zl')];
const zdot=document.getElementById('zdot'),dronev=document.getElementById('dronev');
let locRaf=null;
/* finer layers stack ABOVE coarser and fade in as they grow — one continuous camera */
ZL.forEach((l,i)=>l.style.zIndex=String(i+1));
const zcl1=document.getElementById('zcl1'),zcl2=document.getElementById('zcl2'),zwhite=document.getElementById('zwhite');
function setL(l,op,sc,rot,blur){
  l.style.opacity=String(op);
  l.style.transform=`translate(-50%,-50%) scale(${sc})${rot?` rotate(${rot}deg)`:''}`;
  l.style.filter=blur&&blur>.3?`blur(${blur.toFixed(1)}px)`:'';
}
function cloudsOff(){zcl1.style.opacity='0';zcl2.style.opacity='0';zwhite.style.opacity='0';}
function locReset(){
  if(locRaf){cancelAnimationFrame(locRaf);locRaf=null;}
  dronev.pause();try{dronev.currentTime=0;}catch(_){}
  locSlide.classList.remove('done');zdot.style.opacity=1;
  ZL.forEach(l=>setL(l,0,.25));cloudsOff();
}
function locFinal(){
  ZL.forEach((l,i)=>setL(l,i===ZL.length-1?1:0,1));
  zdot.style.opacity=0;cloudsOff();locSlide.classList.add('done');
}
const Z_HOLD=550,Z_STAGE=430,Z_STAGES=ZL.length-1; // exponential: 4x per STAGE ms, no pauses
function locApply(el){ // render continuous-zoom state for elapsed ms; returns zoom position k
  const k=Math.min(Z_STAGES,Math.max(0,el-Z_HOLD)/Z_STAGE);
  const i=Math.min(Z_STAGES-1,Math.floor(k)),f=k-i;
  const c=(k-(Z_STAGES-1.4))/1.4;       // cloud-descent progress over the last 1.4 stages
  const swapped=c>=.5;                   // at the whiteout peak the camera "lands"
  ZL.forEach((l,j)=>{
    if(j===Z_STAGES){
      /* video NEVER animates in: it stands full-screen behind the whiteout and is
         revealed only by the clouds clearing — like the drone just arrived from space */
      setL(l,swapped?1:0,1,0,swapped?Math.max(0,1-(c-.5)/.38)*10:0);
    }else if(j===i&&!swapped)setL(l,1,Math.pow(4,f),0,f*6);          // coarse: defocuses rushing past
    else if(j===i+1&&j<Z_STAGES&&!swapped){                           // fine sat layer: focuses in
      const e=Math.min(1,f/.7),s=e*e*(3-2*e);
      setL(l,s,Math.pow(4,f-1),0,(1-s)*9);
    }else setL(l,0,j<i?4:.25);
  });
  if(k>Z_STAGES-1.4)zdot.style.opacity=String(Math.max(0,1-c*2.4));
  if(c>0&&c<1){
    const b1=Math.pow(Math.sin(Math.PI*c),1.4);
    setL(zcl1,Math.min(1,b1*1.3),1+c*7,c*9);
    const c2=Math.max(0,(c-.07)/.93),b2=Math.pow(Math.sin(Math.PI*c2),1.5);
    setL(zcl2,Math.min(1,b2*1.2),.7+c*5.4,-c*7);
    /* veil peaks ~0.97 right at the swap so the cut is invisible */
    zwhite.style.opacity=String(Math.min(.97,Math.max(0,Math.pow(Math.sin(Math.PI*c),1.1)*1.28-.16)));
  }else cloudsOff();
  return k;
}
function locPlay(){
  locReset();
  if(Q.has('zt')){ // deterministic debug: render zoom at fixed elapsed ms
    if(locApply(+Q.get('zt')||0)>=Z_STAGES)locSlide.classList.add('done');
    return;
  }
  if(NOTRANS||matchMedia('(prefers-reduced-motion: reduce)').matches){locFinal();return;}
  let start=null,played=false;
  function frame(ts){
    if(start===null)start=ts;
    const k=locApply(ts-start);
    /* start playback while still behind the clouds so it emerges already moving */
    if(k>Z_STAGES-1.6&&!played){played=true;dronev.play().catch(()=>{});}
    if(k>=Z_STAGES){locSlide.classList.add('done');locRaf=null;return;}
    locRaf=requestAnimationFrame(frame);
  }
  locRaf=requestAnimationFrame(frame);
}

/* ============ COUNTERS / BARS / DONUT ============ */
function runCounters(sl){
  sl.querySelectorAll('.cv').forEach(el=>{
    const v=+el.dataset.v;
    if(NOTRANS){el.textContent=v;return;}
    const t0=performance.now(),D=1300;
    (function f(t){const k=Math.min(1,(t-t0)/D);el.textContent=Math.round(v*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(f);})(t0);
  });
}
function runBars(sl){
  const fills=[...sl.querySelectorAll('.fill')],nums=[...sl.querySelectorAll('.vn')],DUR=1600;
  if(NOTRANS){
    fills.forEach(f=>{f.style.transition='none';f.style.width=f.dataset.w+'%';});
    nums.forEach(n=>n.textContent=(+n.dataset.v).toLocaleString('ru-RU'));
    return;
  }
  fills.forEach(f=>{f.style.transition='none';f.style.width='0';});
  nums.forEach(n=>n.textContent='0');
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    fills.forEach(f=>{f.style.transition='width '+DUR+'ms cubic-bezier(.2,.8,.2,1)';f.style.width=f.dataset.w+'%';});
    let t0=null;
    (function tick(now){
      if(t0===null)t0=now||performance.now();
      const p=Math.min(1,((now||performance.now())-t0)/DUR),e=1-Math.pow(1-p,3);
      nums.forEach(n=>n.textContent=Math.round((+n.dataset.v)*e).toLocaleString('ru-RU'));
      if(p<1)requestAnimationFrame(tick);
    })(performance.now());
  }));
}
function runDonut(sl){
  const C=2*Math.PI*80;
  sl.querySelectorAll('.seg').forEach(s=>{
    const p=+s.dataset.p,o=+s.dataset.o;
    s.style.strokeDashoffset=-(o/100*C);
    const set=()=>s.style.strokeDasharray=`${p/100*C-3} ${C-p/100*C+3}`;
    s.style.strokeDasharray=`0 ${C}`;
    if(NOTRANS){set();}else{setTimeout(set,150);}
  });
}

/* ============ NAVIGATION ============ */
let cur=-1;
function activate(idx,backwards){
  const old=cur;cur=idx;
  slides.forEach((s,i)=>{
    s.classList.remove('leaving');
    if(i===idx)s.classList.add('active');
    else{
      if(i===old&&!NOTRANS){s.classList.add('leaving');setTimeout(()=>s.classList.remove('leaving'),700);}
      s.classList.remove('active');
    }
  });
  const sl=slides[idx];
  if(sl.classList.contains('s-loc'))locPlay();
  else if(old>=0&&slides[old]&&slides[old].classList.contains('s-loc'))locReset();
  if(sl.classList.contains('s-bars'))runBars(sl);
  if(sl.classList.contains('s-rev'))runDonut(sl);
  if(sl===smorph){mPrev=-1;mGo(backwards?TRACKS.length-1:0);}
  if(sl===sdrum){eIdx=backwards?EVENTS.length-1:0;drumRender();}
}
/* shared-element morph: Main Circuit mini (slide 6) grows into the big contour (slide 7) */
function flyMainCircuit(idx7){
  const src=document.querySelector('.s-tilke .mini svg');
  if(!src||NOTRANS){activate(idx7,false);return;}
  const st=stage.getBoundingClientRect(),k=st.width/1920,r=src.getBoundingClientRect();
  const S={x:(r.left-st.left)/k,y:(r.top-st.top)/k,w:r.width/k,h:r.height/k};
  const T={x:0.62*1920-440,y:0.54*1080-352,w:880,h:704};
  const wrap=document.createElement('div');
  wrap.style.cssText='position:absolute;left:0;top:0;z-index:60;pointer-events:none;transform-origin:top left;will-change:transform;transition:transform .8s cubic-bezier(.45,.05,.18,1)';
  const clone=src.cloneNode(true);
  clone.style.cssText='display:block;overflow:visible;width:'+S.w+'px;height:'+S.h+'px;transition:width .8s cubic-bezier(.45,.05,.18,1),height .8s cubic-bezier(.45,.05,.18,1)';
  wrap.appendChild(clone);wrap.style.transform='translate('+S.x+'px,'+S.y+'px)';
  stage.appendChild(wrap);
  src.style.visibility='hidden';
  activate(idx7,false);
  mLayers[0].style.transition='none';mLayers[0].style.opacity='0';
  if(minfo)minfo.style.opacity='0';
  requestAnimationFrame(()=>requestAnimationFrame(()=>{
    wrap.style.transform='translate('+T.x+'px,'+T.y+'px)';
    clone.style.width=T.w+'px';clone.style.height=T.h+'px';
  }));
  setTimeout(()=>{
    wrap.remove();
    mLayers[0].style.transition='';mLayers[0].style.opacity='';
    if(minfo)minfo.style.opacity='';
    src.style.visibility='';
  },830);
}
function next(){
  if(slides[cur]===smorph&&mIdx<TRACKS.length-1){mGo(mIdx+1);return;}
  if(slides[cur]===sdrum&&eIdx<EVENTS.length-1){eIdx++;drumRender();return;}
  if(cur<TOTAL-1&&slides[cur].classList.contains('s-tilke')&&slides[cur+1]===smorph){flyMainCircuit(cur+1);return;}
  if(cur<TOTAL-1)activate(cur+1,false);
}
function prev(){
  if(slides[cur]===smorph&&mIdx>0){mGo(mIdx-1);return;}
  if(slides[cur]===sdrum&&eIdx>0){eIdx--;drumRender();return;}
  if(cur>0)activate(cur-1,true);
}
document.getElementById('bNext').addEventListener('click',next);
document.getElementById('bPrev').addEventListener('click',prev);

/* ---- edit mode (designMode) ---- */
let editing=false;
function setEdit(on){
  editing=on;
  document.body.classList.toggle('editing',on);
  document.designMode=on?'on':'off';
  if(!on&&window.getSelection)window.getSelection().removeAllRanges();
}
function saveCopy(){
  setEdit(false);
  const clone=document.documentElement.cloneNode(true);
  clone.querySelectorAll('.edbar,.ehint').forEach(n=>n.remove());
  clone.classList.remove('editing');
  const b=new Blob(['<!DOCTYPE html>\n'+clone.outerHTML],{type:'text/html'});
  const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download='sokol-deck-edited.html';a.click();
}
addEventListener('keydown',e=>{
  /* Ctrl/Cmd+S always saves */
  if((e.ctrlKey||e.metaKey)&&(e.key==='s'||e.key==='S')){e.preventDefault();saveCopy();return;}
  if(editing){
    /* while editing: let every key type normally; Esc exits */
    if(e.key==='Escape'){e.preventDefault();setEdit(false);}
    return;
  }
  if(e.key==='ArrowRight'||e.key===' '){e.preventDefault();next();}
  else if(e.key==='ArrowLeft'){e.preventDefault();prev();}
  else if(e.key==='e'||e.key==='E'||e.key==='у'||e.key==='У'){e.preventDefault();setEdit(true);}
});
/* deep-link: ?slide=N (1-based) & step=M for morph */
const startIdx=Math.min(TOTAL-1,Math.max(0,(parseInt(Q.get('slide')||'1',10)||1)-1));
activate(startIdx,false);
if(slides[startIdx]===smorph&&Q.has('step'))mGo(Math.min(TRACKS.length-1,Math.max(0,+Q.get('step')||0)));
if(slides[startIdx]===sdrum&&Q.has('step')){eIdx=Math.min(EVENTS.length-1,Math.max(0,+Q.get('step')||0));drumRender();}
if(Q.has('edit'))setEdit(true);
</script>
</body>
</html>"""

out = (HTML.replace("__BASECSS__", BASECSS)
           .replace("__MAPSVG__", svg)
           .replace("__MINIS__", MINIS)
           .replace("__DRUMLOGOS__", DRUMLOGOS)
           .replace("__DRUMGAUGE__", DRUMGAUGE)
           .replace("__TRACKS__", json.dumps(TRACKS, ensure_ascii=False)))
dst = os.path.join(ROOT, "sokol-deck.html")
open(dst, "w", encoding="utf-8").write(out)
print("written", os.path.getsize(dst), "bytes ->", dst)
