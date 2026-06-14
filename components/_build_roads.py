# Generates roads-morph.html from official sokol.kz track SVGs (tracks.json).
import json, os

t = json.load(open(r"C:\Users\user\AppData\Local\Temp\sokol_svg\tracks.json", encoding="utf-8"))

def trk(key, render, sw):
    v = t[key]
    return {"vb": v["viewBox"], "paths": v["paths"], "render": render, "sw": sw}

tracks = [
 dict(id="ring",  c="#2aa8ff", kic="ТРАССА 01 · MAIN CIRCUIT", nm="Большое кольцо", en="Sokol International Circuit",
      desc="Главная гоночная трасса комплекса — для автомобилей и мотоциклов, по проекту Hermann Tilke. Готова принимать этапы MotoGP, WTCC, DTM и Superbike.",
      specs=[("4495 м","протяжённость"),("15 м","ширина полотна"),("300+ км/ч","скорость на прямой"),("5 / 8","правых / левых поворотов")],
      **trk("main-circuit","stroke",420)),
 dict(id="drag",  c="#ff8c42", kic="ТРАССА 02 · DRAG STRIP", nm="Драг-стрип", en="Drag Racing Strip",
      desc="Прямая 402 м с барьерами безопасности и телеметрией «RaceAmerica». Коридоры возврата позволяют проводить заезды без задержек.",
      specs=[("402 м","дрэг-стрип"),("866 м","общая длина"),("348 м","тормозной участок"),("2500–3000","вместимость трибун")],
      **trk("drag-strip","fill",0)),
 dict(id="drift", c="#8b7bff", kic="ТРАССА 03 · DRIFT ARENA", nm="Дрифт-арена", en="Drift Arena",
      desc="Площадка для управляемого заноса со специальными ограждениями и зонами вылета. Здесь проходят знаковые чемпионаты по дрифту.",
      specs=[("16 000 м²","площадь арены"),("до 1500","вместимость трибун"),("15+","событий в год"),("FIA","стандарты безопасности")],
      **trk("drift-arena","stroke",360)),
 dict(id="kart",  c="#34d058", kic="ТРАССА 04 · KARTODROM", nm="Картодром", en="Karting Track",
      desc="Компактный трек для картинга — почти в 3 раза короче Большого кольца. Единственный в Казахстане картодром с телеметрией: 7 конфигураций и 12 боксов.",
      specs=[("1650 м","длина трека"),("10 м","ширина"),("14 / 10","правых / левых поворотов"),("7","конфигураций")],
      **trk("kartodrom","fill",0)),
 dict(id="moto",  c="#ed2d91", kic="ТРАССА 05 · MOTOCROSS", nm="Мотокросс", en="Motocross Track", gen=True,
      desc="Грунтовая трасса для мотокросса с трамплинами, контруклонами и зрительскими зонами вдоль ключевых секций. Площадка для национальных и региональных этапов.",
      specs=[("~1500 м","длина круга"),("грунт","покрытие"),("12+","трамплинов и волн"),("MX1 / MX2","классы техники")],
      **trk("motocross","stroke",420)),
 dict(id="off",   c="#98ca48", kic="ТРАССА 06 · OFFROAD", nm="Офф-роуд", en="Offroad Park", gen=True,
      desc="Внедорожный полигон с естественным рельефом: подъёмы, спуски, диагонали и каменистые секции. Формат для тест-драйвов 4×4, ATV и корпоративных программ.",
      specs=[("4×4 / ATV","форматы техники"),("рельеф","естественные препятствия"),("тест-драйвы","партнёрские программы"),("круглый год","сезонность")],
      **trk("offroad","stroke",470)),
]

