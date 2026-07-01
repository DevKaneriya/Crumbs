"""
Scale the illustration content within icons 1-3 to match the visual weight 
of icons 4-9.

Approach: For each icon, detect the bounding box of the actual illustration
content (the colored/dark illustration inside the white circle background),
then scale it up to match a target fill ratio.
"""
from PIL import Image, ImageFilter
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

def get_illustration_bbox(img_array):
    """
    Find bounding box of the illustration (non-white, non-transparent content)
    inside the circular background.
    """
    r, g, b, a = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2], img_array[:,:,3]
    
    # Inside circle = high alpha
    is_inside = a > 128
    
    # Illustration content = not white (cream/beige background of circle)
    # White circle background is R>230, G>220, B>200
    is_bg = (r.astype(float) > 230) & (g.astype(float) > 210) & (b.astype(float) > 190) & is_inside
    is_content = is_inside & ~is_bg
    
    rows = np.any(is_content, axis=1)
    cols = np.any(is_content, axis=0)
    
    if not rows.any():
        return None
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    return (cmin, rmin, cmax, rmax)

def get_bbox_size(bbox):
    if bbox is None:
        return 0, 0
    return bbox[2] - bbox[0] + 1, bbox[3] - bbox[1] + 1

# Analyze all icons
print("Analyzing icons...")
for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    bbox = get_illustration_bbox(data)
    w, h = get_bbox_size(bbox)
    if bbox:
        cx = (bbox[0] + bbox[2]) / 2
        cy = (bbox[1] + bbox[3]) / 2
        print(f'icon{i}.png: illus bbox={bbox}, size={w}x{h}, '
              f'center=({cx:.0f},{cy:.0f}), fills {w/1024*100:.1f}% of canvas')
    else:
        print(f'icon{i}.png: no illustration found')
