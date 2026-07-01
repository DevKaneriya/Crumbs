"""
Compare center crops of icon1 vs icon4 to understand the visual difference.
Sample pixel intensity variation to find where the illustration actually sits.
"""
from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

# For each icon, scan a horizontal line through the center
# and find the range where we see the illustration vs background
for i in [1, 2, 3, 4, 5, 6]:
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    
    # Get center row
    cy = 512
    row = data[cy, :, :]
    
    # Look for the "illustration boundary" — scan from center outward
    # Find where pixels transition from illustration colors to background
    # The background inside the circle is cream/beige (light colors)
    # The illustration has darker/more saturated pixels
    
    r_ch = row[:, 0].astype(float)
    g_ch = row[:, 1].astype(float)
    b_ch = row[:, 2].astype(float)
    a_ch = row[:, 3].astype(float)
    
    # Saturation-like measure
    max_c = np.maximum(np.maximum(r_ch, g_ch), b_ch)
    min_c = np.minimum(np.minimum(r_ch, g_ch), b_ch)
    sat = max_c - min_c
    brightness = (r_ch + g_ch + b_ch) / 3.0
    
    # Content = saturated OR dark, AND inside circle
    is_content = (a_ch > 128) & ((sat > 30) | (brightness < 200))
    
    content_cols = np.where(is_content)[0]
    if len(content_cols) > 0:
        left = content_cols[0]
        right = content_cols[-1]
        illus_width = right - left + 1
        print(f'icon{i}: center row illustration span: {left} to {right}, '
              f'width={illus_width}, fills {illus_width/1024*100:.1f}% of canvas')
    else:
        print(f'icon{i}: no illustration found in center row')

# Also save center 512x512 crops for visual comparison
out_dir = r'd:\Backup\Crumbs\center_crops'
os.makedirs(out_dir, exist_ok=True)
for i in range(1, 7):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path)
    # Center 512x512
    center = img.crop((256, 256, 768, 768))
    center.save(os.path.join(out_dir, f'center{i}.png'))
print("Center crops saved.")
