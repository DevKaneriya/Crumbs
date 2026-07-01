from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    alpha = data[:, :, 3]

    # Sample center row and column to find where the circle edge is
    # The center of the image
    cy, cx = 511, 511

    # Scan from center outward along each axis to find where alpha drops significantly
    # Scan right from center
    center_row_alpha = alpha[cy, :]
    center_col_alpha = alpha[:, cx]

    # Find rightmost pixel with high alpha in center row
    right_edge = np.where(center_row_alpha[cx:] > 128)[0]
    left_edge = np.where(center_row_alpha[:cx] > 128)[0]
    top_edge = np.where(center_col_alpha[:cy] > 128)[0]
    bottom_edge = np.where(center_col_alpha[cy:] > 128)[0]

    if len(right_edge):
        r = right_edge[-1] + cx
    else:
        r = cx
    if len(left_edge):
        l = left_edge[0]
    else:
        l = cx
    if len(top_edge):
        t = top_edge[0]
    else:
        t = cy
    if len(bottom_edge):
        b = bottom_edge[-1] + cy
    else:
        b = cy

    circle_w = r - l + 1
    circle_h = b - t + 1
    print(f'icon{i}.png: circle ~ {circle_w}x{circle_h} px, fills {circle_w/1024*100:.1f}% of canvas')
