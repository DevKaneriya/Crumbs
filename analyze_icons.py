from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'
for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    # Find non-transparent pixels
    alpha = data[:, :, 3]
    rows = np.any(alpha > 10, axis=1)
    cols = np.any(alpha > 10, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    content_h = rmax - rmin
    content_w = cmax - cmin
    padding_top = rmin
    padding_left = cmin
    print(f'icon{i}.png: content={content_w}x{content_h}, offset=({cmin},{rmin}), padding %={(content_w/1024*100):.1f}% of image width')
