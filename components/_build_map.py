# Generates map.html from the OFFICIAL sokol.kz full map (assets/img/map/full_map.svg).
# True geometry: every track sits at its real position and real relative scale.
import re, os

SRC = r"C:\Users\user\AppData\Local\Temp\sokol_svg\full_map.svg"
DST = r"C:\Users\user\presentation\components\map.html"

svg = open(SRC, encoding="utf-8").read()
svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
svg = re.sub(r"<!--.*?-->\s*", "", svg, flags=re.S)

# wire official groups to legend zones
ZONES = {
    "main_circle": "ring", "karting": "kart", "drag_strip": "drag",
    "drift_arena": "drift", "motocross": "moto", "offroad": "off",
    "paintball": "paint", "museum": "museum", "hotel_restaurant": "hotel",
    "parking": "park", "sokol_roads": "road",
}
for gid, z in ZONES.items():
    svg = svg.replace(f'<g id="{gid}"', f'<g id="{gid}" class="zone" data-zone="{z}"')

# responsive sizing + crisp scaling
svg = svg.replace('<svg id=', '<svg preserveAspectRatio="xMidYMid meet" id=', 1)

LEGEND = """
      <div class="grp">Трассы</div>
      <div class="item" data-zone="ring"   style="--clr:#00afef"><span class="box"></span><span class="nm">Большое кольцо <small>4495 м · авто и мото</small></span></div>
      <div class="item" data-zone="kart"   style="--clr:#43b653"><span class="box"></span><span class="nm">Картодром <small>1650 м · карты</small></span></div>
      <div class="item" data-zone="drag"   style="--clr:#f58634"><span class="box"></span><span class="nm">Драг-стрип <small>402 м</small></span></div>
      <div class="item" data-zone="drift"  style="--clr:#7a75b5"><span class="box"></span><span class="nm">Дрифт-арена <small>16 000 м²</small></span></div>
      <div class="item" data-zone="moto"   style="--clr:#ed2d91"><span class="box"></span><span class="nm">Мотокросс</span></div>
      <div class="item" data-zone="off"    style="--clr:#98ca48"><span class="box"></span><span class="nm">Офф-роуд</span></div>
      <div class="grp">Развлечения</div>
      <div class="item" data-zone="paint"  style="--clr:#00c9ff"><span class="box"></span><span class="nm">Пейнтбол</span></div>
      <div class="item" data-zone="museum" style="--clr:#d92d27"><span class="box"></span><span class="nm">Музей</span></div>
      <div class="item" data-zone="hotel"  style="--clr:#ffb800"><span class="box"></span><span class="nm">Отель и ресторан</span></div>
      <div class="grp">Инфраструктура</div>
      <div class="item" data-zone="park"   style="--clr:#205da4"><span class="box"></span><span class="nm">Парковки</span></div>
      <div class="item" data-zone="road"   style="--clr:#aaaaaa"><span class="box"></span><span class="nm">Дороги</span></div>
      <div class="hintbar">▢ клик — подсветить зону · официальная карта sokol.kz, масштаб 1:1</div>
"""

