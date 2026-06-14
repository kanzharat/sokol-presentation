# Captures sokol-ads PPTX source screenshots
param([switch]$Debug)
$edge="C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if(-not(Test-Path $edge)){$edge="C:\Program Files\Microsoft\Edge\Application\msedge.exe"}
$out="C:\Users\user\presentation\ads\shots"
New-Item -ItemType Directory -Force $out | Out-Null
$ud="$env:TEMP\edge-ads"
$base="file:///C:/Users/user/presentation/ads/sokol-ads.html"

if($Debug){
  foreach($n in 1..5){
    & $edge --headless=new --disable-gpu --user-data-dir=$ud --window-size=1920,1080 --screenshot="$out\dbg$n.png" --virtual-time-budget=6000 "$base`?slide=$n&boxes=1" 2>$null | Out-Null
  }
  "debug shots done"
  exit
}

# slide backgrounds @2x (window-size is CSS px; screenshot = CSS px * dsf)
foreach($n in 1..5){
  & $edge --headless=new --disable-gpu --user-data-dir=$ud --window-size=1920,1080 --force-device-scale-factor=2 --screenshot="$out\bg$n.png" --virtual-time-budget=8000 "$base`?slide=$n&shoot=1" 2>$null | Out-Null
}
# transparent objects @2x  (name -> CSS design size)
$objs=@{ "ledtxt3"=@(350,525); "ledtxt4"=@(900,630); "wing"=@(760,560) }
foreach($k in $objs.Keys){
  $w=$objs[$k][0]; $h=$objs[$k][1]
  & $edge --headless=new --disable-gpu --user-data-dir=$ud --default-background-color=00000000 --window-size=$w,$h --force-device-scale-factor=2 --screenshot="$out\obj-$k.png" --virtual-time-budget=6000 "$base`?obj=$k" 2>$null | Out-Null
}
(Get-ChildItem "$out\*.png" | Measure-Object).Count
