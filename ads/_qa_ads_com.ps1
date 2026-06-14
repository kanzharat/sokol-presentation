# PowerPoint COM QA: verify transitions, export slide renders.
$path = "C:\Users\user\presentation\sokol-ads.pptx"
$qa = "C:\Users\user\presentation\ads\qa"
New-Item -ItemType Directory -Force $qa | Out-Null
Remove-Item "$qa\*.png" -ErrorAction SilentlyContinue

$pp = New-Object -ComObject PowerPoint.Application
$pres = $pp.Presentations.Open($path, $false, $false, $false)
try {
  "slides: $($pres.Slides.Count)"
  foreach($sl in $pres.Slides){
    $fx = $sl.SlideShowTransition.EntryEffect
    "slide $($sl.SlideIndex): EntryEffect=$fx  shapes=$($sl.Shapes.Count)"
    $n = "{0:d2}" -f $sl.SlideIndex
    $sl.Export("$qa\q$n.png", "PNG", 1280, 720)
  }
} finally {
  $pres.Close()
  $pp.Quit()
}
"qa done"