HTML = """<!DOCTYPE html>
<!-- Motion-graphic component: interactive Sokol complex map.
     Geometry = OFFICIAL sokol.kz full map (assets/img/map/full_map.svg), embedded 1:1.
     Every track is at its real position and real relative scale. -->
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Карта Sokol</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
<style>
:root{--night:#0a0a0f;--primary:#115ffc;--ink:#f4f5fa;--muted:#7e879c;--line:#222a3a}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;background:var(--night);font-family:'Inter',sans-serif;overflow:hidden;color:var(--ink)}
.app{height:100%;display:flex;flex-direction:column;padding:clamp(14px,2.4vw,30px) clamp(16px,3vw,40px)}
.h1{font-family:'Orbitron';font-weight:900;font-size:clamp(20px,3vw,38px);letter-spacing:.01em}
.h2{color:var(--muted);font-size:clamp(11px,1.3vw,15px);margin:6px 0 clamp(12px,2vh,22px)}
.stage{flex:1;display:grid;grid-template-columns:1fr clamp(230px,25vw,320px);gap:clamp(14px,2vw,30px);min-height:0}
/* MAP */
.map{position:relative;background:radial-gradient(120% 100% at 30% 10%,#17202f,#0c111c 70%);border:1px solid var(--line);border-radius:16px;overflow:hidden;padding:clamp(8px,1.4vw,20px)}
.map svg{width:100%;height:100%;display:block}
.zone{transition:opacity .25s,filter .25s;cursor:pointer}
.map.sel .zone:not(.hl){opacity:.13}
.zone.hl{filter:drop-shadow(0 0 6px rgba(255,255,255,.35))}
/* LEGEND */
.legend{overflow:auto;padding-right:4px}
.legend::-webkit-scrollbar{width:6px}.legend::-webkit-scrollbar-thumb{background:#283242;border-radius:6px}
.grp{font-family:'Orbitron';font-weight:700;font-size:11px;letter-spacing:.14em;color:var(--muted);margin:16px 0 8px;text-transform:uppercase}
.grp:first-child{margin-top:0}
.item{display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:9px;cursor:pointer;user-select:none;transition:background .15s}
.item:hover{background:#161d2b}
.box{width:16px;height:16px;border-radius:4px;border:2px solid #38445c;flex:0 0 auto;position:relative;transition:.15s}
.item.on .box{background:var(--clr);border-color:var(--clr);box-shadow:0 0 8px var(--clr)}
.item.on .box::after{content:"";position:absolute;left:4px;top:1px;width:4px;height:8px;border:solid #0a0a0f;border-width:0 2px 2px 0;transform:rotate(45deg)}
.nm{font-size:13.5px;color:#dfe3ee;line-height:1.25}
.nm small{display:block;font-size:10.5px;color:var(--muted);letter-spacing:.03em}
.item.on .nm{color:#fff}
.hintbar{margin-top:14px;font-family:'JetBrains Mono',monospace;font-size:10.5px;color:var(--muted);letter-spacing:.04em;line-height:1.5}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
</head>
<body>
<div class="app">
  <div class="h1">Карта Sokol</div>
  <div class="h2">Официальная схема комплекса — реальные контуры и масштаб · Select zones to highlight</div>
  <div class="stage">
    <div class="map" id="map">
__SVG__
    </div>
    <div class="legend" id="legend">
__LEGEND__
    </div>
  </div>
</div>
<script>
const map=document.getElementById('map');
const items=[...document.querySelectorAll('.item')];
const zones=[...document.querySelectorAll('.zone')];
function zoneEls(z){return zones.filter(e=>e.dataset.zone===z);}
function refresh(){
  const any=items.some(i=>i.classList.contains('on'));
  map.classList.toggle('sel',any);
  document.querySelectorAll('.hl').forEach(e=>e.classList.remove('hl'));
  items.filter(i=>i.classList.contains('on')).forEach(i=>{
    zoneEls(i.dataset.zone).forEach(e=>e.classList.add('hl'));
  });
}
items.forEach(it=>{
  it.addEventListener('click',()=>{it.classList.toggle('on');refresh();});
  it.addEventListener('mouseenter',()=>{
    if(it.classList.contains('on'))return;
    map.classList.add('sel');
    zoneEls(it.dataset.zone).forEach(e=>e.classList.add('hl'));
  });
  it.addEventListener('mouseleave',()=>{
    if(it.classList.contains('on'))return;
    zoneEls(it.dataset.zone).forEach(e=>e.classList.remove('hl'));
    refresh();
  });
});
zones.forEach(z=>{z.addEventListener('click',()=>{
  const it=items.find(i=>i.dataset.zone===z.dataset.zone);if(it){it.classList.toggle('on');refresh();}
});});
// deep-link / testing: ?zone=ring,kart preselects zones
const Q=new URLSearchParams(location.search);
(Q.get('zone')||'').split(',').filter(Boolean).forEach(zn=>{
  const it=items.find(i=>i.dataset.zone===zn);if(it)it.classList.add('on');
});
refresh();
</script>
</body>
</html>"""

out = HTML.replace("__SVG__", svg).replace("__LEGEND__", LEGEND)
open(DST, "w", encoding="utf-8").write(out)
print("written", os.path.getsize(DST), "bytes ->", DST)