HTML = r"""<!DOCTYPE html>
<!-- Motion-graphic component: Morph-style presentation of Sokol roads.
     Official track outlines from sokol.kz (assets/img/tracks/*.svg).
     Active road sharp w/ info on the left; next roads behind-right, blurred.
     On advance: front road exits, the next one morphs into its place. -->
<html lang="ru">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sokol Roads — Morph</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Play:wght@700&family=JetBrains+Mono:wght@400;600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{--night:#0a0a0f;--primary:#115ffc;--accent:#ff5733;--warm:#ff8c42;--ink:#f4f6ff;--muted:#8a91a6}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:100%;height:100%;background:radial-gradient(130% 110% at 72% 30%,#10141f,#06070b 70%);font-family:'Inter',sans-serif;overflow:hidden;color:var(--ink)}
.stage{position:relative;width:100%;height:100%}
/* ===== road contour layers (right side) ===== */
.layer{position:absolute;top:50%;left:58%;width:min(54vw,62vh);aspect-ratio:1.25;transform-origin:center;
  will-change:transform,filter,opacity;pointer-events:none;
  transition:transform .9s cubic-bezier(.45,.05,.18,1),filter .9s ease,opacity .9s ease}
.layer svg{width:100%;height:100%;overflow:visible}
.layer .tk{filter:drop-shadow(0 0 14px var(--c))}
/* positions: front sharp / behind blurred (like the reference) */
.layer.p0{transform:translate(-50%,-50%) scale(1);filter:none;opacity:1;z-index:30}
.layer.p1{transform:translate(-8%,-72%) scale(.55);filter:blur(7px) brightness(.7) saturate(.85);opacity:.45;z-index:20}
.layer.p2{transform:translate(28%,-86%) scale(.38);filter:blur(12px) brightness(.5);opacity:.25;z-index:10}
.layer.hid{transform:translate(48%,-95%) scale(.3);filter:blur(16px);opacity:0;z-index:5}
.layer.out{transform:translate(-115%,-28%) scale(1.18);filter:blur(10px) brightness(.55);opacity:0;z-index:35}
/* ===== info panel (left) ===== */
.info{position:absolute;left:clamp(26px,5vw,86px);top:50%;transform:translateY(-50%);width:min(38vw,520px);z-index:40}
.kic{font-family:'JetBrains Mono',monospace;font-size:clamp(.55rem,1vw,.8rem);letter-spacing:.3em;color:var(--c,#ff8c42)}
.genb{display:inline-block;font-family:'JetBrains Mono',monospace;font-size:clamp(.46rem,.8vw,.62rem);letter-spacing:.16em;text-transform:uppercase;
  color:#ffb84d;border:1px dashed rgba(255,184,77,.45);border-radius:6px;padding:.4em .8em;margin-bottom:1em}
.nm{font-family:'Orbitron';font-weight:900;font-size:clamp(1.8rem,4.6vw,4rem);line-height:.95;text-transform:uppercase;margin:.3em 0 .12em}
.en{font-family:'Play';color:var(--muted);font-size:clamp(.7rem,1.4vw,1.1rem);letter-spacing:.06em;margin-bottom:1em}
.desc{font-weight:300;color:#c9cedd;font-size:clamp(.66rem,1.25vw,1rem);line-height:1.6;max-width:44ch;margin-bottom:1.4em}
.specs{display:grid;grid-template-columns:1fr 1fr;gap:clamp(8px,1.4vh,16px) clamp(14px,2vw,26px)}
.spec b{display:block;font-family:'Orbitron';font-weight:700;font-size:clamp(.85rem,1.9vw,1.5rem);color:#fff}
.spec span{font-size:clamp(.52rem,1vw,.8rem);color:var(--muted);letter-spacing:.04em}
.spec{border-left:3px solid var(--c,#ff8c42);padding-left:.8em}
/* info morph animation */
.info .a{opacity:0;transform:translateY(18px);animation:up .6s cubic-bezier(.2,.8,.2,1) forwards}
.info .a1{animation-delay:.15s}.info .a2{animation-delay:.24s}.info .a3{animation-delay:.33s}.info .a4{animation-delay:.42s}.info .a5{animation-delay:.5s}
@keyframes up{to{opacity:1;transform:translateY(0)}}
/* ===== chrome ===== */
.top{position:absolute;top:clamp(16px,3vh,30px);left:clamp(26px,5vw,86px);right:clamp(26px,5vw,86px);display:flex;align-items:center;gap:14px;z-index:50;
  font-family:'JetBrains Mono',monospace;font-size:clamp(.55rem,1vw,.8rem);letter-spacing:.2em;color:var(--muted);text-transform:uppercase}
.top .cnt{margin-left:auto;font-family:'Orbitron';font-size:1.3em}.top .cnt b{color:#fff}
.ctrl{position:absolute;bottom:clamp(16px,3.4vh,34px);left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:14px;z-index:50}
.btn{width:clamp(36px,3.6vw,46px);height:clamp(36px,3.6vw,46px);border-radius:50%;border:1px solid #2a3146;background:rgba(14,17,28,.8);color:#cfd5e6;font-size:17px;cursor:pointer;transition:.15s}
.btn:hover{border-color:var(--primary);color:#fff}
.dots{display:flex;gap:8px}
.dot{width:8px;height:8px;border-radius:50%;background:#2c3346;cursor:pointer;transition:.3s;border:0}
.dot.on{background:var(--primary);width:24px;border-radius:5px}
@media (prefers-reduced-motion:reduce){.layer{transition:none}.info .a{animation:none;opacity:1;transform:none}}
.notrans .layer{transition:none}.notrans .info .a{animation:none;opacity:1;transform:none}
</style>
</head>
<body>
<div class="stage" id="stage">
  <div class="top"><span>Трассы Sokol · Roads</span><span class="cnt"><b id="cur">01</b> / <span id="tot">04</span></span></div>
  <div class="info" id="info"></div>
  <div class="ctrl">
    <button class="btn" id="prev" aria-label="Назад">‹</button>
    <div class="dots" id="dots"></div>
    <button class="btn" id="next" aria-label="Вперёд">›</button>
  </div>
</div>
<script>
const Q=new URLSearchParams(location.search); // ?slide=N&noauto=1 for deep-link / testing
const TRACKS=__DATA__;
const stage=document.getElementById('stage'),info=document.getElementById('info'),dots=document.getElementById('dots');
const N=TRACKS.length;let active=Math.min(N-1,Math.max(0,parseInt(Q.get('slide')||'0',10)||0)),prevA=-1;
document.getElementById('tot').textContent=String(N).padStart(2,'0');
TRACKS.forEach((r,i)=>{
  const el=document.createElement('div');el.className='layer';el.style.setProperty('--c',r.c);
  const body=r.paths.map(d=>r.render==='fill'
    ?`<path class="tk" d="${d}" fill="${r.c}" fill-rule="evenodd"/>`
    :`<path class="tk" d="${d}" fill="none" stroke="${r.c}" stroke-width="${r.sw}" stroke-linecap="round" stroke-linejoin="round"/>`).join('');
  el.innerHTML=`<svg viewBox="${r.vb}" preserveAspectRatio="xMidYMid meet">${body}</svg>`;
  stage.appendChild(el);
  const d=document.createElement('button');d.className='dot';d.addEventListener('click',()=>go(i));dots.appendChild(d);
});
const layers=[...document.querySelectorAll('.layer')],dotEls=[...dots.children];
function renderInfo(r){
  info.style.setProperty('--c',r.c);
  info.innerHTML=`${r.gen?'<div class="genb a a1">⚠ текст сгенерирован — заменить реальными данными</div>':''}
   <div class="kic a a1">${r.kic}</div><h1 class="nm a a2">${r.nm}</h1><div class="en a a3">${r.en}</div>
   <p class="desc a a4">${r.desc}</p>
   <div class="specs a a5">${r.specs.map(s=>`<div class="spec"><b>${s[0]}</b><span>${s[1]}</span></div>`).join('')}</div>`;
}
function layout(){
  layers.forEach((el,i)=>{
    const off=(i-active+N)%N;
    el.classList.remove('p0','p1','p2','hid','out');
    if(i===prevA&&off!==0)el.classList.add('out');
    else if(off===0)el.classList.add('p0');
    else if(off===1)el.classList.add('p1');
    else if(off===2)el.classList.add('p2');
    else el.classList.add('hid');
  });
  dotEls.forEach((d,i)=>d.classList.toggle('on',i===active));
  document.getElementById('cur').textContent=String(active+1).padStart(2,'0');
  renderInfo(TRACKS[active]);
}
function go(i){prevA=active;active=(i+N)%N;layout();restart();}
const next=()=>go(active+1),prev=()=>go(active-1);
document.getElementById('next').addEventListener('click',next);
document.getElementById('prev').addEventListener('click',prev);
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')next();if(e.key==='ArrowLeft')prev();});
const AUTO=!Q.has('noauto');
let timer=AUTO?setInterval(next,5000):null;
const restart=()=>{if(!AUTO)return;clearInterval(timer);timer=setInterval(next,5000);};
stage.addEventListener('pointerdown',()=>clearInterval(timer));
if(Q.has('noauto'))document.documentElement.classList.add('notrans');
layout();
</script>
</body>
</html>"""

# specs are tuples -> lists for JSON
for tr in tracks:
    tr["specs"] = [list(s) for s in tr["specs"]]

out = HTML.replace("__DATA__", json.dumps(tracks, ensure_ascii=False))
dst = r"C:\Users\user\presentation\components\roads-morph.html"
open(dst, "w", encoding="utf-8").write(out)
print("written", os.path.getsize(dst), "bytes ->", dst)
