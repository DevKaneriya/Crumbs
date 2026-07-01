from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    alpha = data[:, :, 3]

    # Find bounding box of non-transparent pixels
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    h = rmax - rmin + 1
    w = cmax - cmin + 1
    cx = (cmin + cmax) / 2
    cy = (rmin + rmax) / 2

    print(f'icon{i}.png: bbox=({cmin},{rmin})-({cmax},{rmax}), size={w}x{h}, center=({cx:.1f},{cy:.1f}), fill={w/1024*100:.1f}%')
