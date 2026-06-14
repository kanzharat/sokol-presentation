# Pixel-level verification of roads-morph screenshots (can't view images via API right now).
import numpy as np
from PIL import Image

COLORS = {
    "ring_blue":   (42, 168, 255),
    "drag_orange": (255, 140, 66),
    "drift_purple":(139, 123, 255),
    "kart_green":  (52, 208, 88),
    "text_white":  (244, 246, 255),
}

def count_near(im, rgb, tol=60, region=None):
    a = np.array(im.convert("RGB")).astype(int)
    if region:
        x0,y0,x1,y1 = region
        h,w,_ = a.shape
        a = a[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
    d = np.abs(a - np.array(rgb)).sum(axis=2)
    return int((d < tol).sum())

for shot in ["roads2-1","roads2-2","roads2-3"]:
    p = rf"C:\Users\user\presentation\.frontend-slides\shots\{shot}.png"
    im = Image.open(p)
    w,h = im.size
    print(f"--- {shot} ({w}x{h}) ---")
    # right half: should contain the active track contour pixels
    for name,rgb in COLORS.items():
        right = count_near(im, rgb, region=(0.45,0.0,1.0,1.0))
        left  = count_near(im, rgb, region=(0.0,0.0,0.45,1.0))
        print(f"  {name:13s} right={right:7d} left={left:7d}")
