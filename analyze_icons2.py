from PIL import Image
import numpy as np
import os

assets_dir = r'd:\Backup\Crumbs\frontend\src\assets'

# For each icon, analyze the distinct content (non-background) region
# by looking at the center color vs edge to find the actual graphic element
for i in range(1, 10):
    path = os.path.join(assets_dir, f'icon{i}.png')
    img = Image.open(path).convert('RGBA')
    data = np.array(img)
    
    # Sample the corners to get background color
    corners = [data[10,10], data[10,-10], data[-10,10], data[-10,-10]]
    bg_alpha = np.mean([c[3] for c in corners])
    
    # If background is mostly transparent, find content bounding box
    alpha = data[:, :, 3]
    
    # Check if this icon has a solid circular bg by sampling edge pixels
    edge_pixels_alpha = np.concatenate([
        alpha[0, :], alpha[-1, :], alpha[:, 0], alpha[:, -1]
    ])
    edge_mean_alpha = np.mean(edge_pixels_alpha)
    
    # Sample what percentage of pixels are "nearly white" (background within circle)
    rgb = data[:, :, :3]
    is_white_ish = (rgb[:,:,0] > 220) & (rgb[:,:,1] > 220) & (rgb[:,:,2] > 220) & (alpha > 128)
    white_ratio = np.sum(is_white_ish) / (1024 * 1024) * 100
    
    print(f'icon{i}.png: edge_alpha={edge_mean_alpha:.1f}, white_ratio={white_ratio:.1f}%')
    
    # Save a small thumbnail to check visually
    thumb = img.resize((200, 200), Image.LANCZOS)
    thumb.save(os.path.join(r'd:\Backup\Crumbs', f'thumb{i}.png'))

print("Thumbnails saved to d:\\Backup\\Crumbs\\")
