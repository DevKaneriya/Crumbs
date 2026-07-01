"""
Find the visual 'graphic content' area in each icon by analyzing saturation/color intensity.
Icons 1-3 appear to have smaller illustrated content inside the full-bleed circle.
We need to find where the actual illustration sits within each icon.
"""
from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)

    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Compute saturation-like measure: max-min across RGB channels
    # High saturation = colorful graphic content
    max_rgb = np.maximum(np.maximum(r.astype(float), g.astype(float)), b.astype(float))
    min_rgb = np.minimum(np.minimum(r.astype(float), g.astype(float)), b.astype(float))
    saturation = (max_rgb - min_rgb)  # 0 = grey/white/black, high = colorful

    # Also consider dark pixels as content (not white background)
    brightness = (r.astype(float) + g.astype(float) + b.astype(float)) / 3.0

    # Content = saturated OR dark, AND inside the circle (alpha > 50)
    is_inside = a > 50
    is_content = is_inside & ((saturation > 20) | (brightness < 150))

    rows = np.any(is_content, axis=1)
    cols = np.any(is_content, axis=0)

    if rows.any() and cols.any():
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        h = rmax - rmin + 1
        w = cmax - cmin + 1
        cx = (cmin + cmax) / 2
        cy = (rmin + rmax) / 2
        print(f'icon{i}.png: illustration bbox=({cmin},{rmin})-({cmax},{rmax}), '
              f'size={w}x{h}, center=({cx:.0f},{cy:.0f}), '
              f'fills {w/1024*100:.1f}% of canvas width')
    else:
        print(f'icon{i}.png: no illustration content found')
