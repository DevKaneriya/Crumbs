"""
Save center crops of all icons at the same size so we can visually compare.
Also analyze the contrast/saturation to find the 'graphic content' region 
vs the background circle fill.
"""
from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'
out_dir = r'd:\Backup\Crumbs\crops'
os.makedirs(out_dir, exist_ok=True)

for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)

    # Convert to HSV-ish: look for saturated/non-white content
    rgb = data[:, :, :3].astype(float)
    alpha = data[:, :, 3]

    # "content" = pixels that are not near-white AND are inside the circle (alpha > 128)
    # white-ish = R>200 AND G>200 AND B>200
    is_inside = alpha > 128
    is_not_white = ~((rgb[:,:,0] > 200) & (rgb[:,:,1] > 200) & (rgb[:,:,2] > 200))
    is_not_black = ~((rgb[:,:,0] < 30) & (rgb[:,:,1] < 30) & (rgb[:,:,2] < 30))
    is_content = is_inside & is_not_white & is_not_black

    rows = np.any(is_content, axis=1)
    cols = np.any(is_content, axis=0)

    if rows.any() and cols.any():
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        h = rmax - rmin + 1
        w = cmax - cmin + 1
        print(f'icon{i}.png: graphic content bbox=({cmin},{rmin})-({cmax},{rmax}), size={w}x{h}, fills {w/1024*100:.1f}% of canvas')
    else:
        print(f'icon{i}.png: no non-white content found')

    # Save a center 400px crop for visual check
    center = img.crop((312, 312, 712, 712))
    center.save(os.path.join(out_dir, f'crop{i}.png'))
